import base64
import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


def derive_key(password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,  # 32 bytes = 256 bits
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = kdf.derive(password.encode())
    return key

def encrypt(plaintext, password):
    # Use a fixed salt for key derivation
    salt = b"YourFixedSaltValue"
    key = derive_key(password, salt)

    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_plaintext = padder.update(plaintext.encode()) + padder.finalize()

    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()

    # Use the base64 URL-safe alphabet directly for concatenation
    return base64.urlsafe_b64encode(salt + b"||" + iv + b"||" + ciphertext)

def decrypt(ciphertext, password):
    data = base64.urlsafe_b64decode(ciphertext)
    salt, iv, ciphertext = data.split(b"||")
    key = derive_key(password, salt)

    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()

    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()

    return plaintext.decode()

# Example usage:
text = "Hello World! 你好，中国！"
password = "MySecretPassword"

encrypted_text = encrypt(text, password)
print("Encrypted:", encrypted_text)

decrypted_text = decrypt(encrypted_text, password)
print("Decrypted:", decrypted_text)




'''
import base64
import os
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

# Load the fixed AES key from a secure location (e.g., configuration file)
# Replace the following line with the actual process of loading the key.
# For the purpose of this example, we are using a hardcoded key.
fixed_key = b"\x90\x03...\x02\x99\x55\xee...\xAA"  # Replace with your actual 256-bit AES key

def encrypt_pan(pan_number):
    # Use a fixed salt for encryption
    salt = b"YourFixedSaltValue"

    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_pan = padder.update(pan_number.encode()) + padder.finalize()

    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(fixed_key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_pan) + encryptor.finalize()

    # Use the base64 URL-safe alphabet directly for concatenation
    return base64.urlsafe_b64encode(salt + b"||" + iv + b"||" + ciphertext)

def decrypt_pan(encrypted_pan):
    data = base64.urlsafe_b64decode(encrypted_pan)
    salt, iv, ciphertext = data.split(b"||")

    cipher = Cipher(algorithms.AES(fixed_key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_pan = decryptor.update(ciphertext) + decryptor.finalize()

    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    pan_number = unpadder.update(padded_pan) + unpadder.finalize()

    return pan_number.decode()

# Example usage:
pan_number = "1234-5678-9012-3456"

encrypted_pan = encrypt_pan(pan_number)
print("Encrypted PAN:", encrypted_pan)

decrypted_pan = decrypt_pan(encrypted_pan)
print("Decrypted PAN:", decrypted_pan)


# Example usage:
pan_number = "1234-5678-9012-3456"

encrypted_pan = encrypt_pan(pan_number)
print("Encrypted PAN:", encrypted_pan)

decrypted_pan = decrypt_pan(encrypted_pan)
print("Decrypted PAN:", decrypted_pan)


# Example usage:
pan_number = "1234-5678-9012-3456"

encrypted_pan = encrypt_pan(pan_number)
print("Encrypted PAN:", encrypted_pan)

decrypted_pan = decrypt_pan(encrypted_pan)
print("Decrypted PAN:", decrypted_pan)
'''