from roboflow_connection import roboflow_connection_utility

roboflow_connection = roboflow_connection_utility()


workflow_small_objects_detection = {
    'name' : roboflow_connection['connection_response']['workflows'][0]['name'],
    'url': roboflow_connection['connection_response']['workflows'][0]['url'],
}

workflow_detect_count_visualize = {
    'name' : roboflow_connection['connection_response']['workflows'][1]['name'],
    'url': roboflow_connection['connection_response']['workflows'][1]['url'],
}

workflow_rules_dict = {
    'workflow_1': workflow_small_objects_detection,
    'workflow_2': workflow_detect_count_visualize
}