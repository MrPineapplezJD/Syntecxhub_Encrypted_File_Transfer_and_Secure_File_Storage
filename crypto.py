
import os
import hmac
import hashlib

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from config import AES_KEY, HMAC_KEY


# =========================
# AES ENCRYPTION
# =========================
def encrypt_data(data):

    iv = os.urandom(16)         # 16-byte IV

    cipher = Cipher(algorithms.AES(AES_KEY), modes.CFB(iv))
    encryptor = cipher.encryptor()

    encrypted = encryptor.update(data) + encryptor.finalize()

    return iv + encrypted       # prepend IV



# =========================
# AES DECRYPTION
# =========================
def decrypt_data(data):

    iv = data[:16]
    encrypted = data[16:]

    cipher = Cipher(algorithms.AES(AES_KEY), modes.CFB(iv))
    decryptor = cipher.decryptor()

    return decryptor.update(encrypted) + decryptor.finalize()



# =========================
# HMAC GENERATION
# =========================
def generate_hmac(data):

    return hmac.new(HMAC_KEY, data, hashlib.sha256).digest()



# =========================
# HMAC VERIFICATION
# =========================
def verify_hmac(data, received_hmac):

    calculated = generate_hmac(data)
    return hmac.compare_digest(calculated, received_hmac)


