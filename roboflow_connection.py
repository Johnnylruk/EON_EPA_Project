from roboflow import Roboflow
import os
import requests
from dotenv import load_dotenv

def get_roboflow_key(env_file_name: str) -> str:
    '''This function is going to be responsible to get 
        Roboflow .env file which contains the API Token
    '''
    load_dotenv(env_file_name)
    roboflow_token = os.getenv('ROBOFLOW_API_KEY')
    if roboflow_token is None:
        raise ValueError("API Key not found. Ensure the .env file is correctly loaded.")
    else:
        print('Roboflow Token was found')
        return roboflow_token

def roboflow_login_connection(api_token: str) -> Roboflow:
    '''This function is going to be responsible for 
        make the login to Roboflow utilising the API Token 
        that we got on the function get_roboflow_key'''
    
    roboflow_login = Roboflow(api_key=api_token)
    print("Successfully logged in to Roboflow!")
    return roboflow_login


def connect_to_roboflow_workspace(workspace_name: str, project_name: str, roboflow_login_connection: Roboflow):
    '''This function is going to be responsible to make the roboflow connect to our workspace'''

    project_connection = roboflow_login_connection.workspace(workspace_name).project(project_name)
    print(f'Successful connected to your {workspace_name} and project {project_name}')
    return project_connection

def get_roboflow_workflow_response(workspace_name, api_token):
    endpoint_url = "https://api.roboflow.com/"
    endpoint = f"{endpoint_url}{workspace_name}/workflows?api_key={api_token}"
    response = requests.get(endpoint)
    response = response.json()
    return response

def get_roboflow_workflow_name_list(workflow_response: Roboflow) -> dict:
    '''THis function is for get workflow list to easy identify which one is needed'''

    workflow_list = dict()
    if workflow_response['status'] == 'ok':
        for pos, workflow in enumerate(workflow_response['workflows']):
            workflow_list[f'workflow_{pos + 1}'] = workflow['name']
    return workflow_list
