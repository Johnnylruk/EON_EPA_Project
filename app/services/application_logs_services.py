from app.data_classes.violation_logs_model import ViolationLogs, ViolationMessage
from datetime import datetime, timezone
import os
class ApplicationLogServices():

    def log_violation(self, objects_detected, people_detected):
        """
            @params: list, list

            @returns: Nothing

            @exception: Exception
                - logs exception message in application logs

            Logs 
            
        """
        if people_detected > 0 and objects_detected > 0:      
            severity = "poor"
            
        elif people_detected > 0 and objects_detected == 0:
            severity = "very poor"

        match(severity):
            case "poor": 
                description = "Person detected with incorrect PPE"
            
            case "very poor":
                description = "Person detected without PPE"

        violation_log_list = []
        for obj in objects_detected:
            violation_logs = ViolationLogs(
                violation=obj,
                date=str(datetime.now(tz=timezone.utc).date()),
                time=str(datetime.now(tz=timezone.utc).ctime()),
                description=description
            )
            violation_log_list.append(violation_logs)
        
        self.create_violation_log(violation_log_list)
        
    
    def log_exception():
        return ""
    
    def create_violation_log(self, violation_log_list):
        current_dir = os.getcwd()     
        folder_path = os.path.join(current_dir,"violation_logs")
        if os.path.exists(folder_path):
            for violation in violation_log_list:
                with open(f"{folder_path}/violations.txt", "a") as f:
                    f.write(f"{violation.violation}, {violation.date}, {violation.time}, {violation.description}\n")
        else:
            os.makedirs(folder_path, exist_ok=True)

    def get_violation_logs():
        current_dir = os.getcwd()     
        folder_path = os.path.join(current_dir,"violation_logs")

        if os.path.exists(folder_path):
           with open(f"{folder_path}/violations.txt", "r") as f:
            violations_result = []
            for line in f:
               violation_text = f.readline()
               violation_items = violation_text.split(",")
        
               violation_log = ViolationLogs(
                    violation=violation_items[0],
                    date=violation_items[1],
                    time=violation_items[2],
                    description=violation_items[3]
                )
               violations_result.append(violation_log)
            
            violation_message = ViolationMessage(
                violations=violations_result
            )
            return violation_message
        else:
            os.makedirs(folder_path, exist_ok=True)