import cv2
import numpy as np
import os
from app.services.camera_services import CameraServices
from app.data_classes.image_adjustment_model import ImageAdjustmentModel

camera_services = CameraServices()


class ImageAdjustmentService():
    
    def check_valid_path(self):
        """
            @params: None

            @returns: tuple of string (prototxt_path, model_path)
                - Returns two filepath strings prototxt path and model path

            @exception: FileNotFoundError
                - logs exception message in application logs
        """
        try:
            # Caffe Model txt model path
            prototxt_path = "C://Users/vinny/eon_ppe_backend/app/model_location/file_specification.txt"

            # Caffe Model Line
            model_path = "C://Users/vinny/eon_ppe_backend/app/model_location/blurry_model.caffemodel"

            if os.path.exists(prototxt_path) and os.path.exists(model_path):
                return (prototxt_path, model_path)
        except FileNotFoundError as e:
            # application logs
            return e 
        except Exception as e:
            # application logs
            return e
        
          
    def setup_caffe_model(self, prototxt_path, model_path, image_file):
        """
            @params: str, str, MatLike

            @returns: tuple 
                - Returns two filepath strings 

            @exception: Exception
                - logs general exception message in application logs
            @exception: ValueError
                - logs value exception message in application logs
        """
        try:
            model = cv2.dnn.readNetFromCaffe(prototxt_path, model_path)

            # Get the width and height of the image
            height, width = image_file.shape[:2]

            # Increase the blury effect
            kernel_width = (width // 3) | 1
            kernel_height = (height // 3) | 1
            return (model, height, width, kernel_height, kernel_width)
        
        except Exception as e:
            # application logs
            return e
        
    def process_image_as_blob(self, model, image_file):
        """
            @params: MatLike
                - Receives a matrix object representing the image in memory

            @returns: Ndarray
                - Returns a ndarray representing output
        """
        try:
            # Process the image: resize and perform mean subtraction
            blob = cv2.dnn.blobFromImage(image_file, 1.0, (300, 300), (104.0, 177.0, 123.0))

            # Set the image into the neural network input
            model.setInput(blob)

            # Perform inference and get the result
            output = np.squeeze(model.forward())
            return output
        except Exception as e:
            # application logs
            return e

       
    def apply_blur_effect(self, output, height, width, kernel_height, kernel_width, image_file):
        # Loop with parameters
        for i in range(0, output.shape[0]):
            face_accuracy = output[i, 2]
            # Get high face accuracy
            # If face accuracy is more than 40%, then blur the bounding rectangle (face)
            if face_accuracy > 0.4:
                # Get the coordinates of the surrounding blur rectangle and scale it to the original image
                box = output[i, 3:7] * np.array([width, height, width, height])
                # Convert to integers
                start_x, start_y, end_x, end_y = box.astype(np.int64)
                # Get the face image
                face = image_file[start_y:end_y, start_x:end_x]
                # Apply Gaussian blur to this face
                face = cv2.GaussianBlur(face, (kernel_width, kernel_height), 0)
                # Insert the blurred face back into the original image
                image_file[start_y:end_y, start_x:end_x] = face
        return image_file
            
    
    def blur_face_images(self, image_file):
        """
            @params: MatLike
                - Receives a matrix object representing the image in memory

            @returns: base64 str
                - Returns a base64 str 
        """
        #blur_image_model = ImageAdjustmentModel()

        (prototxt_path, model_path) = self.check_valid_path()

        (model, height, width, kernel_height, kernel_width) = self.setup_caffe_model(prototxt_path, model_path, image_file)

        output = self.process_image_as_blob(model, image_file)

        blurred_image = self.apply_blur_effect(output, height, width, kernel_height, kernel_width, image_file)

        base64_img = camera_services.encode_image_base64(blurred_image)

        return base64_img

