# 💬 UDP Terminal Messenger

A lightweight, console-based messenger built with Python using the UDP protocol. It allows real-time communication between a client and a server directly through the terminal.

---

## 🚀 Features

*   **Bidirectional Communication:** Full-duplex messaging (both sending and receiving).
*   **UDP Protocol:** Data transfer using port `5005`.
*   **Customizable Identity:** Change your display name on the fly within the app.
*   **Port Management:** Dedicated option to open/bind a port for incoming connections.
*   **Zero Dependencies:** Runs on vanilla Python using standard libraries (`socket`, `threading`).

> ## IMPORTANT!
> ### ⚠️ Connection Note (Carrier-Grade NAT / Private IP)
> If you have a **"Gray" (Private/CGNAT) IP address**, direct connection over the internet will not work. In this case, you must use **Radmin VPN**, Hamachi, or a similar tool to create a virtual local network with your friend before connecting.

## 📸 Preview

![App Screenshot](./screenshot.png)

## 🛠 Tech Stack

*   **Language:** Python 3.14 ~~3.11~~
*   **Networking:** `socket` library
*   **Concurrency:** `threading` (for simultaneous listen/send)

## 📦 Installation & Usage

1. **Clone the repository:**
   ```bash
   git clone https://github.com/qualzed/qChat
   cd qChat
   ```

2. **Run the application:**
   ```bash
   python main.py
   ```

## ⌨️ How it Works (Menu Options)

1. **Connect:** Enter the target IP address to start chatting.
2. **Change Name:** Set a custom nickname for the session.
3. **Send Message:** Type your text and hit Enter.
4. **Open Port:** Activate the listener on port `5005` to wait for incoming messages.
