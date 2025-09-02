#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TkSocketChat - Client (Tkinter UI)
"""
import json
import queue
import socket
import threading
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText
from datetime import datetime

ENCODING = "utf-8"

def ts_to_local(ts: str) -> str:
    try:
        # ts like 2025-01-01T12:34:56Z
        dt = datetime.fromisoformat(ts.replace("Z","+00:00")).astimezone()
        return dt.strftime("%H:%M:%S")
    except Exception:
        return ""

class ChatClientUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        root.title("TkSocketChat • Client")
        root.minsize(820, 520)
        root.protocol("WM_DELETE_WINDOW", self.on_close)

        # Colors
        self.themes = {
            "Light": {
                "bg": "#f8fafc", "panel": "#ffffff", "accent": "#2563eb",
                "text": "#0f172a", "muted": "#475569", "input_bg": "#ffffff",
            },
            "Dark": {
                "bg": "#0b1020", "panel": "#0f172a", "accent": "#60a5fa",
                "text": "#e5e7eb", "muted": "#94a3b8", "input_bg": "#111827",
            },
        }
        self.theme_name = "Light"
        self.sock = None
        self.rf = None
        self.wf = None
        self.read_thread = None
        self.msg_queue = queue.Queue()
        self.connected = False
        self.username = ""
        self.server = ("127.0.0.1", 5050)

        self._build_ui()
        self.apply_theme()
        # open connect dialog on start
        self.root.after(200, self.open_connect_dialog)
        # poll queue
        self.root.after(100, self.process_queue)

    def _build_ui(self):
        self.root.configure(padx=10, pady=10)

        # Header
        header = ttk.Frame(self.root)
        header.pack(side="top", fill="x")
        self.status_lbl = ttk.Label(header, text="Disconnected", font=("Segoe UI", 11))
        self.status_lbl.pack(side="left")
        ttk.Button(header, text="Connect", command=self.open_connect_dialog).pack(side="right", padx=(6,0))
        ttk.Button(header, text="Theme", command=self.toggle_theme).pack(side="right")

        # Main layout
        main = ttk.Frame(self.root)
        main.pack(side="top", fill="both", expand=True, pady=(10, 0))

        # Left: chat area
        left = ttk.Frame(main)
        left.pack(side="left", fill="both", expand=True)

        self.chat = ScrolledText(left, wrap="word", state="disabled", height=18, font=("Segoe UI", 11))
        self.chat.pack(side="top", fill="both", expand=True)

        # message entry row
        entry_row = ttk.Frame(left)
        entry_row.pack(side="top", fill="x", pady=(10,0))
        self.msg_entry = tk.Text(entry_row, height=2, font=("Segoe UI", 11))
        self.msg_entry.pack(side="left", fill="x", expand=True)
        self.msg_entry.bind("<Return>", self.on_enter)
        self.msg_entry.bind("<Shift-Return>", lambda e: None)  # allow newline
        send_btn = ttk.Button(entry_row, text="Send ➤", command=self.send_message)
        send_btn.pack(side="left", padx=(8,0))

        # Right: users
        right = ttk.Frame(main, width=200)
        right.pack(side="left", fill="y", padx=(10,0))
        ttk.Label(right, text="Online Users", font=("Segoe UI", 11, "bold")).pack(anchor="w")
        self.user_list = tk.Listbox(right, height=10)
        self.user_list.pack(fill="both", expand=True, pady=(6,0))

        # Footer
        footer = ttk.Frame(self.root)
        footer.pack(side="top", fill="x", pady=(10,0))
        self.tip_lbl = ttk.Label(footer, text="Tip: Press Enter to send, Shift+Enter for a new line.", font=("Segoe UI", 9))
        self.tip_lbl.pack(side="left")

        # Style tweaks
        self.style = ttk.Style(self.root)
        # Use default theme then adjust colors via widget config in apply_theme()

    def apply_theme(self):
        theme = self.themes[self.theme_name]
        self.root.configure(bg=theme["bg"])
        for w in self.root.winfo_children():
            try:
                w.configure(style="")
            except Exception:
                pass
        # Chat
        self.chat.configure(bg=theme["panel"], fg=theme["text"], insertbackground=theme["text"])
        # Entry
        self.msg_entry.configure(bg=theme["input_bg"], fg=theme["text"], insertbackground=theme["text"])
        # Listbox
        self.user_list.configure(bg=theme["panel"], fg=theme["text"], selectbackground=theme["accent"])
        # Labels
        self.status_lbl.configure(foreground=theme["muted"])
        self.tip_lbl.configure(foreground=theme["muted"])

    def toggle_theme(self):
        self.theme_name = "Dark" if self.theme_name == "Light" else "Light"
        self.apply_theme()

    def open_connect_dialog(self):
        dlg = tk.Toplevel(self.root)
        dlg.title("Connect to Server")
        dlg.transient(self.root)
        dlg.grab_set()
        dlg.resizable(False, False)
        ttk.Label(dlg, text="Server Host").grid(row=0, column=0, sticky="w", padx=10, pady=(10,0))
        host_var = tk.StringVar(value=self.server[0])
        ttk.Entry(dlg, textvariable=host_var, width=28).grid(row=0, column=1, padx=10, pady=(10,0))
        ttk.Label(dlg, text="Port").grid(row=1, column=0, sticky="w", padx=10, pady=(10,0))
        port_var = tk.IntVar(value=self.server[1])
        ttk.Entry(dlg, textvariable=port_var, width=10).grid(row=1, column=1, sticky="w", padx=10, pady=(10,0))
        ttk.Label(dlg, text="Username").grid(row=2, column=0, sticky="w", padx=10, pady=(10,0))
        uname_var = tk.StringVar(value=self.username or "")
        ttk.Entry(dlg, textvariable=uname_var, width=28).grid(row=2, column=1, padx=10, pady=(10,0))

        def do_connect():
            host = host_var.get().strip() or "127.0.0.1"
            port = int(port_var.get())
            uname = uname_var.get().strip() or "Guest"
            dlg.destroy()
            self.connect((host, port), uname)

        btn = ttk.Button(dlg, text="Connect", command=do_connect)
        btn.grid(row=3, column=0, columnspan=2, pady=12)
        dlg.bind("<Return>", lambda e: do_connect())

    # --------------- networking ---------------
    def connect(self, server, username: str):
        if self.connected:
            messagebox.showinfo("Already Connected", "You are already connected.")
            return
        self.server = server
        self.username = username[:24]
        try:
            sock = socket.create_connection(server, timeout=6)
            self.sock = sock
            self.rf = sock.makefile("r", encoding=ENCODING, newline="\n")
            self.wf = sock.makefile("w", encoding=ENCODING, newline="\n")
            # send join
            self._send_json({"type": "join", "username": self.username})
            self.connected = True
            self.set_status(f"Connected to {server[0]}:{server[1]} as {self.username}")
            self.append_system(f"Connected. Say hello 👋")
            self.read_thread = threading.Thread(target=self.read_loop, daemon=True)
            self.read_thread.start()
        except Exception as e:
            self.append_system(f"Failed to connect: {e}")
            self.set_status("Disconnected")
            self.connected = False

    def _send_json(self, obj: dict):
        try:
            self.wf.write(json.dumps(obj, ensure_ascii=False) + "\n")
            self.wf.flush()
        except Exception as e:
            self.append_system(f"Send error: {e}")
            self.disconnect()

    def read_loop(self):
        try:
            while self.connected:
                line = self.rf.readline()
                if not line:
                    break
                try:
                    msg = json.loads(line)
                except json.JSONDecodeError:
                    continue
                self.msg_queue.put(msg)
        except Exception:
            pass
        finally:
            self.msg_queue.put({"type": "system", "text": "Connection closed by server."})
            self.connected = False

    def process_queue(self):
        try:
            while True:
                msg = self.msg_queue.get_nowait()
                self.handle_message(msg)
        except queue.Empty:
            pass
        self.root.after(100, self.process_queue)

    def handle_message(self, msg: dict):
        mtype = msg.get("type")
        if mtype == "chat":
            ts = ts_to_local(msg.get("ts", ""))
            sender = msg.get("from", "?")
            text = msg.get("text", "")
            self.append_chat(sender, text, ts)
        elif mtype == "system":
            text = msg.get("text", "")
            self.append_system(text)
        elif mtype == "userlist":
            users = msg.get("users", [])
            self.user_list.delete(0, tk.END)
            for u in users:
                self.user_list.insert(tk.END, u)
        elif mtype == "pong":
            # ignore in UI
            pass

    def send_message(self):
        text = self.msg_entry.get("1.0", "end-1c").strip()
        if not text:
            return
        self.msg_entry.delete("1.0", "end")
        if not self.connected:
            self.append_system("You are not connected.")
            return
        self._send_json({"type": "chat", "text": text})

    def on_enter(self, event):
        # Enter sends; Shift+Enter inserts newline
        if event.state & 0x0001:  # Shift
            return
        self.send_message()
        return "break"

    def append_chat(self, sender: str, text: str, ts: str):
        self.chat.configure(state="normal")
        theme = self._theme()
        self.chat.insert("end", f"[{ts}] ", ("ts",))
        self.chat.insert("end", f"{sender}: ", ("name",))
        self.chat.insert("end", f"{text}\n", ("msg",))
        self.chat.tag_config("ts", foreground=theme["muted"])
        self.chat.tag_config("name", foreground=theme["accent"])
        self.chat.tag_config("msg", foreground=theme["text"])
        self.chat.see("end")
        self.chat.configure(state="disabled")

    def append_system(self, text: str):
        self.chat.configure(state="normal")
        theme = self._theme()
        self.chat.insert("end", f"• {text}\n", ("sys",))
        self.chat.tag_config("sys", foreground=theme["muted"])
        self.chat.see("end")
        self.chat.configure(state="disabled")

    def _theme(self):
        return self.themes[self.theme_name]

    def set_status(self, text: str):
        self.status_lbl.configure(text=text)

    def disconnect(self):
        if not self.connected:
            return
        try:
            self._send_json({"type": "quit"})
        except Exception:
            pass
        try:
            if self.rf: self.rf.close()
            if self.wf: self.wf.close()
            if self.sock: self.sock.close()
        except Exception:
            pass
        self.connected = False
        self.set_status("Disconnected")
        self.append_system("Disconnected.")

    def on_close(self):
        self.disconnect()
        self.root.destroy()

def main():
    root = tk.Tk()
    app = ChatClientUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
