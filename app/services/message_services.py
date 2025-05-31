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
                width = item["width"]
                height = item["height"]
                x = item["x"]
                y = item["y"]
                
                prediction_model = Predictions(
                    confidence,
                    violation,
                    violation_id,
                    detection_id,
                    width,
                    height,
                    x,
                    y
                )
                
                predictions.append(prediction_model)
            return predictions
        except Exception as e:
            return e

    def get_violation_from_predictions(self, predictions) -> Object_Violations:
        try:
            object_violations = self.map_classes_to_model(predictions)   
            return object_violations
              
        except Exception as e:
            return e
    
    def map_classes_to_model(self, predictions):
        
        helmet_predictions = [i for i in predictions if i.violation == "12"]

        hi_vis_predictions = [i for i in predictions if i.violation == "15"]
        
        person_predictions = [i for i in predictions if i.violation == "5"]

        object_violations = Object_Violations(
            helmet_violation=helmet_predictions,
            hi_vis_violation=hi_vis_predictions
        )
        
        person_detected = self.map_to_person_detected(object_violations, person_predictions)
        return person_detected

    def map_to_person_detected(self, object_violations, person_predictions) -> Person:
        try:
            for object in object_violations.helmet_violation:
                for person in person_predictions:  

                    ## PERSON CLASS BOUNDING BOX CALC
                    (person_x_min, person_x_max, person_y_min, person_y_max, person_box_area) = self.person_class_bounding_box_calc(person)
                     
                    ## OBJECT CLASS AREA CALC
                    object_box_area = self.object_class_area_calc(object)

                    if object.x >= person_x_min and object.x <= person_x_max and object.y >= person_y_min and object.y <= person_y_max and object_box_area <= person_box_area:   
                        person_detected = Person(
                            violations=object_violations
                        )
            return person_detected
        except Exception as e:
            return e


    def person_class_bounding_box_calc(self, person):
        person_box_width = person.width
        person_box_height = person.height
        person_x = person.x
        person_y = person.y

        person_width = person_box_width / 2
        person_x_min = person_x - person_width
        person_x_max = person_x + person_width

        person_height = person_box_height / 2
        person_y_min = person_y - person_height
        person_y_max = person_y + person_height

        person_box_area = person_box_height * person_box_width

        return (person_x_min, person_x_max, person_y_min, person_y_max, person_box_area)


    def object_class_area_calc(self, object):
        object_width = object.width
        object_height = object.height

        object_box_area = object_height * object_width
        return object_box_area