from chatbot import OpenAIConversationModule
from util import *

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

module = OpenAIConversationModule(args, assitant_prompts)
response = module.set_initial_question()
print(response)

is_last = False
while not is_last:
    user_text=input()
    if user_text == "끝":
        is_last=True    
    response = module.get_next_response(user_text, is_last)
    print(response)