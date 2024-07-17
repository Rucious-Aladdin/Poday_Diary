import time
from openai import OpenAI

class OpenAIConversationModule:
    def __init__(self, args, assitant_prompts, last_prompts, initial_question= "오늘 하루 어땠어요?", user_args=None):
        self.args = args
        
        self.init_args_config()
        self.user_args = user_args
        self.assitant_prompts = assitant_prompts
        self.last_prompts = last_prompts
        self.initial_question = initial_question
        self.client = self.create_client()
        self.assistant = self.create_assistant()
        self.thread = self.client.beta.threads.create()

        self.run = None
        self.conversations = []

    def init_args_config(self):
        if hasattr(self.args, "temperature"):
            self.args.temperature = float(self.args.temperature)
        else:
            self.args.temperature = .7
        
        if hasattr(self.args, "max_tokens"):
            self.args.max_tokens = int(self.args.max_tokens)
        else:
            self.args.max_tokens = 500
        
        if hasattr(self.args, "temperature"):
            self.args.top_p = float(self.args.top_p)
        else:
            self.args.top_p = .7

        if hasattr(self.args, "frequency_penalty"):
            self.args.frequency_penalty = int(self.args.frequency_penalty)
        else:
            self.args.frequency_penalty = 2
        
        if hasattr(self.args, "precense_penalty"):
            self.args.precense_penalty = int(self.args.precense_penalty)
        else:
            self.args.precense_penaltu = 1
        
    def create_client(self):
        client = OpenAI(api_key=self.args.api_key)
        return client

    def create_assistant(self):
        assistant = self.client.beta.assistants.create(
            name=self.args.name,
            instructions=self.assitant_prompts,
            model=self.args.model,
        )
        return assistant
    
    def create_run(self):
        run = self.client.beta.threads.runs.create(
            thread_id=self.thread.id,
            assistant_id=self.assistant.id
        )
        time.sleep(1)
        return run

    def set_initial_question(self):
        response = self.client.beta.threads.messages.create(
            thread_id=self.thread.id,
            role="assistant",
            content=self.initial_question
        )
        self.conversations.append("[BOT] " + self.initial_question)
        initial_message = response.content[0].text.value
        return initial_message

    def get_next_response(self, user_text="", is_last=False):
        if is_last:
            prompt = self.last_prompts
            for message in self.conversations:
                prompt += message + "\n"
        elif user_text is not None:
            prompt = user_text
        
        response = self.response_generate(prompt)
        last_message = response.data[0].content[0].text.value
        self.conversations.append("[USR] " + prompt)
        self.conversations.append("[BOT] " + last_message)
        return last_message

    def response_generate(self, prompt):
        self.client.beta.threads.messages.create(
            thread_id=self.thread.id,
            role="user",
            content=prompt
        )
        run = self.client.beta.threads.runs.create(
            thread_id=self.thread.id,
            assistant_id=self.assistant.id
        )        
        run = self.wait_on_run(self.thread.id, run.id)
        response = self.client.beta.threads.messages.list(thread_id=self.thread.id, limit=1)
        return response


    def wait_on_run(self, thread_id, run_id):
        run = self.client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run_id,
        )
        while run.status not in ["completed"]:
            time.sleep(0.3)
            run = self.client.beta.threads.runs.retrieve(
                thread_id=thread_id,
                run_id=run_id,
            )
        return run

    def get_conversations(self):
        return self.conversations