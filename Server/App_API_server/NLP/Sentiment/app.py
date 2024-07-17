from electra import ElectraSentimentClassifier
from util import int2emo, preprocess_text
from flask import Flask, request, jsonify, make_response
import json

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
host_addr = "0.0.0.0"
host_port = 5000
model = None

@app.route('/sentiment')
def sentiment_ready(): # 유저 대화 시작시 model을 gpu에 올리고 대기.
    global model
    model = ElectraSentimentClassifier()
    model.ready_model()
    return jsonify(state="model is ready(gpu).")

@app.route('/sentiment/predict', methods=['POST'])
def sentiment():
    global model
    data = request.json
    conversation = data.get('conversation', 'error:no conversation')
    last_Flag = data.get("islast", "false")
    
    if (model is None) or (str(model.device) != "cuda"):
        model = ElectraSentimentClassifier()
        model.ready_model()
    
    if conversation == "error:no conversation":
        probabilities = [0 for i in range(len(int2emo))]
        probabilities[-1] = 1.0
        result = json.dumps({
            "emotion": "중립", 
            "probabilities": probabilities, 
            "emo_dict": int2emo, 
            "last_vector":[0.0 for _ in range(768)]}, 
            ensure_ascii=False, indent=4)
        res = make_response(result)
        res.mimetype = 'application/json'
        return res  # 에러발생시 중립을 리턴
    else:
        emotion, probabilities, context_vector = model.predict_sentiment(conversation)  # int로 받아옴

    if last_Flag == "true":  # 마지막 대화일시 감정분석 중단후 메모리 해제
        model.unload_model()
        model = None
    result = json.dumps({"emotion": int2emo[emotion], "probabilities": probabilities, "context_vector": context_vector, "emo_dict": int2emo}, ensure_ascii=False, indent=4)
    res = make_response(result)
    res.mimetype = 'application/json'
    return res # 감정을 리턴


if __name__ == "__main__":
    app.run(debug=True,
            host=host_addr,
            port=host_port)