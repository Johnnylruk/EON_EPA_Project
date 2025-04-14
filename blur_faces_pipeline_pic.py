import cv2
import numpy as np

prototxt_path = "weights/deploy.prototxt.txt"
model_path = "weights/res10_300x300_ssd_iter_140000_fp16.caffemodel"

model = cv2.dnn.readNetFromCaffe(prototxt_path, model_path)

# Load the image from a file
image_path = "PPE_Test_Image.jpg"
image = cv2.imread(image_path)

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
        start_x, start_y, end_x, end_y = box.astype(np.int)
        face = image[start_y:end_y, start_x:end_x]
        face = cv2.GaussianBlur(face, (kernel_width, kernel_height), 0)
        image[start_y:end_y, start_x:end_x] = face

cv2.imshow("Faces blurred v1.0", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
