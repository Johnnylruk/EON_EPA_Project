from data_classes.violation_logs_model import ViolationLogs
from datetime import datetime, timezone
class ApplicationLogServices():

    def log_exceptions(self, objects_detected, people_detected):
        """
            @params: None

            @returns: None

            @exception: Exception
                - logs exception message in application logs

        
            Logs exception in applications_logs.txt
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
            
        return violation_log_list