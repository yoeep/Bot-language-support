import random
from http import HTTPStatus
import dashscope
import json

from tools import tools
from tools import system_info


def call_with_messages():
    messages = [system_info,{'role': 'user', 'content': '我想点一首龙卷风送给我自己'}]
    response = dashscope.Generation.call(
        dashscope.Generation.Models.qwen_turbo,
        messages=messages,
        tools=tools,
        seed=random.randint(1, 10000),  # set the random seed, optional, default to 1234 if not set
        result_format='message',  # set the result to be "message" format.
        api_key='sk-1c428da2a6d14bf6b3f5eaed88c07197'
    )
    if response.status_code == HTTPStatus.OK:
        run_task(response.output.choices[0].message, "")
    else:
        print('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
            response.request_id, response.status_code,
            response.code, response.message
        ))

def run_task(model_response, model_history):
    print(model_response)
    if model_response.content == "":
        import function_map
        func = getattr(function_map, model_response.tool_calls[0].get("function").get("name"))
        param = eval(model_response.tool_calls[0].get("function").get("arguments"))
        print(param)
        func_response = func(**param)
        result = json.dumps(func_response, ensure_ascii=False)
        print(result)
        messages = [system_info,{"content": "我想点一首龙卷风送给我自己","role": "user"},
            {
                "role": "assistant",
                "content": "",
                "tool_calls": [
                    {
                        "function": {
                            "name": "sing_voice",
                            "arguments": "{\"sing\": \"\"}"
                        },
                        "id": "",
                        "type": "function"
                    }
                ]
            },
            {
                "content": result,
                "name": "sing_voice",
                "role": "tool"
            }
        ]
        response = dashscope.Generation.call(
            dashscope.Generation.Models.qwen_turbo,
            messages=messages,
            tools=tools,
            seed=random.randint(1, 10000),
            result_format='message',
            api_key='sk-1c428da2a6d14bf6b3f5eaed88c07197'
        )
        print(response)
        run_task(response.output.choices[0].message, "")
    else:
        return model_response, model_history
if __name__ == '__main__':
    call_with_messages()