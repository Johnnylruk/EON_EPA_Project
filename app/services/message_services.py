from app.data_classes.message_result_modal import MessageResult, Predictions, Person
from app.services.roboflow_connection_services import RoboflowServices

roboflow_services = RoboflowServices()


class MessageServices():
    def create_message(self, result) -> MessageResult:
        try:
            predictions_list = result[0]["predictions"]["predictions"]
            if not predictions_list:
                return "No items in list"

            output_image = result[0]["output_image"]

            predictions = self.create_prediction_model(predictions_list)
            persons_detected = self.get_violation_from_predictions(predictions)

            result_model = MessageResult(persons_detected, output_image)
                        
            # ## encryption here
            
            return result_model

        except Exception as e:
            return e
    
    # try and use a mapping services
    def create_prediction_model(self, predictions_list: list) -> list:
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

    def get_violation_from_predictions(self, predictions: list) -> list[Person]:
        try:
            object_violations = self.map_classes_to_model(predictions)   
            return object_violations
              
        except Exception as e:
            return e
    
    def map_classes_to_model(self, predictions) -> list[Person]:
        
        object_predictions = [i for i in predictions if (
                            i.violation == "12" or  
                            i.violation == "15" or 
                            i.violation == "3" or 
                            i.violation == "8")]

        person_predictions = [i for i in predictions if i.violation == "person"]

        persons_detected = self.map_to_person_detected(object_predictions, person_predictions)


        return persons_detected

    def map_to_person_detected(self, object_violations: list, person_predictions: list) -> list[Person]:
        try:
            people_detected = []
            for person in person_predictions: 
                objects_detected = []
                for violation in object_violations:
                            
                            ## PERSON CLASS BOUNDING BOX CALC
                            (person_x_min, person_x_max, person_y_min, person_y_max, person_box_area) = self.person_class_bounding_box_calc(person)
                            
                            ## OBJECT CLASS AREA CALC
                            object_box_area = self.object_class_area_calc(violation)

                            is_x_within_bounds = violation.x >= person_x_min and violation.x <= person_x_max
                            is_y_within_bounds = violation.y >= person_y_min and violation.y <= person_y_max
                            is_object_area_valid = object_box_area <= person_box_area

                            if is_x_within_bounds and is_y_within_bounds and is_object_area_valid:
                                objects_detected.append(violation)
                               
                if len(objects_detected) > 0:
                    people = Person(
                        violations=objects_detected
                    )
                    people_detected.append(people)
                       

            return people_detected
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