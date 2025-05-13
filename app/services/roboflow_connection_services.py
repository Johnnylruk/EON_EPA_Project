from roboflow import Roboflow
import os
import requests
from dotenv import load_dotenv


class RoboflowServices():

    def get_roboflow_key(self) -> str:
        '''This function is going to be responsible to get 
            Roboflow .env file which contains the API Token
        '''
        load_dotenv()
        roboflow_token = os.getenv('ROBOFLOW_API_KEY')
        if roboflow_token is None:
            raise ValueError("API Key not found. Ensure the .env file is correctly loaded.")
        else:
            print('Roboflow Token was found')
            return roboflow_token

    def roboflow_login_connection(self, api_token: str) -> Roboflow:
        '''This function is going to be responsible for 
            make the login to Roboflow utilising the API Token 
            that we got on the function get_roboflow_key'''
        
        roboflow_login = Roboflow(api_key=api_token)
        print("Successfully logged in to Roboflow!")
        return roboflow_login


    def connect_to_roboflow_workspace(self,workspace_name: str, project_name: str, roboflow_login_connection: Roboflow):
        '''This function is going to be responsible to make the roboflow connect to our workspace'''

        project_connection = roboflow_login_connection.workspace(workspace_name).project(project_name)
        print(f'Successful connected to your {workspace_name} and project {project_name}')
        return project_connection

    def get_roboflow_workflow_response(self, workspace_name, api_token):
        endpoint_url = "https://api.roboflow.com/"
        endpoint = f"{endpoint_url}{workspace_name}/workflows?api_key={api_token}"
        response = requests.get(endpoint)
        response = response.json()
        return response

    def get_roboflow_workflow_name_list(self, workflow_response: Roboflow) -> dict:
        '''THis function is for get workflow list to easy identify which one is needed'''

        workflow_list = dict()
        if workflow_response['status'] == 'ok':
            for pos, workflow in enumerate(workflow_response['workflows']):
                workflow_list[f'workflow_{pos + 1}'] = workflow['name']
        return workflow_list


    def deploy_roboflow_model(self):
        roboflow_token = self.get_roboflow_key()
        roboflow_connection = self.roboflow_login_connection(roboflow_token)
        roboflow_project_list = roboflow_connection.workspace()
        rf = Roboflow(api_key=roboflow_token)
        workspace = rf.workspace(roboflow_project_list.url)
        project_id = roboflow_project_list.project_list[0]['name'].lower()
     
        absolute_path = f"C://Users/vinny/eon_ppe_backend/app/model_weights"
        workspace.deploy_model(
            model_type="yolov8n",
            model_path=f"{absolute_path}",
            project_ids=[project_id],
            model_name=f"Project_Falcon_Model",
            filename="yolov8n.pt"
        )

    def roboflow_connection_utility(self) -> dict:
        '''This is responsible to call all connections'''
        roboflow_token = self.get_roboflow_key()
        roboflow_connection = self.roboflow_login_connection(roboflow_token)
        roboflow_project_list = roboflow_connection.workspace()
        workflow_connection_response = self.get_roboflow_workflow_response(roboflow_project_list.url, roboflow_token)

        roboflow_utility_connection_dict = {
            'api_token' : roboflow_token,
            'roboflow_login': roboflow_connection,
            'workspace_name': roboflow_project_list.url,
            'connection_response': workflow_connection_response,
            'project_name': roboflow_project_list.project_list[0]['name'].lower()
        }

        return roboflow_utility_connection_dict

