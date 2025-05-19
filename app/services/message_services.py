from app.data_classes.message_result_modal import MessageResult, Predictions


class MessageServices():
    def create_message(self, result):
        predictions_list = result[0]["predictions"]["predictions"]
        output_image = result[0]["output_image"]
        print(len(predictions_list))

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

        result_model = MessageResult(predictions, output_image)

        # ## encryption here
        
        return result_model
    