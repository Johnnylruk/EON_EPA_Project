from app.data_classes.message_result_modal import MessageResult, Predictions, Helmet, HiVis
from app.services.roboflow_connection_services import RoboflowServices

roboflow_services = RoboflowServices()

class MessageServices():
    def create_message(self, result):
        try:
            predictions_list = result[0]["predictions"]["predictions"]
            if not predictions_list:
                return "No items in list"

            output_image = result[0]["output_image"]

            predictions = self.create_prediction_model(predictions_list)
            (helmet_predictions, hi_vis_predictions) = self.filtered_predictions(predictions)
            result_model = MessageResult(helmet_predictions, hi_vis_predictions, output_image)
                        
            # ## encryption here
            
            return result_model

        except Exception as e:
            return e

    def create_prediction_model(self, predictions_list):
        try:
            predictions = list()
            for item in predictions_list:

                confidence = item["confidence"]
                detection_id = item["detection_id"]
                violation_id = item["class_id"]
                violation = item["class"]

                prediction_model = Predictions(
                    confidence,
                    detection_id,
                    violation_id,
                    violation
                )
                
                predictions.append(prediction_model)
            return predictions
        except Exception as e:
            return e

    def filtered_predictions(self, predictions):
        try:
            get_class_names = roboflow_services.get_roboflow_classes()
            print(get_class_names)

            helmet_violations = [i for i in predictions if i["violations"] == "no-helmet"]

            helmet_predictions = Helmet(
                violations=helmet_violations,
                amount=len(helmet_violations)
            )

            hi_vis_violations = [i for i in predictions if i["violations"] == "no-jacket"]

            hi_vis_predictions = HiVis(
                violations=hi_vis_violations,
                amount=len(hi_vis_violations)
            )
            return (helmet_predictions, hi_vis_predictions)
        except Exception as e:
            return e