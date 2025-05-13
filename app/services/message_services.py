from app.data_classes.message_result_modal import MessageResult


class MessageServices():
    def create_message(self, result):
        class_names = result[0]["class_names_array"]
        predictions_list = result[0]["predictions"]["predictions"]
        output_image = result[0]["output_image"]

        print(predictions_list)
        
        return predictions_list
        # result_model = MessageResult()

        # result_model.class_names = class_names
        # result_model.confidence = confidence
        # result_model.output_image = output_image

        # ## encryption here
        
        # return result_model
    