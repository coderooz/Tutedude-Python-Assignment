# TkSocketChat

A clean, beginner-friendly **Python socket chat application** with a pleasant **Tkinter UI**.  
Built for *Module 22: Network Programming in Python Using Socket — Building a Chat Application* (Assignment 17).

> This repo contains a multi-client TCP server (`server.py`) and a desktop client (`client.py`) with a polished, easy-to-use interface.

---

## ✨ Features

- **Multi-client** chat server using standard library only (no external deps).
- **Attractive Tkinter UI** with Light/Dark themes.
- **User list panel** that updates in real time.
- **Timestamps**, Enter to send / Shift+Enter for newline.
- Robust JSON-Lines message protocol and graceful disconnects.
- Simple, readable code structure ideal for learning and demos.

---

## 🧰 Project Structure

```
TkSocketChat/
├── server.py      # Threaded socket server (console)
├── client.py      # Tkinter desktop client
└── README.md
```

---

## 🔧 Requirements

- Python **3.9+** (tested with 3.10/3.11/3.12)
- No third‑party libraries required.

---

## 📦 Installation

1. **Download** this folder or clone/copy it to your machine.
2. Verify Python:
   ```bash
   python --version
   # or
   python3 --version
   ```

> On Windows you might need to use `py` instead of `python`.

---

## ▶️ Running the App

### 1) Start the Server
Open a terminal in the `TkSocketChat` folder and run:
```bash
python server.py --host 0.0.0.0 --port 5050
```
You should see:
```
[YYYY-MM-DDTHH:MM:SSZ] Server listening on 0.0.0.0:5050
```

### 2) Start Clients (on same or different machines)
Run this on each client machine:
```bash
python client.py
```
- Click **Connect** and enter the server’s **host** (IP) and **port** (5050 by default), and your **username**.
- Start chatting! ✨

> If client and server are on the same computer, you can use `127.0.0.1` as the host.

---

## 🧪 Demo Checklist (for screen recording)

- Show the server running and listening.
- Open **two or more** client windows.
- Connect with different usernames.
- Send messages both ways and watch the **Online Users** list update.
- Disconnect one client and verify the **“left the chat”** system message.

This matches the typical demo flow for Module 22’s chat application. ✅

---

## 🧱 Message Protocol

All data is sent as **JSON** per line (newline-delimited).

### Client → Server
- `{"type":"join","username":"Alice"}` — identify yourself after connecting.
- `{"type":"chat","text":"Hello everyone!"}` — send a chat message.
- `{"type":"quit"}` — (optional) disconnect gracefully.
- `{"type":"ping"}` — (optional) keepalive.

### Server → Clients
- `{"type":"system","text":"🟢 Alice joined the chat.","ts":"...Z"}`
- `{"type":"chat","from":"Alice","text":"Hello!","ts":"...Z"}`
- `{"type":"userlist","users":["Alice","Bob"],"ts":"...Z"}`

---

## 🎨 UI Notes

- Clean layout with **chat area**, **message box**, **Send** button, and **Online Users** panel.
- **Light/Dark** theme toggle (top-right **Theme** button).
- Status bar shows connection info.
- **Enter** to send, **Shift+Enter** for a new line.

---

## 🧯 Troubleshooting

- **Firewall**: Allow inbound connections on the server port (default **5050**).
- **Wrong host/port**: Make sure clients use the correct server IP and port.
- If the client shows *“Failed to connect”*, verify the server is running and accessible on the network.

---

## 📄 License

MIT — do whatever you like; attribution appreciated.

---

## 🙌 Credits

Built with love for the assignment: **Module 22 — Socket Chat App**. Good luck! 🚀
