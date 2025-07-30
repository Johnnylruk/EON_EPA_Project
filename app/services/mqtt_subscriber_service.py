import paho.mqtt.client as mqtt
import requests
import os
import asyncio
import aiomqtt
import binascii
from dotenv import load_dotenv
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
from app.services.ppe_ai_services import PPE_AI_Services
from app.services.message_services import MessageServices


# Load secret key
load_dotenv()
key = binascii.unhexlify(os.getenv("SECRET_KEY"))
ai__services = PPE_AI_Services()
message_services = MessageServices()

class Subcriber_Service():
        

    # Handle incoming MQTT message
    async def on_message(self, client, userdata, msg):
        file_url = msg.payload.decode()
        print(f"Received file URL: {file_url}")
        response = requests.get(file_url)

        if response.status_code == 200:
            print("Image recieved")
            encrypted_base64_img = response.content
            base64_string = encrypted_base64_img.decode("latin-1")
            ai_response = await ai__services.ai_processing(base64_string)
            prediction_data = ai__services.generate_response(ai_response)
            valid_predictions = message_services.get_valid_predictions(prediction_data)

            # save to render database

            # CONNECT TO MESSAGE SERVICE
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


    async def run_subscriber(self):
        async with aiomqtt.Client(
            hostname="mqtt-broker-wk0v.onrender.com",
            port=443,
            transport="websockets",
            tls_params=aiomqtt.TLSParameters()
        ) as client:
            await client.subscribe("camera_1")
            print("Subscriber connected and waiting for messages...")
            # THIS loop is the aiomqtt equivalent of paho's loop_start()
            async for message in client.messages:
                await self.on_message(message)