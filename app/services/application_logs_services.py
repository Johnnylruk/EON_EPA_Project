from app.data_classes.violation_logs_model import ViolationLogs, ViolationMessage
from datetime import datetime, timezone
import os
import math
class ApplicationLogServices():

    async def log_violation(self, people_detected):
        """
            @params: list, list

            @returns: Nothing

            @exception: Exception
                - logs exception message in application logs

            Logs 
            
        """
        # find different violation levels

        # whether helmet is on head or not class as no helmet
        # whether person is wearing ppe
        # map classes to names
        # write message to data base

        # put this for loop in a servicesto connect to repo
        violation_log_list = []
        for obj in objects_detected:
            violation_logs = ViolationLogs(
                violation=obj.violation,
                confidence=str(round(obj.confidence, 2)),
                date=str(datetime.now(tz=timezone.utc).date()),
                time=str(datetime.now(tz=timezone.utc).ctime()),
                description=description
            )
            violation_log_list.append(violation_logs)
        
        await self.create_violation_log(violation_log_list)
          
    
    async def create_violation_log(self, violation_log_list):
        current_dir = os.getcwd()     
        folder_path = os.path.join(current_dir,"violation_logs")
        if os.path.exists(folder_path):
            for violation in violation_log_list:
                with open(f"{folder_path}/violations.txt", "a") as f:
                    f.write(f"{violation.violation}, {violation.confidence}, {violation.date}, {violation.time}, {violation.description}\n")
        else:
            os.makedirs(folder_path, exist_ok=True)

    # replaced with render database call
    async def get_violation_logs(self, startDate, endDate):
        current_dir = os.getcwd()     
        folder_path = os.path.join(current_dir,"violation_logs")

        if os.path.exists(folder_path):
           with open(f"{folder_path}/violations.txt", "r") as f:
            violations_result = []
            for line in f:
               violation_items = [item.strip() for item in line.split(",")]
               if violation_items[2] >= startDate and violation_items[2] <= endDate:
                violation_log = ViolationLogs(
                        violation=violation_items[0],
                        confidence=violation_items[1],
                        date=violation_items[2],
                        time=violation_items[3],
                        description=violation_items[4]
                    )
                violations_result.append(violation_log)
            
            violation_message = ViolationMessage(
                violations=violations_result
            )
            return violation_message
        else:
            os.makedirs(folder_path, exist_ok=True)

    
        