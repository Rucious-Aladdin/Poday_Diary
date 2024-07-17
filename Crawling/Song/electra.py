import torch
from util import int2emo
from transformers import AutoTokenizer, AutoModelForSequenceClassification

class ElectraSentimentClassifier:
    def __init__(self):
        self.model_name = "blue2959/koelectra-base-v3-discriminator-finetuned-kor-8-emotions_v1.4"
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(self.model_name).to(self.device)

    def predict_sentiment(self, conversation):
        inputs = self.tokenizer(conversation, return_tensors="pt", padding=True, truncation=True, max_length=512).to(self.device)
        with torch.no_grad():
            outputs = self.model(**inputs)
        logits = outputs.logits
        predictions = torch.argmax(logits, dim=-1).item()
        probabilities = torch.nn.functional.softmax(logits, dim=-1)[0].tolist()
        self.print_result(conversation, probabilities, predictions)

        return predictions, probabilities  # Ensure int2emo[predictions] is returned correctly

    def ready_model(self):
        self.model.to(self.device)
    
    def unload_model(self):
        self.model.cpu()
        torch.cuda.empty_cache()
        del self.model
        self.model = None

    def print_result(self, sentence, probabilities, predictions):
        # 터미널에 출력
        print("==== Model Prediction ====")
        print(f"Input Sentence: {sentence}")
        print("Probabilities:")
        for i, prob in enumerate(probabilities):
            print(f"  {int2emo[i]}: {prob * 100:.1f}%")
        predicted_label = int2emo[predictions]  # Add this line to define predicted_label
        print(f"Predicted Label: {predicted_label} ({predictions})")
        print("==========================")
