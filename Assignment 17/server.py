#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TkSocketChat - Server
A lightweight, multi-client chat server using TCP sockets and JSON lines.
Author: ChatGPT (for Ranit Saha)
License: MIT
"""
import argparse
import json
import socket
import threading
from datetime import datetime
from typing import Dict, Tuple, List

ENCODING = "utf-8"
BUF_SIZE = 4096

def now_iso() -> str:
    return datetime.utcnow().isoformat(timespec="seconds") + "Z"

class Client:
    def __init__(self, sock: socket.socket, addr: Tuple[str, int]):
        self.sock = sock
        self.addr = addr
        self.username = None
        self.lock = threading.Lock()
        self.alive = True
        self.rfile = sock.makefile('r', encoding=ENCODING, newline='\n')
        self.wfile = sock.makefile('w', encoding=ENCODING, newline='\n')

    def send_json(self, obj: dict):
        try:
            with self.lock:
                self.wfile.write(json.dumps(obj, ensure_ascii=False) + "\n")
                self.wfile.flush()
        except Exception:
            self.alive = False

    def close(self):
        try:
            self.alive = False
            try:
                self.rfile.close()
            except Exception:
                pass
            try:
                self.wfile.close()
            except Exception:
                pass
            self.sock.close()
        except Exception:
            pass

class ChatServer:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.clients: Dict[socket.socket, Client] = {}
        self.clients_lock = threading.Lock()
        self.running = False

    def start(self):
        self.server_sock.bind((self.host, self.port))
        self.server_sock.listen(50)
        self.running = True
        print(f"[{now_iso()}] Server listening on {self.host}:{self.port}")
        threading.Thread(target=self.accept_loop, daemon=True).start()
        try:
            while self.running:
                # keep the main thread alive
                threading.Event().wait(1.0)
        except KeyboardInterrupt:
            print("\nShutting down...")
        finally:
            self.shutdown()

    def shutdown(self):
        self.running = False
        with self.clients_lock:
            for c in list(self.clients.values()):
                c.close()
            self.clients.clear()
        try:
            self.server_sock.close()
        except Exception:
            pass
        print(f"[{now_iso()}] Server stopped.")

    def accept_loop(self):
        while self.running:
            try:
                sock, addr = self.server_sock.accept()
                client = Client(sock, addr)
                with self.clients_lock:
                    self.clients[sock] = client
                threading.Thread(target=self.client_loop, args=(client,), daemon=True).start()
            except OSError:
                break

    def broadcast(self, obj: dict, exclude: Client = None):
        dead = []
        with self.clients_lock:
            for c in self.clients.values():
                if c is exclude:
                    continue
                c.send_json(obj)
                if not c.alive:
                    dead.append(c)
            for d in dead:
                self._remove_client(d)

    def _remove_client(self, client: Client):
        # Called with clients_lock held
        for sock, c in list(self.clients.items()):
            if c is client:
                try:
                    c.close()
                finally:
                    del self.clients[sock]
                break

    def user_list(self) -> List[str]:
        with self.clients_lock:
            return [c.username for c in self.clients.values() if c.username]

    def send_userlist(self):
        users = self.user_list()
        self.broadcast({"type": "userlist", "users": users, "ts": now_iso()})

    def client_loop(self, client: Client):
        addr = f"{client.addr[0]}:{client.addr[1]}"
        print(f"[{now_iso()}] Connection from {addr}")
        try:
            # Expect a join message first
            line = client.rfile.readline()
            if not line:
                raise ConnectionError("No join message")
            msg = json.loads(line)
            if msg.get("type") != "join" or not msg.get("username"):
                raise ValueError("Invalid join message")
            username = str(msg["username"])[:24].strip()
            if not username:
                raise ValueError("Empty username")
            client.username = username

            # Announce join
            self.broadcast({"type": "system", "text": f"🟢 {username} joined the chat.", "ts": now_iso()})
            self.send_userlist()

            # Send welcome to the client
            client.send_json({"type": "system", "text": f"Welcome, {username}! You are connected.", "ts": now_iso()})

            # Main read loop
            while self.running and client.alive:
                line = client.rfile.readline()
                if not line:
                    break
                try:
                    msg = json.loads(line)
                except json.JSONDecodeError:
                    continue
                mtype = msg.get("type")
                if mtype == "chat":
                    text = (msg.get("text") or "").strip()
                    if text:
                        payload = {
                            "type": "chat",
                            "from": client.username,
                            "text": text,
                            "ts": now_iso(),
                        }
                        self.broadcast(payload)  # send to all, including sender for consistency
                elif mtype == "ping":
                    client.send_json({"type": "pong", "ts": now_iso()})
                elif mtype == "quit":
                    break
                else:
                    # ignore unknown
                    pass
        except Exception as e:
            # print(f"[{now_iso()}] Error with client {addr}: {e}")
            pass
        finally:
            uname = client.username or addr
            with self.clients_lock:
                self._remove_client(client)
            self.broadcast({"type": "system", "text": f"🔴 {uname} left the chat.", "ts": now_iso()})
            self.send_userlist()
            print(f"[{now_iso()}] Disconnected {addr}")

def parse_args():
    ap = argparse.ArgumentParser(description="TkSocketChat Server")
    ap.add_argument("--host", default="0.0.0.0", help="Bind address (default: 0.0.0.0)")
    ap.add_argument("--port", type=int, default=5050, help="Port (default: 5050)")
    return ap.parse_args()

if __name__ == "__main__":
    args = parse_args()
    server = ChatServer(args.host, args.port)
    server.start()
