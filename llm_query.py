#!/usr/bin/env python3

import os
import sys
import json
import atexit
import configparser
from typing import Dict, Optional, List
from openai import OpenAI

CUR_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG = os.path.join(CUR_DIR, "config.ini")
PLATFORM = "DeepSeek"


def load_config(field: str, value: str) -> str:
    config = configparser.ConfigParser()
    config.read(CONFIG)
    return config[field][value]


"""
An simple example from DeepSeek:

# Please install OpenAI SDK first: `pip3 install openai`

from openai import OpenAI

client = OpenAI(api_key="<DeepSeek API Key>", base_url="https://api.deepseek.com")

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "Hello"},
    ],
    stream=False
)

print(response.choices[0].message.content)
"""


class QueryChat:
    """Interface for interacting with LLM"""

    def __init__(self) -> None:
        self.chat_context: List[Dict[str, str]] = []
        self.chat_history: List[Dict[str, str]] = []
        self.temperature: float = 0.2
        self.use_history = False
        self.system_prompt: Optional[str] = None
        atexit.register(self.log_history)

    def clear(self):
        self.chat_context = []

    def set_history(self, open: bool) -> None:
        self.use_history = open

    def insert_system_prompt(self, system_prompt: str) -> None:
        """add system_prompt in self.chat_context"""

        if self.chat_context and self.chat_context[0]["role"] == "system":
            self.chat_context[0]["content"] = system_prompt
        else:
            self.chat_context.insert(
                0, {"role": "system", "content": system_prompt})

    def log_history(self, log_file: str = "chat_log.json"):
        if not os.path.exists(log_file):
            with open(log_file, "w") as w:
                json.dump([], w, indent=4)

        with open(log_file, "r") as r:
            log = json.load(r)
        assert isinstance(log, list)
        log.append(self.chat_history)
        with open(log_file, "w") as w:
            json.dump(log, w, indent=4)

    def __query(self, prompt: str, model: str) -> Optional[str]:
        self.chat_context.append({"role": "user", "content": prompt})
        self.chat_history.append({"role": "user", "content": prompt})

        client = OpenAI(
            api_key=load_config(PLATFORM, "api_key"),
            base_url=load_config(PLATFORM, "api_base"),
        )
        response = client.chat.completions.create(
            messages=self.chat_context,  # type: ignore
            model=model,
            temperature=self.temperature,
        )
        response_content = str(response.choices[0].message.content)

        self.chat_context.append(
            {"role": "assistant", "content": response_content})
        self.chat_history.append(
            {"role": "assistant", "content": response_content})

        return response_content

    def query(
        self, prompt: str, *, model: str = load_config(PLATFORM, "model")
    ) -> Optional[str]:

        response = self.__query(prompt, model)
        if not self.use_history:
            self.clear()
        return response


if __name__ == "__main__":
    if len(sys.argv) > 2 or len(sys.argv) < 1:
        print(f"Usage: {sys.argv[0]} <system prompt>")
        sys.exit(1)
    if len(sys.argv) == 2:
        system_prompt = sys.argv[1]
    else:
        system_prompt = "You are a helpful assistant"
    # 创建查询LLM的实例
    q = QueryChat()
    q.insert_system_prompt(system_prompt)
    # 获取查询结果
    print("Give me your prompt: ")
    user_prompt = input()
    response = q.query(user_prompt)
    # 输出结果
    assert isinstance(response, str)
    print(f"response: {response}")
