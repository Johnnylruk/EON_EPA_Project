from fastapi import FastAPI, HTTPException, Query
from typing import Optional
from inference_sdk import InferenceHTTPClient
from app.services.message_services import MessageServices
from app.services.image_adjustment_service import ImageAdjustmentService
from app.services.application_logs_services import ApplicationLogServices
from app.data_classes.message_result_modal import MessageResult
from app.data_classes.violation_logs_model  import ViolationMessage
from app.services.camera_services import CameraServices

app = FastAPI()
message_services = MessageServices()
image_adjustment = ImageAdjustmentService()
application_log_service = ApplicationLogServices()
camera_services = CameraServices()

@app.get("/camera-api-connection")
async def get_image_from_camera():
        """
            camera api connection sends image upon motion detection
        """
        camera_services.send_to_publisher()


##____________________ GET VIOLATION DATA _________________________##
   
@app.get("/get-violation-data")
async def get_violation_data() -> MessageResult: 
        """ 
            @accepts - No type
            @returns - MessageResult
            Gets violation amounts from render database
         """
    
        # needs to get logs from render
        
        return ""

 
##____________________ GET VIOLATION LOGs _________________________##
   
@app.get("/get-violation-log")
async def get_violation_log(startDate: Optional[str] = Query(None), endDate: Optional[str] = Query(None)) -> ViolationMessage: 
        """ 
            @accepts - No type
            @returns - ViolationLogs

            Gets image violation log model storage log information from
            application log services
         """
        # -------- GET LOGS FROM TXT FILE FOR VIOLATIONS----------- #
        violation_logs_message = await application_log_service.get_violation_logs(startDate, endDate)

        return violation_logs_message

