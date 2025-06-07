
from app.services.roboflow_connection_services import RoboflowServices

roboflow_services = RoboflowServices()

class WorkflowService():
    def run_roboflow_workflow(self, roboflow_client, workflow_rules_dict: dict, workflow_response: dict,workspace_name: str, images: str) -> list:

        get_workflows = roboflow_services.get_roboflow_workflow_name_list(workflow_response)
        for detection_workflow in get_workflows:
            print(f'{detection_workflow}: {get_workflows[detection_workflow]}')
        

        workflow = roboflow_client.run_workflow(
                    workspace_name=workspace_name,
                    workflow_id= workflow_rules_dict[detection_workflow]['url'],
                    images={
                        "image": images
                    }
                )
        return workflow

