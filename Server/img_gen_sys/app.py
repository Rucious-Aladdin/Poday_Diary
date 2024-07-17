# -*- coding: utf-8 -*-
import base64
from util import load_text_file, load_config
from img_gen_module import StableDiffusionImageGenerator
from flask import Flask, request, make_response, jsonify

app = Flask(__name__)

config_path = "./config"
config_filename = "config.txt"
config = load_text_file(config_path, config_filename)
args = load_config(config)
host_addr = "0.0.0.0"
host_port = 5002

# Initialize the image generation module once
img_gen_module = StableDiffusionImageGenerator.set_initial_arguments(args)

@app.route("/stable_diffusion/generate", methods=["POST"])
def get_image():
    data = request.json
    img_prompt = data.get("img_prompt")
    user_id = data.get("user_id")
    date = data.get("date")
    response = img_gen_module.get_img(img_prompt, display=False)
    img_gen_module.save_image(user_id, date)
    print("prompt: %s" % img_gen_module.args.prompt)
    if response.headers.get("finish-reason") == 'CONTENT_FILTERED':
        return jsonify({"img_prompt": img_prompt, "status": "false", "image": ""}), 400

    output_image = response.content
    encoded_image = base64.b64encode(output_image).decode('utf-8')
    
    return jsonify({"img_prompt": img_prompt, "status": "true", "image": encoded_image})

if __name__ == "__main__":
    app.run(host=host_addr, port=host_port, debug=True)
