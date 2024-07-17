import torch
from util import *
from transformers import AutoTokenizer, AutoModelForSequenceClassification

class ElectraSentimentClassifier:
    def __init__(self):
        self.model_name = "blue2959/koelectra-base-v3-discriminator-finetuned-kor-8-emotions_v1.4"
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(self.model_name, output_hidden_states=True).to(self.device)

    def predict_sentiment(self, conversation):
        conversation = preprocess_text(conversation)
        print("preprocessed: %s" % conversation)
        inputs = self.tokenizer(conversation, return_tensors="pt", padding=True, truncation=True, max_length=512).to(self.device)
        tokens = self.tokenizer.convert_ids_to_tokens(inputs['input_ids'][0])
        with torch.no_grad():
            outputs = self.model(**inputs)
        logits = outputs.logits
        hidden_state = outputs.hidden_states[-1]
        predictions = torch.argmax(logits, dim=-1).item()
        probabilities = torch.nn.functional.softmax(logits, dim=-1)[0].tolist()
        self.print_result(conversation, probabilities, predictions, tokens)

        return predictions, probabilities, hidden_state[0][0].cpu().tolist()

    def ready_model(self):
        self.model.to(self.device)
    
    def unload_model(self):
        self.model.cpu()
        torch.cuda.empty_cache()
        del self.model
        self.model = None

    def print_result(self, sentence, probabilities, predictions, tokens):
        # 터미널에 출력
        print("==== Model Prediction ====")
        print(f"Input Sentence: {sentence}")
        print("Tokens:")
        print(tokens)
        print("Probabilities:")
        for i, prob in enumerate(probabilities):
            print(f"  {int2emo[i]}: {prob * 100:.1f}%")
        predicted_label = int2emo[predictions]
        print(f"Predicted Label: {predicted_label} ({predictions})")
        print("==========================")
        print()
