import json
import base64
import numpy as np
import openvino as ov

core = ov.Core()
compiled_model = core.compile_model("/opt/python/mobilenetv4.xml", "AUTO")
output_layer = compiled_model.output(0)
    
def lambda_handler(event, context):
    image = json.loads(event['body'])['image']
    image = base64.b64decode(image)
    image = np.frombuffer(image, dtype=np.float32).reshape(1, 3, 224, 224)
    result = compiled_model(image)
    output_data = result[output_layer]
    return {
        'statusCode': 200,
        'body': json.dumps({
            'logits': output_data.tolist(),
        })
    }