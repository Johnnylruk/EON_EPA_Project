from fastapi import FastAPI
from app.services.roboflow_connection_services import RoboflowServices
from inference_sdk import InferenceHTTPClient
from app.services.roboflow_workflow_pipeline import WorkflowService
from app.services.roboflow_workflow_pipeline_rules import workflow_rules_dict
from app.services.camera_services import CameraServices
from app.services.message_services import MessageServices
from app.services.image_adjustment_service import ImageAdjustmentService
from app.services.application_logs_services import ApplicationLogServices
from app.data_classes.message_result_modal import MessageResult
from app.data_classes.violation_logs_model  import ViolationMessage

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
application_log_service = ApplicationLogServices()


##____________________ GET VIOLATION DATA _________________________##
   
@app.get("/get-violation-data")
async def get_violation_data() -> MessageResult: 
        """ 
            @accepts - No type
            @returns - MessageResult

            Gets image from reo link cloud and sends it to roboflow cloud storage
            to be processed by AI model
         """
         
        # -------- GET IMAGE FROM CAMERA -------------------------- #
        image_from_reo = await camera_services.get_reo_link_images_frames()

        #image = camera_services.take_image()
       
        # -------- BEGIN IMAGE BLURRING --------------------------- #
        blurred_imgs = []
        for img in image_from_reo:
            blurred_img = await image_adjustment.blur_face_images(img)
            blurred_imgs.append(blurred_img)
        
       
        # -------- SEND TO ROBOFLOW ------------------------------- #
        # send image to roboflow using image variable temporarily
        # will uses image_reo_link variable when camera connected
        result = await workflow.run_roboflow_workflow(
                roboflow_client, 
                workflow_rules_dict,
                roboflow_connection['connection_response'],
                roboflow_connection['workspace_name'],
                blurred_imgs[0]
            )
        
        # -------- CREATE MESSAGE TO SEND TO FRONT END ----------- #
        response_message = await message_services.create_message(result)

        return response_message


##____________________ GET VIOLATION LOGs _________________________##
   
@app.get("/get-violation-log")
async def get_violation_log() -> ViolationMessage: 
        """ 
            @accepts - No type
            @returns - ViolationLogs

            Gets image violation log model storage log information from
            application log services
         """
        # -------- GET LOGS FROM TXT FILE FOR VIOLATIONS----------- #
        violation_logs_message = await application_log_service.get_violation_logs()

        return violation_logs_message

