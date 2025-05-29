from app.data_classes.message_result_modal import MessageResult, Predictions, Helmet, HiVis, Object_Violations, Person
from app.services.roboflow_connection_services import RoboflowServices
import numpy as np

roboflow_services = RoboflowServices()


class MessageServices():
    def create_message(self, result):
        try:
            predictions_list = result[0]["predictions"]["predictions"]
            if not predictions_list:
                return "No items in list"

            output_image = result[0]["output_image"]

            predictions = self.create_prediction_model(predictions_list)
            person_detected = self.get_violation_from_predictions(predictions)

            result_model = MessageResult(person_detected, output_image)
                        
            # ## encryption here
            
            return result_model

        except Exception as e:
            return e
    
    # try and use a mapping services
    def create_prediction_model(self, predictions_list) -> list:
        try:
            predictions = list()
            for item in predictions_list:

                confidence = item["confidence"]
                violation = item["class"]
                violation_id = item["class_id"]
                detection_id = item["detection_id"]
                
                prediction_model = Predictions(
                    confidence,
                    violation,
                    violation_id,
                    detection_id,
                )
                
                predictions.append(prediction_model)
            return predictions
        except Exception as e:
            return e

    def get_violation_from_predictions(self, predictions) -> Object_Violations:
        try:
            violations = {
                "5": Person,
                "12": Helmet,
                "15": HiVis
            }
            object_violations = self.map_classes_to_model(predictions, violations)   
            return object_violations
              
        except Exception as e:
            return e
    
    def map_classes_to_model(self, predictions, violations):
        
        for item in violations:
            match item.value:
                case Helmet():
                    helmet_predictions = [i for i in predictions if i.violation == item.key]

                case HiVis():
                    hi_vis_predictions = [i for i in predictions if i.violation == item.key]
                
                case Person():
                    person_predictions = [i for i in predictions if i.violation == item.key]

        object_violations = Object_Violations(
            helmet_violation=helmet_predictions,
            hi_vis_violation=hi_vis_predictions
        )
        
        person_detected = self.map_to_person_detected(object_violations, person_predictions)
        return person_detected

    def map_to_person_detected(self, object_violations, person_predictions) -> Person:
        try:
            for person in person_predictions:
                person_detected = Person(
                    violations=object_violations
                )
            return person_detected
        except Exception as e:
            return e
        