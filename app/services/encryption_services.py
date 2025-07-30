import hashlib
#import gnupg
import os
import cv2
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import binascii
import numpy as np
from dotenv import load_dotenv 


load_dotenv()
key = binascii.unhexlify(os.getenv("SECRET_KEY"))

class EncryptionService():
    
    # def encrypt(self):
    #     gpg = gnupg.GPG()
    #     input_data = gpg.gen_key_input(
            

    #     )

    #     gpg.encrypt()
    #     return

    # def decrypt(self):
    #     gpg = gnupg.GPG()
    #     input_data = gpg.gen_key_input(
            

    #     )

    #     gpg.decrypt()
    #     return
    

    def decrypt_and_show(self, data):
        try:
            base64_bytes = data.encode("latin-1")
            full_data = base64.b64decode(base64_bytes)
            iv = full_data[:16]
            ciphertext = full_data[16:]

            cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
            decryptor = cipher.decryptor()
            padded_data = decryptor.update(ciphertext) + decryptor.finalize()

            unpadder = padding.PKCS7(128).unpadder()
            decoded_image = unpadder.update(padded_data) + unpadder.finalize()

            np_arr = np.frombuffer(decoded_image, dtype=np.uint8)

            img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
            cv2.imwrite('image.png', img)
            
            return img
        except Exception as e:
            return e

    def create_tls_connection():
        return ""