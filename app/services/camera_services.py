import cv2
from PIL import Image
import numpy as np
from app.services.mqtt_subscriber_service import Subcriber_Service
from app.services.mqtt_publisher_service import Publisher_Service

publisher_service = Publisher_Service()

class CameraServices():
    def __init__(self):
        self.subscriber_service = Subcriber_Service()
        self.subscriber_service.run_subscriber()
    
    ##----------- BEGIN TESTING FUNCTIONS ---------------##

    def take_image(self):
        cam_port = 0
        cam = cv2.VideoCapture(cam_port)
        result, image = cam.read()
        if result:
            return image
        cam.release()
    
    def get_local_image(self):
        image_file = Image.open("app/images/test_image.jpg")
        image = np.array(image_file)
        return image
    
    def send_to_publisher(self):
        image = self.take_image()
        image_to_bytes = self.encode_image_base64(image)
        publisher_service.run_publisher(self, image_to_bytes)

    ##----------- END TESTING FUNCTIONS ---------------##
    def encode_image_base64(self, image):
        quality = 90
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), quality]
        ret, buffer = cv2.imencode('.jpg', image, encode_param)
        if ret:
            img_bytes = buffer.tobytes()
            return img_bytes
        else:
            no_image_taken = "no image file found"
            return no_image_taken