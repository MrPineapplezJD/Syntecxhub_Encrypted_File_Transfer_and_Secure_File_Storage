
import socket
import os
from crypto import verify_hmac, generate_hmac
from config import SERVER_HOST, SERVER_PORT, CHUNK_SIZE

STORAGE_DIR = "storage"

# Ensure storage folder exists
os.makedirs(STORAGE_DIR, exist_ok=True)


# Receive file from client
def receive_file(conn):

    # Receive filename size (4 bytes)
    filename_size = int.from_bytes(conn.recv(4), 'big')

    # Receive filename 
    filename = conn.recv(filename_size).decode()

    print(f"[+] Receiving file: {filename}")

    # Receive file size (8 bytes)
    file_size = int.from_bytes(conn.recv(8), 'big')

    received_data = b''
    while len(received_data) < file_size:
        chunk = conn.recv(CHUNK_SIZE)
        if not chunk:
            break
        received_data += chunk

    # Split data and HMAC
    file_data = received_data[:-32]
    received_hmac = received_data[-32:]

    # Verify integrity
    if verify_hmac(file_data, received_hmac):
        print("[✔] HMAC verified")

        # Save encrypted file
        with open(os.path.join(STORAGE_DIR, filename), "wb") as f:
            f.write(file_data)
        print("[✔] File stored securely")
    
    else:
        print("[✘] HMAC verification failed!")


# Send file to client
def send_file(conn):

    # Receive filename size
    filename_size = int.from_bytes(conn.recv(4), 'big')

    # Receive filename
    filename = conn.recv(filename_size).decode()

    filepath = os.path.join(STORAGE_DIR, filename)

    if not os.path.exists(filepath):
        print("[✘] File not found on server")
        conn.send(b"ERROR")
        return

    conn.send(b"OK")
    print(f"[+] Sending file: {filename}")
    
    with open(filepath, "rb") as f:
        data = f.read()

    # Generate HMAC
    file_hmac = generate_hmac(data)

    payload = data + file_hmac

    # Send file size
    conn.send(len(payload).to_bytes(8, 'big'))

    # Send file
    conn.sendall(payload)

    print("[✔] File sent to client")



def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((SERVER_HOST, SERVER_PORT))
    server.listen(5)

    print(f"[+] Server listening on {SERVER_HOST}:{SERVER_PORT}")

    while True:
        conn, addr = server.accept()
        print(f"[+] Connection from {addr}")

        command = conn.recv(10).decode().strip()
        print(f"[DEBUG] Command received: '{command}'")
        if command == "UPLOAD":
            receive_file(conn)

        elif command == "DOWNLOAD":
            send_file(conn)

        else:
            print("[✘] Unknown command")
        
        conn.close()


if __name__ == "__main__":
    start_server()



