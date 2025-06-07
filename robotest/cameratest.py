from ultralytics import YOLO
import cv2

# Load the trained model
model = YOLO("runs/train/yolov8-custom3/weights/best.pt")

# Run prediction with streaming output
results = model.predict(
    source=0,        # webcam
    conf=0.5,        # confidence threshold
    stream=True      # required to get iterable results
)

# Loop through results and display using OpenCV
for result in results:
    frame = result.plot()  # draw the bounding boxes
    cv2.imshow("YOLOv8 Live", frame)

    # Exit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
