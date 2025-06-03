from fastapi import FastAPI
from app.services.roboflow_connection_services import RoboflowServices
from inference_sdk import InferenceHTTPClient
from app.services.roboflow_workflow_pipeline import WorkflowService
from app.services.roboflow_workflow_pipeline_rules import workflow_rules_dict
from app.services.camera_services import CameraServices
from app.services.message_services import MessageServices
from app.services.image_adjustment_service  import ImageAdjustmentService
from app.services.application_logs_services import ApplicationLogServices

app = FastAPI()

roboflow_services = RoboflowServices()
workflow = WorkflowService()
camera_services = CameraServices()
roboflow_connection = roboflow_services.roboflow_connection_utility()
roboflow_client = InferenceHTTPClient(
      
        api_url='https://detect.roboflow.com', 
        api_key=roboflow_connection['api_token']
    )
message_services = MessageServices()
image_adjustment = ImageAdjustmentService()
application_service = ApplicationLogServices()


##____________________ GET VIOLATION DATA _________________________##
   
@app.post("/get-violation-data")
def get_violation_data() -> str: 
        """ 
            @accepts - string base64
            @returns - string json

            Gets image from reo link cloud and sends it to roboflow cloud storage
            to be processed by AI model
         """
         
        # -------- GET IMAGE FROM CAMERA -------------------------- #
        # TEMPORARY DELETE WHEN REO LINK CONNECTED  
        image_from_local = camera_services.get_local_image()
        #image = camera_services.take_image()
       
        # -------- BEGIN IMAGE BLURRING --------------------------- #
        image = image_adjustment.blur_face_images(image_from_local)
        
        
        # -------- DEPLOY MOST RECENT MODEL TO ROBOFLOW ----------- #
        #check_model_update()
        #application_service.log_exceptions()
       
        # -------- SEND TO ROBOFLOW ------------------------------- #
        # send image to roboflow using image variable temporarily
        # will uses image_reo_link variable when camera connected
        result = workflow.run_roboflow_workflow(
                roboflow_client, 
                workflow_rules_dict,
                roboflow_connection['connection_response'],
                roboflow_connection['workspace_name'],
                image
            )
        
        # -------- CREATE MESSAGE TO SEND TO FRONT END ----------- #
        response_message = message_services.create_message(result)

        return response_message

######### READ ME ##########
## This is called for testing the front end will call this as an endpoint
# get_violation_data()


##____________________ UPDATE AI MODEL _________________________##

# def check_model_update():
#     """
#         @params: None
#         @returns: None
#         @exception: Exception

#         Checks if local model file has been updated and then sends a new 
#         model to be used in roboflow workflow
#     """
#     roboflow_services.deploy_roboflow_model()

# check_model_update()
