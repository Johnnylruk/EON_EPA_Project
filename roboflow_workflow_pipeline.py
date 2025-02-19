from roboflow import Roboflow
from inference_sdk import InferenceHTTPClient
from roboflow_connection import get_roboflow_key, roboflow_login_connection, connect_to_roboflow_workflow

roboflow_token = get_roboflow_key('roboflow_app_settings.env')
roboflow_connection = roboflow_login_connection(roboflow_token)
roboflow_workspace_name = roboflow_connection.workspace().url

workflow_connection_response = connect_to_roboflow_workflow(roboflow_workspace_name, roboflow_token)


            
roboflow_client = InferenceHTTPClient(
    api_url='https://detect.roboflow.com',
    api_key=roboflow_token
)


result = roboflow_client.run_workflow(
    workspace_name=roboflow_workspace_name,
    workflow_id='detect-count-and-visualize',
    images={
        'image': 'PPE_Test_Image.jpg'
    }
)

print(f'Result: {result}')
