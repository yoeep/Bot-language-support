# gpt.py

from dashscope import Generation
import random
from utils import logUtils as logger


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

    def __call_handle(self, messages, callback_info=None):
        assistant_output = self.__get_response(messages).output.choices[0].message
        if assistant_output.content == "":
            messages.append(assistant_output)
            from gpt import function_map
            func = getattr(function_map, assistant_output.tool_calls[0]['function']['name'])
            param = eval(assistant_output.tool_calls[0]['function']['arguments'])
            logger.info(f'function : {func}, parameter : {param}')
            if callback_info :
                param['callback_info'] = callback_info
            tool_info = {"name": assistant_output.tool_calls[0]['function']['name'], 'role': 'tool',
                         'content': func(**param)}
            messages.append(tool_info)
            return self.__call_handle(messages)
        else:
            return assistant_output

    def __call_with_messages(self, messages,callback_info=None):
        messages = [self.system_info] + messages
        assistant_output = self.__call_handle(messages, callback_info)
        return assistant_output['content']

    def chat(self, q):
        try:
            messages = [{
                "content": q,
                "role": "user"
            }]
            return self.__call_with_messages(messages)
        except Exception as e:
            print("Error:", e)
            return "GPT出错了!"
    def chat_with_callback(self, q, callback_info):
        try:
            messages = [{
                "content": q,
                "role": "user"
            }]
            return self.__call_with_messages(messages, callback_info)
        except Exception as e:
            print("Error:", e)
            return "GPT出错了!"
if __name__ == '__main__':
    import tool_factory
    assistant = GPTAssistant(tool_factory.tools, tool_factory.system_info)
    print(assistant.chat("我要ting周杰伦"))
