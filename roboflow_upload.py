from roboflow import Roboflow
import os
from dotenv import load_dotenv

var = load_dotenv('roboflow_app_settings.env')
roboflow_token = os.getenv("ROBOFLOW_API_KEY")

if roboflow_token is None:
    raise ValueError("API Key not found. Ensure the .env file is correctly loaded.")

roboflow_connection = Roboflow(api_key=roboflow_token)

workspace_name = 'epaproject'
project_name = 'ppe-identification'

get_project = roboflow_connection.workspace(workspace_name).project(project_name)

dataset_path = os.listdir('images')

for file in dataset_path:
    get_file_path = os.path.join('images', file)

    if os.path.isfile(get_file_path):
        get_project.upload(get_file_path)

