from flask import Flask, request, jsonify
import roberta

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    sentence = data.get('sentence', '')
    result = roberta.predict(sentence)
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

