# 🔐 Encrypted File Transfer & Secure File Storage (Python)

A secure client-server file transfer system built in Python that ensures confidentiality, integrity, and safe storage using AES encryption and HMAC verification.

---

## 🚀 Features

* 🔐 **AES-256 Encryption (CFB Mode)** for secure file transmission
* 🛡️ **HMAC Integrity Verification (SHA-256)** to detect tampering
* 🌐 **Client-Server Architecture** using Python sockets
* 📂 **Encrypted File Storage** on the server
* 🔽 **Secure File Download & Decryption**
* 🧩 **Manual Chunking** for efficient large file transfer

---

## 🧠 How It Works

### 🔼 Upload Process

1. Client reads the file
2. File is encrypted using AES
3. HMAC is generated for integrity
4. Encrypted file + HMAC is sent to server
5. Server verifies HMAC
6. File is stored **encrypted** on disk

---

### 🔽 Download Process

1. Client requests a file from server
2. Server sends encrypted file + HMAC
3. Client verifies integrity using HMAC
4. File is decrypted using AES
5. Clean file is saved locally

---

## 🛠️ Technologies Used

* **Python**
* **Socket Programming** (TCP)
* **cryptography library** (AES encryption)
* **hashlib & hmac** (integrity verification)
* **File handling (binary mode)**

---

## 📁 Project Structure

```
encrypted_file_transfer/
│
├── client.py          # Handles file upload & download
├── server.py          # Handles incoming connections & storage
├── crypto_utils.py    # Encryption, decryption, HMAC functions
├── config.py          # Configuration (keys, ports, chunk size)
├── storage/           # Encrypted files stored here (server)
└── downloads/         # Decrypted files saved here (client)
```

---

## ⚙️ Installation & Setup

### 1. Install dependencies

```
pip install cryptography
```

---

### 2. Start the server

```
python server.py
```

---

### 3. Run the client

```
python client.py
```

---

## ▶️ Usage

### Upload a file

```
1. Choose "Upload File"
2. Enter file name (must exist in project folder)
```

---

### Download a file

```
1. Choose "Download File"
2. Enter filename stored on server
```

---

## 🔐 Security Concepts Implemented

### 1. AES Encryption

* Ensures **confidentiality**
* Even if intercepted, data is unreadable

---

### 2. HMAC (Hash-Based Message Authentication Code)

* Ensures **integrity**
* Detects:

  * File tampering
  * Data corruption
  * Unauthorized modification

---

### 3. Encrypted Storage

* Files are stored in encrypted form on the server
* Prevents data exposure even if storage is compromised

---

## ⚠️ Threat Model & Mitigation

### 🧨 Man-in-the-Middle (MITM) Attack

**Threat:**
An attacker intercepts communication between client and server.

**Mitigation:**

* AES encryption prevents reading of intercepted data
* HMAC ensures tampered data is detected

---

### 🔑 Key Management

**Risk:**
Hardcoded keys can be exposed.

**Current Approach:**

* Static keys stored in `config.py` (for simplicity)

**Improvement:**

* Use environment variables
* Implement secure key exchange (e.g., Diffie-Hellman)

---

## ⚠️ Limitations

* No authentication system (any client can connect)
* Static encryption keys (not dynamically generated)
* No resume support for interrupted transfers
* Runs on local network (no TLS layer)

---

## 🚀 Future Improvements

* 🔐 Secure key exchange (Diffie-Hellman / RSA)
* 👤 User authentication system
* 🌍 TLS/SSL secure communication
* 📊 Transfer progress indicator
* 💾 Resume interrupted downloads

---

## 📌 Learning Outcomes

This project demonstrates:

* Secure file handling techniques
* Cryptography fundamentals (AES, HMAC)
* Network programming using sockets
* Designing a custom communication protocol
* Understanding real-world security threats

---

## 📬 Submission

This project was developed as part of the **Syntecxhub Cyber Security Internship Program**.

---

## 👨‍💻 Author

Emmanuel Joshua Deoduth

---
