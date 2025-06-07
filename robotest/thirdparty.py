from inference_sdk import InferenceHTTPClient
from pprint import pprint

CLIENT = InferenceHTTPClient(
    api_url="https://serverless.roboflow.com",
    api_key="FiOTxrnapkJdSer95zFT"
)

result = CLIENT.infer("person2.jpg", model_id="construction-site-safety/27")


pprint(result)
