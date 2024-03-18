import os
from flask import Flask, jsonify, send_file
from flask import request
import random
import uuid
from diffusers import DiffusionPipeline
import torch
import threading
import time
from urllib.parse import unquote
import shutil
os.environ['PYTORCH_MPS_HIGH_WATERMARK_RATIO'] = '0.0'

app = Flask(__name__)

LightMode = True # If this is true it returns random images, if it is false it returns an artifically generated images
def start_thread():
    print("Starting thread")
    threading.Thread(target=check_and_generate_images, daemon=True).start()


@app.route('/get-image/<image_id>')
def get_image(image_id):
    #open requests.csv and check if the image_id is in the file and that the ip address is the same as the requester
    with open('requests.csv', 'r') as file:
        imageRequests = file.readlines()
        for imageRequest in imageRequests:
            request_id, prompt, ip_address, genirated = imageRequest.split(',')
            print(request_id)
            print(image_id)
            print(request_id.strip() == image_id)
            if request_id.strip() == image_id and ip_address.strip() == request.remote_addr and genirated.strip() == "Generated":   
                try: 
                    return send_file(f'images/{image_id}.jpg', mimetype='image/jpg')
                finally:
                    os.remove(f'images/{image_id}.jpg')
                    remove_image_from_csv(image_id)  
    return "Invalid request"

def remove_image_from_csv(image_id):
                        with open('requests.csv', 'r') as file:
                            lines = file.readlines()

                        with open('requests.csv', 'w') as file:
                            for line in lines:
                                request_id, _, _, _ = line.split(',')
                                if request_id.strip() != image_id:
                                    file.write(line)

@app.route('/request-image/<prompt>')
def request_image(prompt):
    ip_address = request.remote_addr
    image_id = str(uuid.uuid4())
    
    with open('requests.csv', 'a') as file:
        file.write(f'{image_id},{unquote(prompt)},{ip_address},Not generated\n')
    
    return image_id.strip()

def request_image(prompt):
    ip_address = request.remote_addr
    image_id = str(uuid.uuid4())
    
    with open('requests.csv', 'a') as file:
        file.write(f'{image_id},{prompt},{ip_address},Not generated\n')

    return image_id

@app.route('/status/<image_id>')
def image_status(image_id):
    with open('requests.csv', 'r') as file:
        image_requests = file.readlines()
        for image_request in image_requests:
            request_id, prompt, ip_address, genirated = image_request.split(',')
            if request_id.strip() == image_id and ip_address.strip() == request.remote_addr:
                return genirated.strip()
    return "Invalid request ID"

@app.route('/all-status')
def all_status():
    all_status = ""
    with open('requests.csv', 'r') as file:
        image_requests = file.readlines()
        for image_request in image_requests:
            request_id, prompt, ip_address, genirated = image_request.split(',')
            if ip_address.strip() == request.remote_addr:
                all_status = all_status + f'{request_id.strip()}:{genirated.strip()},' 
    if len(all_status) == 0:
        return "No requests"
    return all_status[:-1]

def random_image(image_id):
    base_dir = os.path.dirname(__file__) 
    imageNo = random.randint(0, 9)
    random_image= os.path.join(base_dir, f'exampleImages/{imageNo}.jpg')
    shutil.copy(random_image, f'images/{image_id}.jpg')
    return random_image

def check_and_generate_images():
    while True:
        with open('requests.csv', 'r') as file:
            requests = file.readlines()
        
        # This list will hold the updated requests
        updated_requests = []

        for request_line in requests:
            request_id, prompt, ip_address, generated = request_line.split(',')
            if generated.strip() == "Not generated":
                generate_image(prompt, request_id)
                updated_requests.append(f'{request_id},{prompt},{ip_address},Generated\n')
            else:
                # If it's already generated or in process, just append it to the list as is
                updated_requests.append(request_line)

        # Now write the updated_requests back to the file
        with open('requests.csv', 'w') as file:
            file.writelines(updated_requests)
            
        time.sleep(10)  # check every 10 seconds

# Ensure generate_image updates request status immediately
def generate_image(prompt, image_id):
    if LightMode:
        # If in LightMode, use a placeholder image
        random_image(image_id)
        return 
    
    print(f"Generating image for: {image_id}")
    pipeline = DiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v1-4", torch_dtype=torch.float32)
    device = "cpu"
    pipeline = pipeline.to(device)
    
    image = pipeline(prompt, num_inference_steps=8, guidance_scale=7.5).images[0]
    image.save(f'images/{image_id}.jpg')


if __name__ == '__main__':
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        start_thread()
    app.run(debug=True)