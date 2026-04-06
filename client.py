
import socket
import os
from crypto import encrypt_data, generate_hmac, verify_hmac, decrypt_data
from config import SERVER_HOST, SERVER_PORT


# Client sends encrypted file to server
def send_file(filepath):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER_HOST, SERVER_PORT))

    client.send(b"UPLOAD    ")
    
    filename = os.path.basename(filepath)

    # Read file
    with open(filepath, "rb") as f:
        data = f.read()

    print("[+] Encrypting file...")
    encrypted_data = encrypt_data(data)

    print("[+] Generating HMAC...")
    file_hmac = generate_hmac(encrypted_data)

    payload = encrypted_data + file_hmac

    # Send filename size
    client.send(len(filename).to_bytes(4, 'big'))

    # Send filename
    client.send(filename.encode())

    # Send file size
    client.send(len(payload).to_bytes(8, 'big'))

    # Send file data
    for i in range(0, len(payload), 4096):
        chunk = payload[i:i+4096]
        client.send(chunk)

    print("[✔] File sent successfully")
    client.close()



def download_file(filename):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER_HOST, SERVER_PORT))

    # Send command
    client.send(b"DOWNLOAD  ")

    # Send filename
    client.send(len(filename).to_bytes(4, 'big'))
    client.send(filename.encode())

    # Check server response
    status = client.recv(5)

    if status != b"OK":
        print("[✘] File not found on server")
        return

    print("[+] Receiving file...")
    # Receive file size
    file_size = int.from_bytes(client.recv(8), 'big')

    received_data = b''
    while len(received_data) < file_size:
        chunk = client.recv(4096)
        if not chunk:
            break
        received_data += chunk

    # Split data and HMAC
    file_data = received_data[:-32]
    received_hmac = received_data[-32:]

    # Verify integrity
    if not verify_hmac(file_data, received_hmac):
        print("[✘] File integrity check failed!")
        return

    print("[✔] HMAC verified")

    # Decrypt file
    decrypted = decrypt_data(file_data)

    # Save to downloads folder
    downloads_dir = "downloads"
    os.makedirs(downloads_dir, exist_ok=True)

    save_path = os.path.join(downloads_dir, filename)

    with open(save_path, "wb") as f:
        f.write(decrypted)
    print(f"[✔] File downloaded and decrypted: {save_path}")

    client.close()


# Main menu
if __name__ == "__main__":
    print("1. Upload File")
    print("2. Download File")

    choice = input("Choose option: ")
    if choice == "1":
        file_name = input("Enter file name: ")

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(BASE_DIR, file_name)

        if not os.path.exists(file_path):
            print("[✘] File not found")
            exit()
        send_file(file_path)

    elif choice == "2":
        filename = input("Enter filename to download: ")
        download_file(filename)

    else:
        print("Invalid choice")



