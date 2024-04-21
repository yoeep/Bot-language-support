from flask import Flask, request, jsonify
import requests
def callback_support(callback_info):
    if callback_info:
        url = callback_info.get('url')
        body = callback_info.get('body')
        headers = callback_info.get('header')

        if url:
            print(f"{url},{body}, {headers}")
            response = requests.post(url, json=body, headers=headers)
            return jsonify(response.json()), response.status_code


def sing_voice(sing, user_id, callback_info):
    callback_support(callback_info)
    print(f"{user_id} order {sing}")
    return "已经在你的频道做播放"