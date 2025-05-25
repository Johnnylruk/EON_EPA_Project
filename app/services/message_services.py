from app.data_classes.message_result_modal import MessageResult, Predictions, Helmet, HiVis


class MessageServices():
    def create_message(self, result):
        predictions_list = result[0]["predictions"]["predictions"]
        output_image = result[0]["output_image"]

        predictions = self.create_prediction_model(predictions_list)
        (helmet_predictions, hi_vis_predictions )= self.filtered_predictions(predictions)
        result_model = MessageResult(helmet_predictions, hi_vis_predictions, output_image)

        # ## encryption here
        
        return result_model


    def create_prediction_model(self, predictions_list):
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

    def filtered_predictions(predictions):
        print(predictions)
        helmet_predictions = Helmet(
            violations=predictions
        )
    