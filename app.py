from flask import Flask, request, jsonify
from gpt.gpt import  GPTAssistant

app = Flask(__name__)

@app.route('/api/chat', methods=['POST'])
def stream_data():

    data = request.json
    return GPTAssistant().chat(data['msg'])

if __name__ == '__main__':
    app.run(debug=True)
