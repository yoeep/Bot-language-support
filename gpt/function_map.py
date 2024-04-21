from flask import Flask, request, jsonify
import requests
def callback_support(callback_info, request_body):
    if callback_info:
        url = callback_info.get('url')
        body = callback_info.get('body')
        headers = callback_info.get('header')

        if url:
            print(f"{url},{body}, {headers}")
            timeout = (5, 10)
            body.update(request_body)
            print(body)
            response = requests.post(url, json=body, headers=headers, timeout=timeout)
            print(response.text)
            return response.text


def sing_voice(sing, user_id, callback_info):
    request_body = {
        "user_id": user_id,
        "sing_name": sing
    }
    return callback_support(callback_info, request_body)