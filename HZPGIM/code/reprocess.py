import json

def preprocess_sentence(sentence):
    """
    预处理句子，去除多余空格和不可见字符
    """
    return sentence.strip()

def find_span_indices(sentence, span):
    """
    在句子中找到 span 的起始和结束索引
    """
    start_idx = sentence.find(span)
    if start_idx == -1:
        return None, None
    end_idx = start_idx + len(span)
    return start_idx, end_idx

def reannotate_data(data):
    """
    重新标注数据，并删除recguid_eventname_eventdict_list为空的条目
    """
    reannotated_data = []

    for entry in data:
        guid, details = entry

        # 跳过recguid_eventname_eventdict_list为空的条目
        if not details['recguid_eventname_eventdict_list']:
            continue

        sentences = [preprocess_sentence(sent) for sent in details['sentences']]
        ann_valid_mspans = sorted(set(details['ann_valid_mspans']), key=lambda x: -len(x))  # 按长度排序，长的优先
        marked_positions = set()

        ann_valid_dranges = []
        ann_mspan2dranges = {}
        for span in ann_valid_mspans:
            span_ranges = []
            for sent_idx, sentence in enumerate(sentences):
                start_idx, end_idx = find_span_indices(sentence, span)
                if start_idx is not None:
                    # 检查是否已经被标注
                    if any(pos in marked_positions for pos in range(start_idx, end_idx)):
                        continue
                    span_ranges.append([sent_idx, start_idx, end_idx])
                    ann_valid_dranges.append([sent_idx, start_idx, end_idx])
                    # 标记位置为已标注
                    for pos in range(start_idx, end_idx):
                        marked_positions.add(pos)
            if span_ranges:
                ann_mspan2dranges[span] = span_ranges

        reannotated_entry = [
            guid,
            {
                "sentences": sentences,
                "ann_valid_mspans": [span for span in ann_valid_mspans if span in ann_mspan2dranges],
                "ann_valid_dranges": ann_valid_dranges,
                "ann_mspan2dranges": ann_mspan2dranges,
                **{k: v for k, v in details.items() if k not in ["sentences", "ann_valid_mspans", "ann_valid_dranges", "ann_mspan2dranges"]}
            }
        ]
        reannotated_data.append(reannotated_entry)

    return reannotated_data

def main(input_file, output_file):
    # 读取原始 JSON 数据
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 重新标注数据并过滤
    reannotated_data = reannotate_data(data)

    # 写回新的 JSON 文件
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(reannotated_data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    input_file = 'E:\\bishe\\MNER\\HZPGIM\\train.json'
    output_file = 'E:\\bishe\\MNER\\HZPGIM\\output\\train.json'
    main(input_file, output_file)
    input_file = 'E:\\bishe\\MNER\\HZPGIM\\dev.json'
    output_file = 'E:\\bishe\\MNER\\HZPGIM\\output\\dev.json'
    main(input_file, output_file)
    input_file = 'E:\\bishe\\MNER\\HZPGIM\\test.json'
    output_file = 'E:\\bishe\\MNER\\HZPGIM\\output\\test.json'
    main(input_file, output_file)
