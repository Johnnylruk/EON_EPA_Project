import base64
import cv2
from PIL import Image
import numpy as np
from data_retriever import retrieve_footage
from image_extraction import extract_key_frames
class CameraServices():


    ##----------- BEGIN TESTING FUNCTIONS ---------------##

    #### READ THIS FIRST #####
    # these funcitons can be removed or altered just make sure to use
    #  encode_image_base64 to turn the images into base64 strings
    # otherwise sending to roboflow will not work

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

    ##----------- END TESTING FUNCTIONS ---------------##

    ##----------- BEGIN CAMERA CONNECTION FUNCTIONS ---------##


    # Get video footage from reolink
    filename = retrieve_footage()
    print("Downloaded file:", filename)

    # Extract the iamge frames from the footage
    video_path = f"footage/{filename}"
    frames = extract_key_frames(video_path)
    print("Extracted frames:", frames)


    ##----------- END CAMERA CONNECTION FUNCTIONS -----------##


    ##----------- BEGIN IMAGE BASE64 ENCODING FUNCTION --------------##
    
    def encode_image_base64(self, image):
        quality = 90
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), quality]
        ret, buffer = cv2.imencode('.jpg', image, encode_param)
        if ret:
            img_base64 = base64.b64encode(buffer).decode('latin-1')
            return img_base64
        else:
            no_image_taken = "no image file found"
            return no_image_taken

    ##----------- END IMAGE BASE64 ENCODING FUNCTION --------------##

    ##----------- BEGIN IMAGE DECRYPT FUNCTION --------------##

    def decode_image_base64(img_string):
        img_bytes = base64.b64decode(img_string)
        arr = np.frombuffer(img_bytes, dtype=np.uint8)
        decoded_img = cv2.imdecode(arr, cv2.IMREAD_COLOR) 
        return decoded_img

    ##----------- END IMAGE DECRYPT FUNCTION --------------##




