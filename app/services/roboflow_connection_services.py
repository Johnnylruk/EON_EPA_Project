from roboflow import Roboflow
import os
import requests
from dotenv import load_dotenv

class RoboflowServices():

    def get_roboflow_key(self) -> str:
        '''This function is going to be responsible to get 
            Roboflow .env file which contains the API Token
        '''
        try:
            load_dotenv()
            roboflow_token = os.getenv('ROBOFLOW_API_KEY')
            if roboflow_token is None:
                raise ValueError("API Key not found. Ensure the .env file is correctly loaded.")
            else:
                print('Roboflow Token was found')
                return roboflow_token
        except Exception as e:
            return e

    def roboflow_login_connection(self, api_token: str) -> Roboflow:
        '''This function is going to be responsible for 
            make the login to Roboflow utilising the API Token 
            that we got on the function get_roboflow_key'''
        try:
            roboflow_login = Roboflow(api_key=api_token)
            print("Successfully logged in to Roboflow!")
            return roboflow_login
        except Exception as e:
            return e

    def connect_to_roboflow_workspace(self,workspace_name: str, project_name: str, roboflow_login_connection: Roboflow):
        '''This function is going to be responsible to make the roboflow connect to our workspace'''
        try:
            project_connection = roboflow_login_connection.workspace(workspace_name).project(project_name)
            print(f'Successful connected to your {workspace_name} and project {project_name}')
            return project_connection
        except Exception as e:
            return e

    def get_roboflow_workflow_response(self, workspace_name, api_token):
        try:
            endpoint_url = "https://api.roboflow.com/"
            endpoint = f"{endpoint_url}{workspace_name}/workflows?api_key={api_token}"
            response = requests.get(endpoint)
            response = response.json()
            return response
        except Exception as e:
            return e

    def get_roboflow_workflow_name_list(self, workflow_response: Roboflow) -> dict:
        '''THis function is for get workflow list to easy identify which one is needed'''
        try:
            workflow_list = dict()
            if workflow_response['status'] == 'ok':
                for pos, workflow in enumerate(workflow_response['workflows']):
                    workflow_list[f'workflow_{pos + 1}'] = workflow['name']
            return workflow_list
        except Exception as e:
            return e


    # def deploy_roboflow_model(self):
    #     try:
    #         (roboflow_token, roboflow_connection, roboflow_project_list) = self.roboflow_details_helper()
    #         project_id = roboflow_project_list.project_list[0]['name'].lower()
    #         project = roboflow_project_list.project(project_id)
    #         classes = project.classes

            
    #         absolute_path = f"C://Users/vinny/eon_ppe_backend/app/model_weights"
    #         roboflow_project_list.deploy_model(
    #             model_type="yolov8n",
    #             model_path=f"{absolute_path}",
    #             project_ids=[project_id],
    #             model_name=f"Project_Falcon_Model",
    #             filename="yolov8n.pt"
    #         )
    #     except Exception as e:
    #         return e

    def get_roboflow_classes(self) -> list:
        try:
            (roboflow_token, roboflow_connection, roboflow_project_list) = self.roboflow_details_helper()
            project_id = roboflow_project_list.project_list[0]['name'].lower()
            project = roboflow_project_list.project(project_id)
            classes = project.classes
            return classes
        
        except Exception as e:
            return e


    def roboflow_connection_utility(self) -> dict:
        '''This is responsible to call all connections'''
        try:
            (roboflow_token, roboflow_connection, roboflow_project_list) = self.roboflow_details_helper()
            workflow_connection_response = self.get_roboflow_workflow_response(roboflow_project_list.url, roboflow_token)

            roboflow_utility_connection_dict = {
                'api_token' : roboflow_token,
                'roboflow_login': roboflow_connection,
                'workspace_name': roboflow_project_list.url,
                'connection_response': workflow_connection_response,
                'project_name': roboflow_project_list.project_list[0]['name'].lower()
            }
            return roboflow_utility_connection_dict
        
        except Exception as e:
            return e


    def roboflow_details_helper(self):
        try:
            roboflow_token = self.get_roboflow_key()
            roboflow_connection = self.roboflow_login_connection(roboflow_token)
            roboflow_project_list = roboflow_connection.workspace()
            return (roboflow_token, roboflow_connection, roboflow_project_list)
        except Exception as e:
            return e