import re


def extract_entities_from_output(model_output):
    pattern = r'\["(.*?)", "(.*?)"\]'
    matches = re.findall(pattern, model_output)
    entities = {}
    for match in matches:
        entities[match[0]] = match[1]
    return entities


def bio_tag_text(text, entities):
    tokens = text.split()
    labels = ['O'] * len(tokens)
    sorted_entities = sorted(entities.items(), key=lambda x: len(x[0]), reverse=True)

    for entity, tag in sorted_entities:
        entity_tokens = entity.split()
        length = len(entity_tokens)

        for i in range(len(tokens)):
            if tokens[i:i + length] == entity_tokens:
                labels[i] = f'B-{tag}'
                for j in range(1, length):
                    labels[i + j] = f'I-{tag}'

    return tokens, labels


def write_to_train_txt(tokens, labels, filename='train.txt'):
    with open(filename, 'w') as file:
        for token, label in zip(tokens, labels):
            file.write(f'{token}\t{label}\n')
        file.write('<EOS>\tX\n')
        file.write('Named entities:1.\tX\n')
        # You can add more structured reasoning or any other content here as required


# Sample model_output and text to be processed
model_output = '''
["2020年4月21日", "TIME"], ["雅漾官网", "INVOLVED_COMPANY"], ["雅漾舒泉调理喷雾", "PRODUCT_NAME"], ["vene Thermal", "PRODUCT_BRAND"]。
'''
text = "出效果却不能提供依据证明被认定为虚假宣称功效二人。却不能提供依据证明,被认定为虚假宣称功效。判决书显示,自2020年4月21日始,雅漾官网宣称“维护并加强激光/光子美容手术效果上发布广告宣传经营的产品 “雅漾舒泉调理喷雾” vene Thermal ”,"

entities = extract_entities_from_output(model_output)
tokens, labels = bio_tag_text(text, entities)
write_to_train_txt(tokens, labels)
