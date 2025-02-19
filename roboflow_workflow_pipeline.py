from inference_sdk import InferenceHTTPClient
from roboflow_connection import roboflow_connection_utility, get_roboflow_workflow_name_list
from roboflow_workflow_pipeline_rules import workflow_rules_dict

roboflow_connection = roboflow_connection_utility()


roboflow_client = InferenceHTTPClient(
    api_url='https://detect.roboflow.com',
    api_key=roboflow_connection['api_token']
)

def run_roboflow_workflow(roboflow_client: InferenceHTTPClient, workflow_rules_dict: dict, workflow_response: dict,workspace_name: str, images: str) -> list:

    get_workflows = get_roboflow_workflow_name_list(workflow_response)
    for workflow in get_workflows:
        print(f'{workflow}: {get_workflows[workflow]}')
        
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

run_roboflow_workflow(
    roboflow_client, 
    workflow_rules_dict,
    roboflow_connection['connection_response'],
    roboflow_connection['workspace_name'],
    'PPE_Test_Image.jpg'
    )



