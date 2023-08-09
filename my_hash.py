import hashlib
def generate_hash(pan_number):
    #create a sha-256 hash object 
    sha256_hash=hashlib.sha256()
    #encode the PAN number as bytes (UTF-8) before hashing
    pan_number_bytes=pan_number.encode('utf-8')
    #update the hash object with the PAN number bytes 
    sha256_hash.update(pan_number_bytes)
    #get the hexadecimal representation of the hash 
    hashed_pan_number=sha256_hash.hexdigest()

    return hashed_pan_number
# example usage 
pan_number="ABCD1234567" #replace with the actual PAN number 
hashed_pan=generate_hash(pan_number)
print("PAN number :",pan_number)
print("SHA-256 hash:",hashed_pan)