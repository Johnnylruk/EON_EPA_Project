from app.services.roboflow_connection_services import RoboflowServices

roboflow_services = RoboflowServices()

roboflow_connection = roboflow_services.roboflow_connection_utility()

workflow_small_objects_detection = {
    'name' : roboflow_connection['connection_response']['workflows'][0]['name'],
    'url': roboflow_connection['connection_response']['workflows'][0]['url'],
}

workflow_rules_dict = {
    'workflow_1': workflow_small_objects_detection
}