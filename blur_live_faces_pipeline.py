import cv2
import numpy as np
import time


prototxt_path = "model_location/file_specification.txt"
model_path = "model_location/blurry_model.caffemodel"

def blur_real_time_faces(caffe_config_txt_file: str, caffe_model_file):
    
    model = cv2.dnn.readNetFromCaffe(caffe_config_txt_file, caffe_model_file)
    cap = cv2.VideoCapture(0)
    
    while True:
        try:
            start = time.time()
            live, image = cap.read()
            if not live:
                print("Failed to capture image")
                break
            
            h, w = image.shape[:2]
            kernel_width = (w // 7) | 1
            kernel_height = (h // 7) | 1
            blob = cv2.dnn.blobFromImage(image, 1.0, (300, 300), (104.0, 177.0, 123.0))
            model.setInput(blob)
            output = np.squeeze(model.forward())

            for i in range(0, output.shape[0]):
                face_accuracy = output[i, 2]
                if face_accuracy > 0.4:
                    box = output[i, 3:7] * np.array([w, h, w, h])
                    start_x, start_y, end_x, end_y = box.astype(int)
                    face = image[start_y:end_y, start_x:end_x]
                    face = cv2.GaussianBlur(face, (kernel_width, kernel_height), 0)
                    image[start_y:end_y, start_x:end_x] = face

            cv2.imshow("Faces blurred v1.0", image)
            if cv2.waitKey(1) == ord("q"):
                break
            time_elapsed = time.time() - start
            fps = 1 / time_elapsed
            print("FPS:", fps)
        except Exception as e:
            print(f"An error occurred: {e}")
            break

    cv2.destroyAllWindows()
    cap.release()

blur_real_time_faces(prototxt_path,model_path)