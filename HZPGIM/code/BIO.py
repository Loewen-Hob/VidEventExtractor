import re
import pandas as pd
import numpy as np
import random


def load_and_process_data(filepath):
    # Load data
    data = pd.read_csv(filepath, usecols=['合并去重文本', 'LLM_output'])

    # Handle missing values
    data.fillna('', inplace=True)  # Replace NaN with empty string

    # Process each row of data and generate BIO tagging
    processed_data = []
    for index, row in data.iterrows():
        # Ensure the text and model_output are strings
        text = str(row['合并去重文本'])
        model_output = str(row['LLM_output'])
        formatted_output = format_bio_output(text, model_output)
        processed_data.append(formatted_output)

    return processed_data


def split_and_save_data(processed_data, train_ratio=0.7, valid_ratio=0.15):
    # Shuffle the data randomly
    random.shuffle(processed_data)

    # Determine the size of each part
    total_size = len(processed_data)
    train_size = int(total_size * train_ratio)
    valid_size = int(total_size * valid_ratio)

    # Split the dataset
    train_data = processed_data[:train_size]
    valid_data = processed_data[train_size:train_size + valid_size]
    test_data = processed_data[train_size + valid_size:]

    # Save data to files
    with open("../CO/train.txt", "w", encoding="utf-8") as f_train:
        f_train.write("\n\n".join(train_data))
    with open("../CO/valid.txt", "w", encoding="utf-8") as f_valid:
        f_valid.write("\n\n".join(valid_data))
    with open("../CO/test.txt", "w", encoding="utf-8") as f_test:
        f_test.write("\n\n".join(test_data))


def extract_entities_from_output(model_output):
    pattern = r'\["(.*?)", "(.*?)"\]'
    matches = re.findall(pattern, model_output)

    entities = {}
    for match in matches:
        entity, label = match
        entities[entity] = label
    return entities

def bio_tadgging(entities, text):
    sorted_entities = sorted(entities.items(), key=lambda x: len(x[0]), reverse=True)
    tokens = list(text)
    labels = ['O'] * len(tokens)
    marked = [False] * len(tokens)
    for entity, label in sorted_entities:
        start_idx = [m.start() for m in re.finditer(re.escape(entity), text)]
        for idx in start_idx:
            if all(not marked[idx + i] for i in range(len(entity))):
                labels[idx] = f'B-{label}'
                marked[idx] = True
                for i in range(1, len(entity)):
                    labels[idx + i] = f'I-{label}'
                    marked[idx + i] = True

    tagged_result = [(token, label) for token, label in zip(tokens, labels)]
    return tagged_result

def bio_tagging(entities, text):
    sorted_entities = sorted(entities.items(), key=lambda x: len(x[0]), reverse=True)
    tokens = list(text)
    labels = ['O'] * len(tokens)
    marked = [False] * len(tokens)
    for entity, label in sorted_entities:
        start_idx = [m.start() for m in re.finditer(re.escape(entity), text)]
        for idx in start_idx:
            if all(not marked[idx + i] for i in range(len(entity))):
                labels[idx] = f'B-{label}'
                marked[idx] = True
                for i in range(1, len(entity)):
                    labels[idx + i] = f'I-{label}'
                    marked[idx + i] = True
    return tokens, labels

def format_bio_output(text, model_output):
    # 提取实体和标签
    entities = extract_entities_from_output(model_output)

    # 获取 BIO 标注结果
    tokens, labels = bio_tagging(entities, text)

    # 构建输出格式
    result = []
    for token, label in zip(tokens, labels):
        result.append(f"{token}\t{label}")
    result.append("<EOS>\tX")
    tokens = list(model_output)
    for token in tokens:
        result.append(f"{token}\tX")
    return "\n".join(result)

# 路径可能需要根据您的文件存放位置进行调整
filepath = 'E:\\bishe\MNER\HZPGIM\CO\co_llm_output.csv'
processed_data = load_and_process_data(filepath)
split_and_save_data(processed_data)