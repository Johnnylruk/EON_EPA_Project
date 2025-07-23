from app.data_classes.message_result_modal import MessageResult, Predictions, Person
from app.services.application_logs_services import ApplicationLogServices

application_log_services = ApplicationLogServices()

class MessageServices():
    async def create_message(self, result: list) -> MessageResult:
        try:
            predictions_list = []
            for item in result:
                for i in item:
                    if i == "predictions":
                         
                        prediction = item[i]["predictions"]
                        predictions_list.append(prediction)                      

            if not predictions_list:
                return "No items in list"

            predictions_by_image = await self.create_prediction_model(predictions_list)
            persons_detected = await self.get_violation_from_predictions(predictions_by_image)

            result_model = MessageResult(persons_detected)
                        
            # ## encryption here
            
            return result_model

        except Exception as e:
            return e
    
    # try and use a mapping services
    async def create_prediction_model(self, predictions_list: list) -> list:
        try:
            
            predictions = []   
            for item in predictions_list:
                temp_predictions = []
                if not item:
                    print("No items in list")
                    continue
                for i in item:
                    if not i:
                        print("No items in list")
                        continue    
                    
                    confidence = i["confidence"]
                    violation = i["class"]
                    width = i["width"]
                    height = i["height"]
                    x = i["x"]
                    y = i["y"]
                    
                    prediction_model = Predictions(
                        confidence,
                        violation,
                        width,
                        height,
                        x,
                        y
                    )
                    if prediction_model.confidence > 0.75:
                        temp_predictions.append(prediction_model)
                predictions.append(temp_predictions)

            if predictions:
                best_predictions = max(predictions, key=len)
            else:
                best_predictions = []

            return best_predictions
        except Exception as e:
            return e

    async def get_violation_from_predictions(self, predictions: list) -> list[Person]:
        try:
            object_violations = await self.map_classes_to_model(predictions)   
            return object_violations
              
        except Exception as e:
            return e
    
    async def map_classes_to_model(self, predictions) -> list[Person]:
        

        object_predictions = [i for i in predictions 
                                if (
                                    i.violation == "12" or  
                                    i.violation == "15"
                                )]

        person_predictions =  [i for i in predictions 
                               if (
                                    i.violation == "5"
                                )]


        persons_detected = await self.map_to_person_detected(object_predictions, person_predictions)

        return persons_detected

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
        person_box_width = person.width
        person_box_height = person.height
        person_x = person.x
        person_y = person.y
        
        ## STEP 2
        ####### create 10% margin around the poerson box 
        margin_width = person_box_width * 0.1
        margin_height = person_box_height * 0.1
        
        person_width = (person_box_width + margin_width) / 2
        person_height = (person_box_height + margin_height) / 2

        person_x_min = person_x - person_width
        person_x_max = person_x + person_width
        person_y_min = person_y - person_height
        person_y_max = person_y + person_height

        person_box_area = (person_box_width + margin_width) * (person_box_height + margin_height)

        return (person_x_min, person_x_max, person_y_min, person_y_max, person_box_area)


    async def object_class_area_calc(self, object):
        try:
            object_width = object.width
            object_height = object.height

            object_box_area = object_height * object_width
            return object_box_area
        except Exception as e:
            return e
    
    async def application_log_violation(self, people_detected, objects_detected):
        try:
            await application_log_services.log_violation(objects_detected, people_detected)
        except Exception as e:
            print(f"Application log violation exception: {e}")
            return e
