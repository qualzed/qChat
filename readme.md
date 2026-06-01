<p align="center">
  <img src="icon.ico" width="128" alt="qChat Logo">
</p>

<h1 align="center">
  <samp>qChat</samp>
</h1>

<p align="center">
  <b>A lightweight, console-based UDP messenger built entirely from scratch in Python using standard sockets.</b><br>
  <i>Features secure real-time messaging, local system echo suppression, and seamless file transfers.</i>
</p>

<p align="center">
  <a href="https://python.org" target="_blank">
    <img src="https://img.shields.io/badge/Python-3.14-yellow?style=plastic" alt="Python Version">
  </a>
  <a href="https://radmin-vpn.com" target="_blank">
    <img src="https://img.shields.io/badge/RadminVPN-Network%20Tool-blue?style=plastic" alt="Radmin VPN">
  </a>
</p>

---

## 📸 Preview
<p align="center">
  <img src="screenshot.png" alt="Main Menu" width="100%">
</p>

---

## ✨ Features

* **UDP Transport Layer** — Uses standard UDP sockets for low-latency packet transmission.
* **Hybrid Session Encryption** — Secure messaging architecture protecting data in transit (details below).
* **Multi-Client Room Setup** — The server acts as a central room hosting simultaneous client connections.
* **Bi-directional File Transfer** — Send binary assets securely (Client ➔ Server / Server ➔ Client).
* **Command-Driven Control** — System directives parsed via the `$` prefix with local input cleanup.
* **Dynamic Nicknames** — Change your identity on the fly during an active chat session.
* **Modular Codebase** — Clean, decoupled project architecture containing 10+ focused modules.

---

## 🔐 Cryptography Architecture

The session is hardened against local eavesdropping, public Wi-Fi sniffing, and LAN-based network attacks. The cryptographic handshake follows a 2-stage lifecycle:

1. **Secure Handshake Bridge (ECDH):** Upon connecting, the client and server exchange temporary public keys using the **Elliptic Curve Diffie-Hellman (ECDH)** protocol over the `secp256r1` curve. A shared secret is computed and fed into a Key Derivation Function (**HKDF-SHA256**) to spin up a brief, authenticated session cipher.
2. **Room Key Distribution (Fernet / AES-128):** The server initializes a standalone, persistent master room key. This key is encrypted via the temporary ECDH bridge and dispatched to the client. Once received, all future messages and files are symmetrically encrypted using **Fernet** ciphers (AES in CBC mode coupled with HMAC-SHA256 authentication tags).

Brute-forcing the resulting payload over the network is mathematically impossible.

---

## 🛠️ Command System

Messages prefixed with `$` bypass standard broadcasts and are handled as local infrastructure routines.

* `$sendfile` — Initiates the automated binary file transmission sequence.
* `$exit` — Safely tears down connection states and terminates the application cleanly.

---

## 📁 Repository Structure

```bash
.
├── main.py                      # Application entry point (launches the main menu)
├── requirements.txt             # Project dependencies (cryptography, nuitka)
├── icon.png                     # Application logo
├── screen.png                   # Interface screenshot
└── src/
    ├── console.py               # Console utility wrappers (e.g., screen clearing)
    ├── header.py                # Global imports aggregator
    ├── menu.py                  # Main menu interface and navigation
    ├── packet.py                # Packet size configurations and headers
    ├── port.py                  # Port scanner and manager (defaults to 5005)
    ├── user.py                  # Nickname manager and connection state definitions
    ├── tag.py                   # Tag templates
    ├── settings.py              # Settings configurations
    ├── serializer.py            # JSON Reader, Initializer, and UI macros
    ├── crypto/
    │   ├── crypto_main.py       # Core cryptographic primitives (Enc/Dec logic)
    │   └── key_generation.py    # Ephemeral key registers and runtime ciphers
    ├── file/
    │   └── sendFile.py          # Binary file encoding and transmission logic
    ├── host/
    │   ├── client.py            # Core client engine (manages local session & custom clock)
    │   ├── message.py           # Message processing, formatting, and packet relaying
    │   ├── server.py            # Core server engine (tracks clients, IPs, and master ciphers)
    │   └── var.py               # System flags and request markers (e.g., \$filerequest)
    └── ui/
        └── interface.py         # UI terminal rendering engine
```

---

## 🚀 Getting Started

### Prerequisites
* Python 3.14+ runtime environment installed.

### Execution

1. **Clone the repository:**
   ```bash
   git clone https://github.com/qualzed/qChat
   cd qChat
   ```

2. **Run the application:**
   ```bash
   python main.py
   ```

---

## 🔨 Building the Project

Follow the instructions below to compile the project into a standalone executable for your target operating system.

### Quick Build

1. **Install the verified compiler version:**
   ```bash
   pip install nuitka==4.1.2
   ```

2. **Run the build automation script for your OS:**
   * **Windows:** Run `build.bat`
   * **Linux / macOS:** Run `build.sh`

*Note: This project is explicitly verified for deployment using **Nuitka** and **PyInstaller**. Utilizing experimental Python freezers may trigger compilation exceptions inside the `cryptography` native binaries.*