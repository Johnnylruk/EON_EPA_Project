from ultralytics import YOLO


class Face_Detection_AI():

    def run_face_detection(image_file):
        # Load yolov8n face model file
        model = YOLO('./face_detection_model/yolov8n-face.pt') 

        # Run detection
        results = model(image_file)

        return results