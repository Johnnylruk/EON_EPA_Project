from inference_sdk import InferenceHTTPClient
from roboflow_connection import roboflow_connection_utility, get_roboflow_workflow_name_list
from roboflow_workflow_pipeline_rules import workflow_rules_dict
import base64
from PIL import Image
from io import BytesIO

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

def decode_images_from_string_format(workflow_output) -> list:
    images_list_to_decode = []
    for item in workflow_output:
        for image in item:
            if image == 'output_image':
                images_list_to_decode.append(base64.b64decode(item[image]))
    return images_list_to_decode

def save_images_after_decode(decoded_image_list: list):

    for pos, image in enumerate(decoded_image_list):
        open_image = Image.open(BytesIO(image))
        open_image.save(f'image_{pos + 1}_with_label.jpg')

images_list = ['PPE_Test_Image.jpg','PPE_Test_Image_2.jpg'] # Remind to myself to change it to a path

result = run_roboflow_workflow(
    roboflow_client, 
    workflow_rules_dict,
    roboflow_connection['connection_response'],
    roboflow_connection['workspace_name'],
    images_list
    )

imagem_to_save = decode_images_from_string_format(result)
save_images_after_decode(imagem_to_save)