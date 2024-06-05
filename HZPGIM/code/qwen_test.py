# For prerequisites running the following sample, visit https://help.aliyun.com/document_detail/611472.html

import dashscope
import json
dashscope_api_key = 'sk-f3e26d9a7f1e4494b3302f03a2ec10eb'
import pandas as pd
from http import HTTPStatus


def call_with_messages(text):
    dashscope.api_key = 'sk-f3e26d9a7f1e4494b3302f03a2ec10eb'
    text = str(text)
    prompt_before = '''
        请假设你是一个NLP算法工程师，负责完成一个命名实体识别任务。你将得到一些文本，需要从中识别并标注出以下实体类别：
        - 时间
        - 地点
        - 罚款金额
        - 禁用产品名称
        - 禁用产品类别
        - 禁用产品品牌
        - 生产厂商
        - 销售厂商
        - 禁用物质
        - 检验机构
        你的任务是输出一个字典，其中键为实体类别，值为识别出的实体。确保格式清晰且准确。
        请注意！！！你的回复我将用于json读取后用于二次处理，所以一定一定一定不要输出多余的内容！！！
        例如，"请分析这段文本和对应的图片描述并完成实体识别的任务。\n图片的名称是：虚假宣传1_segment_0_00_0_60_keyframe.jpg\n这段文本的事件类型是：虚假宣传。\n这是需要分析的文本，第一个标点符号前的文本是图片对应视频ASR识别出来的文本，之后是OCR识别出来的文本：‘香奈儿也玩虚假宣传 ’。\n这是对应图片的英文描述：‘arafed man in a suit and tie sitting at a table with a sign that says,’。\n这是对应图片的中文描述：‘穿着西装和领带的阿拉法特男子坐在一张桌子旁 ， 上面有一个标语 ， 上面写着 ，’。\n这是需要检测出来的实体类型：时间，地点，涉及金额，监管机构，产品名称，产品类别，产品品牌。"
        返回：
        {"产品品牌": "香奈儿"}
        请处理以下句子：
        '''
    prompt = prompt_before + text
    messages = [{'role': 'system', 'content': 'You are a helpful assistant.'},
                {'role': 'user', 'content': prompt}]

    response = dashscope.Generation.call(
        dashscope.Generation.Models.qwen_plus,
        messages=messages,
        result_format='message',  # set the result to be "message" format.
    )
    if response.status_code == HTTPStatus.OK:
        result = json.loads(response.output.choices[0].message.content)
        return result
    else:
        print('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
            response.request_id, response.status_code,
            response.code, response.message
        ))

text = '"请分析这段文本和对应的图片描述并完成实体识别的任务。\n图片的名称是：虚假宣传30_segment_76_90_78_10_keyframe.jpg\n这段文本的事件类型是：虚假宣传。\n这是需要分析的文本，第一个标点符号前的文本是图片对应视频ASR识别出来的文本，之后是OCR识别出来的文本：‘这么大的店。 像哈药生物这么大的店 快 ’。\n这是对应图片的英文描述：‘arafed woman in a white lab coat standing in front of a counter’。\n这是对应图片的中文描述：‘穿着白色实验室外套的阿拉法特妇女站在柜台前’。\n这是需要检测出来的实体类型：时间，地点，涉及金额，监管机构，产品名称，产品类别，产品品牌。"'

print(call_with_messages(text))