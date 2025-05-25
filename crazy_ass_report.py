#!/usr/bin/env python3

from llm_query import QueryChat
from config import *

num_people = len(peoples)

system_prompt = """
...
"""

query_prompt = f"""
这是报告模板：

1、会议纪要（主要记录会议的流程、内容、发言、讨论情况等）
（1）会议开场
主持人XXX同志宣布会议开始，介绍本次会议主题和学习目标：学习XXX。
（2）专题学习
第一部分：XXX
XXX同志带领大家学习XXX，重点包括：XXX。
第二部分：XXX
学习XXX。XXX同志详细解读XXX。
（3）集体讨论与发言
XXX：XXX。
XXX：XXX。
XXX：XXX。
XXX：XXX。
XXX：XXX。

主持人是{leader}，请你将以下内容分为{num_people}人份填写，这些人是：{peoples}。

{report_content}
"""

if __name__ == "__main__":
    if len(sys.argv) > 2 or len(sys.argv) < 1:
        print(f"Usage: {sys.argv[0]} <system prompt>")
        sys.exit(1)
    if len(sys.argv) == 2:
        system_prompt = sys.argv[1]
    else:
        pass
