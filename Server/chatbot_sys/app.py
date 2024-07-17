from flask import Flask, request, make_response
import json
import requests
from chatbot import OpenAIConversationModule
from util import *

# Flask init
app = Flask(__name__)

# load prompt file
prompt_path = "./prompt/"
assitant_prompt_filename = "assitant_prompts.txt"
last_prompt_filename = "last_prompts.txt"
initial_questions_filename = "initial_questions.txt"
assitant_prompts = load_text_file(prompt_path, assitant_prompt_filename)
last_prompts = load_text_file(prompt_path, last_prompt_filename)
initial_questions = load_text_file(prompt_path, initial_questions_filename)

# load config_file
config_path = "./config/"
config_filename = "gpt_config.txt"
gpt_config = load_text_file(config_path, config_filename)
args = load_config(gpt_config)
# definite host_addr, host_port
host_addr = "0.0.0.0"
host_port = 5001

#openai_module = OpenAIConversationModule(args, assitant_prompts)

@app.route("/openai/response/init", methods=["POST"])
def init_openai():
    global openai_module
    openai_module = OpenAIConversationModule(args, assitant_prompts, last_prompts, initial_questions)
    response = openai_module.set_initial_question()
    result = json.dumps({"response": response, "state": "module is ready", "is_last": False}, ensure_ascii=False, indent=4)
    result = make_response(result)
    return result

@app.route("/openai/response/next", methods=["POST"])
def req_next_response():
    data = request.json
    user_text = data.get("user_text")
    response = openai_module.get_next_response(user_text=user_text)
    if "일기를 작성할게요." in response:
        result = json.dumps({"response": response, "is_last": True}, ensure_ascii=False, indent=4)
    else:
        result = json.dumps({"response": response, "is_last": False}, ensure_ascii=False, indent=4)
    result = make_response(result)
    return result

@app.route("/openai/response/last", methods=["POST"])
def req_last_response():
    response = openai_module.get_next_response(user_text="끝", is_last=True)
    result = json.dumps({"response": response, "is_last": True}, ensure_ascii=False, indent=4)
    result = make_response(result)
    return result
##===========================================================

if __name__ == "__main__":
    app.run(debug=True,
            host=host_addr,
            port=host_port)