import torch
from transformers import XLMRobertaTokenizer, XLMRobertaForSequenceClassification

def label_int2str(label):
    emo2int = {
        "기쁨": 0, "당황": 1, "분노": 2,
        "불안": 3, "상처": 4, "슬픔": 5,
        "중립": 6
    }
    int2emo = {v: k for k, v in emo2int.items()}
    return int2emo[label]

def get_emotions():
    return ["기쁨", "당황", "분노", "불안", "상처", "슬픔", "중립"]

# 모델과 토크나이저 로드
model_name = "blue2959/xlm-roberta-base-finetuned-kor-8-emotions_v1.0"
tokenizer = XLMRobertaTokenizer.from_pretrained(model_name)
model = XLMRobertaForSequenceClassification.from_pretrained(model_name)

# GPU 사용 설정
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

def predict(sentence):
    # 입력 텐서로 변환
    inputs = tokenizer(sentence, return_tensors="pt").to(device)

    # 모델 예측
    with torch.no_grad():
        outputs = model(**inputs)

    # 예측 결과 출력
    logits = outputs.logits
    probabilities = torch.nn.functional.softmax(logits, dim=-1)[0]
    predictions = torch.argmax(probabilities, dim=-1).item()
    predicted_label = label_int2str(predictions)

    # 결과를 JSON 형식으로 반환
    emotions = get_emotions()
    result = {
        "input_sentence": sentence,
        "probabilities": {emotions[i]: f"{prob.item() * 100:.1f}%" for i, prob in enumerate(probabilities)},
        "predicted_label": predicted_label
    }

    # 터미널에 출력
    print("==== Model Prediction ====")
    print(f"Input Sentence: {sentence}")
    print("Probabilities:")
    for i, prob in enumerate(probabilities):
        print(f"  {emotions[i]}: {prob.item() * 100:.1f}%")
    print(f"Predicted Label: {predicted_label} ({predictions})")
    print("==========================")

    return result

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        sentence = sys.argv[1]
    else:
        sentence = "This is a test sentence."

    predict(sentence)

