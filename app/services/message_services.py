from app.data_classes.message_result_modal import MessageResult, Predictions


class MessageServices():
    def create_message(self, result):
        predictions_list = result[0]["predictions"]["predictions"]
        output_image = result[0]["output_image"]

        confidence = predictions_list[0]["confidence"]
        print(confidence)

        predictions = list()
        for item in predictions_list:
            prediction_model = Predictions()
            prediction_model.confidence = predictions_list[item]["confidence"]
            prediction_model.detection_id = predictions_list[item]["detection_id"]
            prediction_model.violation_id = predictions_list[item]["class_id"]
            prediction_model.violation = predictions_list[item]["class"]
            predictions.append(prediction_model)


        result_model = MessageResult()
        result_model.violations = predictions
        result_model.output_image = output_image
        

        # ## encryption here
        
        return result_model
    