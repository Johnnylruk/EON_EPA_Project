from app.data_classes.message_result_modal import MessageResult, Prediction, Person
from app.services.application_logs_services import ApplicationLogServices

application_log_services = ApplicationLogServices()

class MessageServices():

    def get_valid_predictions(self, prediction_data):
        predictions = self.create_prediction_model(prediction_data)
        valid_predictions = self.map_classes_to_model(predictions)

        message_result = MessageResult(
            person_detected=valid_predictions
        )
        return message_result

    def create_prediction_model(self, prediction_data):
        try:
            p_dict = dict(prediction_data)
            print("dict" ,p_dict.values())
            predictions = []
            for detections in  p_dict.values():
                prediction_items =[]
                for prediction in detections:
                    x1 = prediction[0]
                    y1 = prediction[1]
                    x2 = prediction[2]
                    y2 = prediction[3]
                    confidence = prediction[4]
                    violation = prediction[5]

                    prediction_model = Prediction(
                        x1,
                        y1,
                        x2,
                        y2,
                        confidence,
                        violation
                    )
                    if prediction_model.confidence > 0.75:
                        prediction_items.append(prediction_model)
                predictions.append(prediction_items)

            if predictions:
                best_predictions = max(predictions, key=len)
            else:
                best_predictions = []
            return best_predictions
        except Exception as e:
            return e

    
    async def map_classes_to_model(self, predictions):
        try:
            object_predictions = [i for i in predictions 
                                    if (
                                        i.violation == 0.0 or  
                                        i.violation == 1.0
                                    )]

            person_predictions =  [i for i in predictions 
                                if (
                                        i.violation == 3.0
                                    )]
            persons_detected = await self.map_to_person_detected(object_predictions, person_predictions)

            return persons_detected
        except Exception as e:
            return e
        

    async def map_to_person_detected(self, object_violations: list, person_predictions: list) -> list[Person]:
        try:
            people_detected = []
            for person in person_predictions: 
                objects_detected = []
                for violation in object_violations:
                            
                            ## PERSON CLASS BOUNDING BOX CALC
                            (person_x_min, person_x_max, person_y_min, person_y_max, person_box_area) = await self.person_class_bounding_box_calc(person)
                            
                            ## OBJECT CLASS AREA CALC
                            object_box_area = await self.object_class_area_calc(violation)

                            is_x_within_bounds = violation.x >= person_x_min and violation.x <= person_x_max
                            is_y_within_bounds = violation.y >= person_y_min and violation.y <= person_y_max
                            is_object_area_valid = object_box_area <= person_box_area

                            if is_x_within_bounds and is_y_within_bounds and is_object_area_valid:
                                objects_detected.append(violation)

                            
                            # expand to detect helmet inside person but not on head

                            
                            # expand to detect person without violation

                people = Person(
                    person= person,
                    violations=objects_detected
                )
                people_detected.append(people)
                
                await self.application_log_violation(people_detected, objects_detected)
                

            return people_detected
        except Exception as e:
            return e
        

    
    async def person_class_bounding_box_calc(self, person):
        ## STEP 1
        ####### take person box hieght, width, x and y from Person class
        print(person.x1)
        original_height = abs(person.y2 - person.y1) 
        original_width = abs(person.x2 - person.x1)

        center_x = (person.x1 + person.x2) / 2
        center_y = (person.y1 + person.y2) / 2

        new_width = original_width * 1.10
        new_height = original_height * 1.10

        half_new_width = new_width / 2
        half_new_height = new_height / 2

        person_x_min = center_x - half_new_width
        person_x_max = center_x + half_new_width
        person_y_min = center_y - half_new_height
        person_y_max = center_y + half_new_height

        # STEP 4: Calculate the new area
        person_box_area = new_width * new_height

        return (person_x_min, person_x_max, person_y_min, person_y_max, person_box_area)


    async def object_class_area_calc(self, violation):
        try:
            violation_height = abs(violation.y2 - violation.y1) 
            violation_width = abs(violation.x2 - violation.x1)

            violation_box_area = violation_height * violation_width
            return violation_box_area
        except Exception as e:
            return e
    
    async def application_log_violation(self, people_detected, objects_detected):
        try:
            await application_log_services.log_violation(objects_detected, people_detected)
        except Exception as e:
            print(f"Application log violation exception: {e}")
            return e
