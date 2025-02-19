from roboflow_connection import get_roboflow_workflow_response, get_roboflow_workflow_name_list,get_roboflow_key, roboflow_login_connection

roboflow_token = get_roboflow_key('roboflow_app_settings.env')
roboflow_connection = roboflow_login_connection(roboflow_token)
roboflow_workspace_name = roboflow_connection.workspace().url
roboflow_response = get_roboflow_workflow_response(roboflow_workspace_name, roboflow_token)


workflow_small_objects_detection = {
    'name' : roboflow_response['workflows'][0]['name'],
    'connection': roboflow_response['workflows'][0]['uct-count-arl'],
    
}

workflow_small_objects_detection = {
    'name' : roboflow_response['workflows'][0]['name'],
    'connection': roboflow_response['workflows'][0]['uct-count-arl'],
    
}
