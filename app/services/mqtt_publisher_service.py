import paho.mqtt.client as mqtt
import base64
import os
import secrets
import requests
import binascii
from dotenv import load_dotenv
from uuid import uuid4
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import time
# Load secret key
load_dotenv()
key = binascii.unhexlify(os.getenv("SECRET_KEY"))

class Publisher_Service():
    
    def image_padding(self, image_to_bytes):
        # Pad
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(image_to_bytes) + padder.finalize()
        return padded_data

    def image_encryption(self, image_to_bytes):
        # Encrypt
        iv = secrets.token_bytes(16)
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        padded_data = self.image_padding(image_to_bytes)
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()
        final_payload = base64.b64encode(iv + ciphertext)
        return final_payload

    def save_encrypted_file(self,image_to_bytes):
        # Save encrypted file temporarily
        filename = f"{uuid4().hex}.bin"
        final_payload = self.image_encryption(image_to_bytes)
        with open(filename, "wb") as f:
            f.write(final_payload)
        return filename

    # Upload to FastAPI
    def connect_to_image_server(self, image_to_bytes):
        filename = self.save_encrypted_file(image_to_bytes)
        upload_url = "https://image-server-ytw4.onrender.com/upload"
        with open(filename, "rb") as f:
            res = requests.post(upload_url, files={"file": (filename, f)})
            if res.status_code != 200:
                raise Exception(f"Upload failed: {res.text}")
            file_url = res.json()["url"]
        # Clean up
        os.remove(filename)
        return file_url

    def run_publisher(self, image_to_bytes):
       file_url = self.connect_to_image_server(image_to_bytes)
       # Send file URL via MQTT
       client = mqtt.Client(client_id="publisher", transport="websockets", protocol=mqtt.MQTTv311)
       client.tls_set()
       client.connect("mqtt-broker-wk0v.onrender.com", 443, 60)
       client.loop_start()
       client.publish("camera_1", file_url)
       print(f"Published encrypted image URL: {file_url}")
       time.sleep(1)
       client.loop_stop()
       client.disconnect()