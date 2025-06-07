import cv2
import numpy as np
import time
import sys
import os

# Caffe Model txt model path
prototxt_path = "model_location/file_specification.txt"

# Caffe Model Line
model_path = "model_location/blurry_model.caffemodel"

# Load the Caffe model
model = cv2.dnn.readNetFromCaffe(prototxt_path, model_path)

# Provide video path as an argument
video_path = sys.argv[1]

output_directory = "output/"

os.makedirs(output_directory, exist_ok=True)

# Capture frames from video
capture = cv2.VideoCapture(video_path)

# Extract filename from video_path
filename = os.path.basename(video_path)

# Separate filename and extension
the_name, extension = os.path.splitext(filename)

# Create a four-character code (fourcc) used to specify the video codec
fourcc = cv2.VideoWriter_fourcc(*"XVID")
video, image = capture.read()
print(image.shape)
output_video_path = cv2.VideoWriter(
    os.path.join(output_directory, f"{the_name}_blurred.avi"),
    fourcc,
    20.0,
    (image.shape[1], image.shape[0]),
)

while True:  # Forever looping
    start = time.time()
    captured, image = capture.read()

    # Get width and height of the image
    if not captured:
        break
    h, w = image.shape[:2]
    kernel_width = (w // 3) | 1
    kernel_height = (h // 3) | 1

    # Preprocess the image: resize and perform mean subtraction
    blob = cv2.dnn.blobFromImage(image, 1.0, (300, 300), (104.0, 177.0, 123.0))
    # Set the image into the input of the neural network
    model.setInput(blob)
    # Perform inference and get the result
    output = np.squeeze(model.forward())
    for i in range(0, output.shape[0]):
        confidence = output[i, 2]
        # Get the confidence
        # If confidence is above 40%, then blur the bounding box (face)
        if confidence > 0.4:
            # Get the surrounding box coordinates and upscale them to original image
            box = output[i, 3:7] * np.array([w, h, w, h])
            # Convert to integers
            start_x, start_y, end_x, end_y = box.astype(np.int64)
            # Get the face image
            face = image[start_y:end_y, start_x:end_x]
            # Apply Gaussian blur to this face
            face = cv2.GaussianBlur(face, (kernel_width, kernel_height), 0)
            # Put the blurred face into the original image
            image[start_y:end_y, start_x:end_x] = face

    # Set width & height of the image in the window
    width = 480
    height = 640
    # Set window size according to the original image
    cv2.namedWindow("The results", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("The results", width, height)

    # Display the result
    cv2.imshow("The results", image)

    # Close the window if "q" is pressed
    if cv2.waitKey(1) == ord("q"):
        break
    time_elapsed = time.time() - start
    fps = 1 / time_elapsed
    print("FPS:", fps)
    output_video_path.write(image)

cv2.destroyAllWindows()
capture.release()
output_video_path.release()
