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
        例如，对于句子：“在2023年3月，北京一工厂因使用禁用化学品被罚款5000元。”，你应该返回：
        {
          "时间": "2023年3月",
          "地点": "北京",
          "罚款金额": "5000元",
          "禁用物质": "禁用化学品"
        } 
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

def process_annotations(df, text_column):
    for entity in ["时间", "地点", "罚款金额", "禁用产品名称", "禁用产品类别", "禁用产品品牌", "生产厂商", "销售厂商",
                   "禁用物质", "检验机构"]:
        df[entity] = df[text_column].apply(lambda x: call_with_messages(x).get(entity, ''))
        df[entity] = df[entity].apply(lambda items: '_'.join(items) if isinstance(items, list) else items)

def main():
    file_path = '禁用禁止第一批/processed_videos_info.xlsx'
    df = pd.read_excel(file_path)
    process_annotations(df, '合并去重文本')
    df.to_excel('annotated_output.xlsx', index=False)

if __name__ == '__main__':
    main()