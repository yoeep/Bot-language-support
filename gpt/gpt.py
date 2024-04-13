# gpt.py

from dashscope import Generation
from datetime import datetime
import random


class GPTAssistant:
    def __init__(self, tools=None, system_info=None):
        if tools is None:
            from gpt import tool_factory
            self.tools = tool_factory.tools
            self.system_info = tool_factory.system_info
        else:
            self.tools = tools
            self.system_info = system_info
        with open('./gpt/gpt_key.init', 'r') as file:
            key = file.read()
        self.key = key

    def __get_response(self, messages):
        response = Generation.call(
            model='qwen-turbo',
            messages=messages,
            tools=self.tools,
            seed=random.randint(1, 10000),
            result_format='message',
            api_key='sk-'+self.key.strip()
        )
        return response

    def __call_handle(self, messages):
        assistant_output = self.__get_response(messages).output.choices[0].message
        if assistant_output.content == "":
            messages.append(assistant_output)
            import gpt.function_map as function_map
            func = getattr(function_map, assistant_output.tool_calls[0]['function']['name'])
            param = eval(assistant_output.tool_calls[0]['function']['arguments'])
            tool_info = {"name": assistant_output.tool_calls[0]['function']['name'], 'role': 'tool',
                         'content': func(**param)}
            messages.append(tool_info)
            return self.__call_handle(messages)
        else:
            return assistant_output

    def __call_with_messages(self, messages):
        messages = [self.system_info] + messages
        assistant_output = self.__call_handle(messages)
        return assistant_output['content']

    def chat(self, q):
        messages = [{
            "content": q,
            "role": "user"
        }]
        return self.__call_with_messages(messages)
if __name__ == '__main__':
    import tool_factory
    assistant = GPTAssistant(tool_factory.tools, tool_factory.system_info)
    print(assistant.chat("我要ting周杰伦"))
