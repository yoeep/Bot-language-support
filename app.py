from flask import Flask, request, jsonify
import requests
from gpt import  GPTAssistant

app = Flask(__name__)

@app.route('/api/chat', methods=['POST'])
def stream_data():

    data = request.json
    return GPTAssistant().chat(data['msg'])
@app.route('/api/chat_with_callback', methods=['POST'])
def handle_request():
    data = request.json
    return GPTAssistant().chat_with_callback(data['msg'], data['callback'])

if __name__ == '__main__':
    print(GPTAssistant().chat("2435654:我要点一首歌"))
    app.run(debug=False, host='0.0.0.0', port=5000)
