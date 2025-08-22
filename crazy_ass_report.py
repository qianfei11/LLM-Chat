#!/usr/bin/env python3

import sys
from llm_query import QueryChat
from config import *

num_people = len(peoples)

system_prompt = """
请帮我生成一份党小组会议报告，模板如下：

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
"""

query_prompt = f"""
本次党小组会议的主题是：{report_topic}

主持人是{leader}，参会人员有：{peoples}，请你将以下报告内容按照参会人员分成{num_people}份发言（每个人的发言字数在100-200字之间），并根据模板输出对应的党小组会议报告。

{report_content}
"""

if __name__ == "__main__":
    if len(sys.argv) == 1:
        q = QueryChat()
        q.insert_system_prompt(system_prompt)
        response = q.query(query_prompt)
        assert isinstance(response, str)
        print(f"response: {response}")
    else:
        print(f"Usage: {sys.argv[0]} <system prompt>")
        sys.exit(-1)
