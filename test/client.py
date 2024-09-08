import requests
import orjson
import base64
import io
from PIL import Image
import numpy as np
import openvino as ov
import time

core = ov.Core()
core.compile_model()

def preprocess_image(image_path, target_size=(224, 224)):
    mean = np.array([0.5, 0.5, 0.5]).reshape(1, 1, 3)
    std = np.array([0.5, 0.5, 0.5]).reshape(1, 1, 3)
    image = Image.open(image_path).resize(target_size)
    image = ((np.array(image) / 255.0 - mean) / std).astype(np.float32)
    image = np.transpose(image, (2, 0, 1))[None, ...]
    return base64.b64encode(image.tobytes()).decode('utf-8')

api_url = "https://0e0er7ojo8.execute-api.ap-southeast-1.amazonaws.com/dev/inference"

body = {
    "image": preprocess_image("./input/dog.jpg")
}

headers = {
    "Content-Type": "application/json"
}

def get_labels():
    with open("imagenet1k.txt", 'r') as file:
        lines = file.readlines()
        labels = [line.strip().strip('"')[:-2] for line in lines]
        return labels

def softmax(x):
    exp_x = np.exp(x - np.max(x))
    return exp_x / np.sum(exp_x)

def post_process(output_data):
    probabilities = softmax(output_data)
    top_5_clx_ids = np.argsort(probabilities)[::-1][:5]
    top_5_probs = probabilities[top_5_clx_ids]
    labels = get_labels()

    for i, (prob, id) in enumerate(zip(top_5_probs, top_5_clx_ids)):
        print(f"Rank {i+1}: Class = {labels[id]}, Probability = {prob:.6f}")
        
        
if __name__ == "__main__":
    
    response = requests.post(api_url, headers=headers, data=orjson.dumps(body))
    if response.status_code == 200:
        print("Response Successfully:\n")
        output = np.array(response.json()["logits"][0])
        post_process(output)
        
    else:
        print(f"Failed to retrieve data: {response.status_code}")