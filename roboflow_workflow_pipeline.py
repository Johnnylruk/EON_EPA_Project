from inference_sdk import InferenceHTTPClient
from roboflow_connection import get_roboflow_key, roboflow_login_connection, get_roboflow_workflow_response, get_roboflow_workflow_name_list
from roboflow_workflow_pipeline_rules import workflow_rules_dict

roboflow_token = get_roboflow_key('roboflow_app_settings.env')
roboflow_connection = roboflow_login_connection(roboflow_token)
roboflow_workspace_name = roboflow_connection.workspace().url
workflow_connection_response = get_roboflow_workflow_response(roboflow_workspace_name, roboflow_token)

           
roboflow_client = InferenceHTTPClient(
    api_url='https://detect.roboflow.com',
    api_key=roboflow_token
)

def run_roboflow_workflow(roboflow_client: InferenceHTTPClient, workflow_rules_dict: dict, workflow_response: dict,workspace_name: str, images: str) -> list:

    get_workflows = get_roboflow_workflow_name_list(workflow_response)
    for workflow in get_workflows:
        print(f'For workflow {get_workflows[workflow]}, please type {workflow} for select this workflow')
        
    while True:
        select_workflow = str(input(f'Please, type a workflow name from the list above: ')).strip().lower()
        if select_workflow in get_workflows.keys():
            workflow = roboflow_client.run_workflow(
                workspace_name=workspace_name,
                workflow_id= workflow_rules_dict[select_workflow]['url'],
                images={
                    'image': images
                }
            )
            break
        else:
            print('We only accept workflow from the list, please type it again.')

    return workflow

run_roboflow_workflow(roboflow_client, workflow_rules_dict,workflow_connection_response,roboflow_workspace_name,'PPE_Test_Image.jpg')



