from roboflow import Roboflow
import os
from roboflow_connection import get_roboflow_key, roboflow_login_connection, connect_to_roboflow_workspace


def import_image_to_roboflow(image_directory_path: str, project_connection: Roboflow):
    '''This function is going to be responsible to import our dataset on Roboflow environment'''
    count_images = 0
    dataset_path = os.listdir(image_directory_path)

    for image_file in dataset_path:
        create_full_path = os.path.join(image_directory_path, image_file)
        if os.path.isfile(create_full_path):
            project_connection.upload(create_full_path)
            count_images += 1
    print(f'You have uploaded a total of {count_images}')
    print('Finished operations with Roboflow.')

roboflow_token = get_roboflow_key('roboflow_app_settings.env')
roboflow_connection = roboflow_login_connection(roboflow_token)

workspace_connection = connect_to_roboflow_workspace('epaproject', 'ppe-identification', roboflow_connection)
import_image_to_roboflow('images', workspace_connection)