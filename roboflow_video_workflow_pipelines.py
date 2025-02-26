from inference import InferencePipeline
from roboflow_connection import roboflow_connection_utility
from roboflow_workflow_pipeline_rules import workflow_rules_dict
import threading

roboflow_connection = roboflow_connection_utility()

def my_sink(result, video_frame):
    print(result) # do something with the predictions of each frame
    pipeline._stop()
    
# initialize a pipeline object
pipeline = InferencePipeline.init_with_workflow(
    api_key=roboflow_connection['api_token'],
    workspace_name=roboflow_connection['workspace_name'],
    workflow_id=workflow_rules_dict['workflow_2']['url'],
    video_reference='ppe_video_test.mov', # Path to video, RSTP stream, device id (int, usually 0 for built in webcams), or RTSP stream url
    on_prediction=my_sink
)
thread = threading.Thread(target=pipeline.start)
#pipeline.start() #start the pipeline
thread.start()
thread.join(timeout=10)

print(pipeline)
#pipeline.join() #wait for the pipeline thread to finish

