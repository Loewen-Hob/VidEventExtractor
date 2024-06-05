import re

def extract_entities_from_output(model_output):
    # 正则表达式提取实体和标签
    pattern = r'\["(.*?)", "(.*?)"\]'
    matches = re.findall(pattern, model_output)

    # 构建实体字典
    entities = {}
    for match in matches:
        entity, label = match
        entities[entity] = label

    return entities, model_output

# 使用例子
model_output = '''
答：["2020年4月21日", "TIME"], ["雅漾官网", "INVOLVED_COMPANY"], ["雅漾舒泉调理喷雾", "PRODUCT_NAME"], ["vene Thermal", "PRODUCT_BRAND"]。
分析：这段文本提到了“2020年4月21日”作为时间，表示广告宣传活动从这一天开始。提及的“雅漾官网”代表发布广告的公司，属于涉事企业。广告宣传的产品“雅漾舒泉调理喷雾”明确了产品名称，而“vene Thermal”则是该品牌的名称。
'''

entities, original_text = extract_entities_from_output(model_output)
print("构建的实体字典：")
print(entities)
print("\n原文本：")
print(original_text)
