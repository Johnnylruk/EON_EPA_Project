import requests
from dotenv import load_dotenv 
import os
import logging

logging.basicConfig(level=logging.DEBUG)
load_dotenv()
LOCAL_HOST = os.getenv("local_host")
TEST_ENV = os.getenv("test_env")


class PPE_AI_Services():
    def __init__(self):
        self.url = f"{LOCAL_HOST}/predict"

    async def ai_processing(self, encrypted_image):  
        try:   
            ai_response = requests.post(self.url, json=encrypted_image)
            return ai_response
        except Exception as e:
            return f"Error: {ai_response.status_code}\n Content: {ai_response.content}\n Exception: {e}"
            
    def generate_response(self, ai_response):
        try:
            if ai_response.ok:
                prediction_data = ai_response.json()
                return prediction_data
            else:
                 print("no prediction returned")
          
        except Exception as e:
            return f"{e} and {ai_response.status_code} {ai_response.reason}"
        
    

    # def draw_image(self, prediction_data, image):
    #     p_dict = dict(prediction_data)
    #     print("dict" ,p_dict.values())
    #     predictions = []
    #     for detections in  p_dict.values():
    #         prediction_items =[]
    #         for prediction in detections:
    #             x1_y1 = tuple(prediction[:2])
    #             x2_y2 = tuple(prediction[:4])
    #             cv2.rectangle(image, x1_y1, x2_y2,color=,thickness=2)
    #             cv2.imwrite('vinny',image)
# colors = {
#     0.0: "red", 
#     1.0:"green", 
#     2.0: "purple"}
#
#

    
