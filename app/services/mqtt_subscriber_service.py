import paho.mqtt.client as mqtt
import base64
import requests
import os
import cv2
import numpy as np
import binascii
from dotenv import load_dotenv
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

# Load secret key
load_dotenv()
key = binascii.unhexlify(os.getenv("SECRET_KEY"))
class Subcriber_Service():

    # Decrypt and display image
    def decrypt_and_show(self, data):
        full_data = base64.b64decode(data)
        iv = full_data[:16]
        ciphertext = full_data[16:]

        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        padded_data = decryptor.update(ciphertext) + decryptor.finalize()

        unpadder = padding.PKCS7(128).unpadder()
        decoded_image = unpadder.update(padded_data) + unpadder.finalize()

        np_arr = np.frombuffer(base64.b64decode(decoded_image), np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        # cv2.imshow("Decrypted Image", img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        return img
        

    # Handle incoming MQTT message
    def on_message(self, client, userdata, msg):
        file_url = msg.payload.decode()
        print(f"Received file URL: {file_url}")
        response = requests.get(file_url)

        if response.status_code == 200:
            decrypted_image = self.decrypt_and_show(response.content)
            
            # DELETE image after viewing
            filename = file_url.split("/")[-1]
            delete_url = f"https://image-server-ytw4.onrender.com/files/{filename}"
            delete_res = requests.delete(delete_url)
            if delete_res.status_code == 200:
                print(f"Deleted {filename} from server.")
            else:
                print(f"Failed to delete {filename}: {delete_res.text}")
        else:
            print("Failed to fetch image from URL.")


    def run_subscriber(self):
        # MQTT setup
        client = mqtt.Client(client_id="subscriber", transport="websockets", protocol=mqtt.MQTTv311)
        client.tls_set()
        client.on_message = self.on_message

        client.connect("mqtt-broker-wk0v.onrender.com", 443, 60)
        client.subscribe("camera_1")
        print("Waiting for encrypted image URL...")
        client.loop_forever()