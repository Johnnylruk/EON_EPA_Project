import cv2
import numpy as np
import sys
import os

# Caffe Model txt model path
prototxt_path = "model_location/file_specification.txt"

# Caffe Model Line
model_path = "model_location/blurry_model.caffemodel"

# Load Caffe Model
model = cv2.dnn.readNetFromCaffe(prototxt_path, model_path)

# Pass Image path as argument
# image_path = sys.argv[1]

image_base_path = 'images'

images_dir = os.listdir(image_base_path)
image_path = os.path.join(image_base_path, images_dir[0])


output_directory = "output/"

os.makedirs(output_directory, exist_ok=True)
# Load the image to be tested
image = cv2.imread(image_path)

# Extract files from image path
filename = os.path.basename(image_path)

# Separating file names and extensions
name, extension = os.path.splitext(filename)

# Combine output directory & file name with the suffix "_blurred"
output_image_path = os.path.join(output_directory, f"{name}_blurred{extension}")

# Get the width and height of the image
height, width = image.shape[:2]

# Increase the blury effect
kernel_width = (width // 3) | 1
kernel_height = (height // 3) | 1
# Process the image: resize and perform mean subtraction
blob = cv2.dnn.blobFromImage(image, 1.0, (300, 300), (104.0, 177.0, 123.0))

# Set the image into the neural network input
model.setInput(blob)

# Perform inference and get the result
output = np.squeeze(model.forward())

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
        face = image[start_y:end_y, start_x:end_x]
        # Apply Gaussian blur to this face
        face = cv2.GaussianBlur(face, (kernel_width, kernel_height), 0)
        # Insert the blurred face back into the original image
        image[start_y:end_y, start_x:end_x] = face

# Set the width & height of the image in the window
width = 1080
height = 540

# Set the window size according to the original image
cv2.namedWindow("The results", cv2.WINDOW_NORMAL)
cv2.resizeWindow("The results", width, height)

cv2.imshow("The results", image)
cv2.waitKey(0)
cv2.imwrite(output_image_path, image)
