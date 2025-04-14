predictions = {
  "predictions": [
        {
          "width": 195,
          "height": 358,
          "x": 341.5,
          "y": 458,
          "confidence": 0.9614913463592529,
          "class_id": 4,
          "class": "4",
          "detection_id": "15cce617-0f6d-496b-814c-d41ad6619ab0",
          "parent_id": "image"
        },
        {
          "width": 56,
          "height": 118,
          "x": 202,
          "y": 330,
          "confidence": 0.9288449883460999,
          "class_id": 4,
          "class": "4",
          "detection_id": "dfce3430-0010-4d97-ba76-5a15e70ac96c",
          "parent_id": "image"
        },
        {
          "width": 107,
          "height": 114,
          "x": 340.5,
          "y": 124,
          "confidence": 0.9226313233375549,
          "class_id": 0,
          "class": "2",
          "detection_id": "0d8ce430-a56d-43d0-a117-9bcc1f3c3160",
          "parent_id": "image"
        }
      ]
}

print(predictions['predictions'])

# # Parse the JSON data
# annotations = json.loads(predictions["annotations"]["objects"]["converted"])
# image_width = annotations["width"]
# image_height = annotations["height"]

# Convert and format the annotations
formatted_annotations = []
for box in predictions["predictions"]:
    label = box["class"]
    x_center = (float(box["x"]) + float(box["width"]) / 2) / 640
    y_center = (float(box["y"]) + float(box["height"]) / 2) / 640
    width = float(box["width"]) / 640
    height = float(box["height"]) / 640
    formatted_annotations.append(f"{label} {x_center} {y_center} {width} {height}")

# Print the formatted annotations
for annotation in formatted_annotations:
    print(annotation)


