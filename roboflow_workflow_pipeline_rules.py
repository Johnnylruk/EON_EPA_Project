from roboflow_connection import get_roboflow_workflow_response, get_roboflow_workflow_name_list,get_roboflow_key, roboflow_login_connection

roboflow_token = get_roboflow_key('roboflow_app_settings.env')
roboflow_connection = roboflow_login_connection(roboflow_token)
roboflow_workspace_name = roboflow_connection.workspace().url
roboflow_response = get_roboflow_workflow_response(roboflow_workspace_name, roboflow_token)


workflow_small_objects_detection = {
    'name' : roboflow_response['workflows'][0]['name'],
    'url': roboflow_response['workflows'][0]['url'],
}

workflow_detect_count_visualize = {
    'name' : roboflow_response['workflows'][1]['name'],
    'url': roboflow_response['workflows'][1]['url'],
}

workflow_rules_dict = {
    'workflow_1': workflow_small_objects_detection,
    'workflow_2': workflow_detect_count_visualize
}