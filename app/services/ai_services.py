import requests
import json
 

class AI_Services():
    url = "https://yolov8-ai.onrender.com/predict/"
    file_path = "ppe.png"
    
    print(f"Preparing to send image: {file_path} to {url}")
    
    with open(file_path, "rb") as f:
        print("Reading image file")
        files = {"file": (file_path, f, "image/jpeg")}
    
        print("Sending POST request to the API")
        response = requests.post(url, files=files)
    
    print(f"Response status code: {response.status_code}")
    
    if response.ok:
        print("Parsing and formatting JSON response")
        data = response.json()
        print(json.dumps(data, indent=2))
    else:
        print("Request failed")
        print(response.text)