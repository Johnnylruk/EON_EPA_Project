import json
import os

# This is piece of RAW data from Roboflow
# I am changing manually converted value as it will be the same amount of work for copying and paste after manually label on roboflow
data = {
    "annotations": {
        "objects": {
            "converted": "{\"key\":\"00022_jpg.rf.cbbab30cf0acb6bf9bb500adc05503c9.jpg\",\"boxes\":[{\"label\":\"3\",\"x\":266.5,\"y\":434,\"width\":196,\"height\":217},{\"label\":\"4\",\"x\":261,\"y\":190,\"width\":67,\"height\":65},{\"label\":\"2\",\"x\":273,\"y\":399,\"width\":240,\"height\":463}],\"width\":640,\"height\":640}",
        }
    }
}

base_path = 'C:\\Users\\johnny.rodrigues\\Documents\\EPA\\datasets\\Main_Dataset\\Dataset_to_clean_1\\train\\labels'

# Filtering json raw data file to sample Json
def json_file_to_convert(json_roboflow_raw_file_txt: json) -> json:
    annotations = json.loads(json_roboflow_raw_file_txt["annotations"]["objects"]["converted"])
    return annotations

def format_json_file(annotation_json_format_file: json) -> str:
    formatted_annotations = []
    formatted_annotations_to_string = ''
    image_width = annotation_json_format_file["width"]
    image_height = annotation_json_format_file["height"]
   
    for box in annotation_json_format_file["boxes"]:
        label = box["label"]
        x_center = (float(box["x"]) + float(box["width"]) / 2) / image_width
        y_center = (float(box["y"]) + float(box["height"]) / 2) / image_height
        width = float(box["width"]) / image_width
        height = float(box["height"]) / image_height
        formatted_annotations.append(f"{label} {x_center} {y_center} {width} {height}")
    
    for annotation in formatted_annotations:
        formatted_annotations_to_string += annotation + '\n'
    
    return formatted_annotations_to_string

def save_annotation_to_text_file(file_to_save: str, json_roboflow_raw_file_txt, path_to_save, directory_name_to_save):
    json_key = json.loads(json_roboflow_raw_file_txt["annotations"]["objects"]["converted"])
    text_file_name = f'{json_key['key']}.txt'
    directory = os.path.join(path_to_save, directory_name_to_save)
    if not os.path.exists(directory):
        os.makedirs(directory)
    save_location = os.path.join(directory, text_file_name)
    with open(save_location, 'w') as file:
        file.write(file_to_save)

filtered_json = json_file_to_convert(data)
formatted_json = format_json_file(filtered_json)
save_annotation_to_text_file(formatted_json, data, base_path, 'transformed_labels_files')



