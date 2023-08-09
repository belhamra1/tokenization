import hashlib
import base64
import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import random





def read_counter_from_file(increment):
    try:
        with open(increment, 'r') as file:
            return int(file.read())
    except FileNotFoundError:
        # If the file does not exist, return 0 and create the file with initial value 0.
        write_counter_to_file(increment, 0)
        return 0

def write_counter_to_file(increment, counter):
    with open(increment, 'w') as file:
        file.write(str(counter))

# Example usage:
increment = 'incrementc.txt'
j = read_counter_from_file(increment)
print("Current value of i:", j)

# Increment j
j += 1

# Write the updated value of i back to the file
write_counter_to_file(increment, j)







class MinimalStandardGenerator:
    def __init__(self, seed=1):
        self.a = 16807
        self.m = 2**31 - 1
        self.seed = seed #le premier element cad x0

    def generate(self):
        self.seed = (self.a * self.seed) % self.m
        return self.seed



def read_seed_from_file(seed):
    try:
        with open(seed, 'r') as file:
            return int(file.read())
    except FileNotFoundError:
        # If the file does not exist, return 555 and create the file with the value 555.
        write_counter_to_file(increment, 555)
        return 555


def get_last_random_number(taille,j):

    seed='seed.txt'
    s=read_seed_from_file(seed)
    generator = MinimalStandardGenerator(seed=s)
    last_random_number = None
    
   
    for _ in range(j):
        random_number = generator.generate()
        
    last_random_number = random_number**3

    

    while(len(str(last_random_number)) <taille):
       last_random_number=int(last_random_number)
       last_random_number +=1000000000000000

    
    last_random_number=int(str(last_random_number)[:taille])
    print("Current value of i por la fonction random :", j)
  

    return last_random_number


########################################################################














# the hash 

import hashlib

def generate_hash(password):
    # Create a sha-256 hash object 
    sha256_hash = hashlib.sha256()

    # Encode the password as bytes (UTF-8) before hashing
    password_bytes = password.encode('utf-8')

    # Update the hash object with the password bytes 
    sha256_hash.update(password_bytes)

    # Get the hexadecimal representation of the hash 
    hashed_password = sha256_hash.hexdigest()

    return hashed_password


# for encryption 

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

    return pan_number.decode()'''

def generate_token(taille,j):
    
    random_number=get_last_random_number(taille,j)
    random_number_str = str(random_number)
    
   
    token = random_number_str.encode() 
    print("Current value of i por la fonction generate :", j)

    return token

# Example usage:
'''pan_number = "1234567890123456"
password = "MySecretPassword" 

token = generate_token(pan_number, password)
print("Token:", token) '''