from roboflow import Roboflow
import os
from roboflow_connection import roboflow_connection_utility, connect_to_roboflow_workspace

roboflow_connection = roboflow_connection_utility()

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


workspace_connection = connect_to_roboflow_workspace(
    roboflow_connection['workspace_name'], 
    roboflow_connection['project_name'], 
    roboflow_connection['roboflow_login']
    )

import_image_to_roboflow('images', workspace_connection)