import re
import pandas as pd
import json


def load_data(filepath):
    data = pd.read_csv(filepath)
    data.fillna('', inplace=True)  # Replace NaN with empty string
    return data


def extract_entities_from_output(model_output):
    pattern = r'\["(.*?)", "(.*?)"\]'
    matches = re.findall(pattern, model_output)
    entities = {}
    for match in matches:
        entity, label = match
        if entity in entities:
            if label not in entities[entity]:
                entities[entity].append(label)
        else:
            entities[entity] = [label]
    return entities


def get_entity_positions(text, entity):
    positions = []
    start = 0
    while start < len(text):
        start = text.find(entity, start)
        if start == -1:
            break
        end = start + len(entity)
        positions.append((start, end))
        start = end
    return positions


def parse_segment_id(segment_id):
    parts = segment_id.split('_')
    start_seconds = int(parts[-4])
    start_microseconds = int(parts[-3])
    end_seconds = int(parts[-2])
    end_microseconds = int(parts[-1])
    return (start_seconds * 1000 + start_microseconds, end_seconds * 1000 + end_microseconds)


def generate_structure(data):
    result = []

    # Group by video ID and segment them
    grouped = data.groupby('原视频ID')

    for video_id, group in grouped:
        segments = []
        for _, row in group.iterrows():
            segment_id = row['视频分段后ID']
            start_time, end_time = parse_segment_id(segment_id)
            segments.append((start_time, end_time, row['合并去重文本'], row['LLM_output'], segment_id))

        # Sort segments by start time
        segments.sort(key=lambda x: x[0])

        # Split segments into separate videos based on time gaps
        split_videos = []
        current_video = [segments[0]]
        for i in range(1, len(segments)):
            if segments[i][0] - current_video[-1][1] > 2000:  # If time gap > 2 seconds, start a new video
                split_videos.append(current_video)
                current_video = [segments[i]]
            else:
                current_video.append(segments[i])
        split_videos.append(current_video)

        for video in split_videos:
            first_segment_id = video[0][4]
            combined_text = ' '.join([seg[2] for seg in video])
            combined_output = ' '.join([seg[3] for seg in video])
            entities = extract_entities_from_output(combined_output)

            sentences = [seg[2] for seg in video]
            sentence_boundaries = [0]
            current_length = 0
            for sentence in sentences:
                current_length += len(sentence)
                sentence_boundaries.append(current_length)

            ann_valid_mspans = []
            ann_valid_dranges = []
            ann_mspan2dranges = {}
            ann_mspan2guess_field = {}

            for entity, labels in entities.items():
                for label in labels:
                    positions = get_entity_positions(combined_text, entity)
                    ann_valid_mspans.append(entity)
                    for (start, end) in positions:
                        sentence_start_idx = 0
                        for i in range(len(sentence_boundaries) - 1):
                            if sentence_boundaries[i] <= start < sentence_boundaries[i + 1]:
                                sentence_start_idx = i
                                break

                        relative_start = start - sentence_boundaries[sentence_start_idx]
                        relative_end = end - sentence_boundaries[sentence_start_idx]
                        drange = [sentence_start_idx, relative_start, relative_end]

                        ann_valid_dranges.append(drange)

                        if entity not in ann_mspan2dranges:
                            ann_mspan2dranges[entity] = []
                        ann_mspan2dranges[entity].append(drange)

                        ann_mspan2guess_field[entity] = label

            result.append([
                first_segment_id,
                {
                    "sentences": sentences,
                    "ann_valid_mspans": ann_valid_mspans,
                    "ann_valid_dranges": ann_valid_dranges,
                    "ann_mspan2dranges": ann_mspan2dranges,
                    "ann_mspan2guess_field": ann_mspan2guess_field
                }
            ])

    return result

def save_to_json(data, filepath):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# 路径可能需要根据您的文件存放位置进行调整
filepath = 'E:\\bishe\MNER\HZPGIM\\NC\\all_merge_NC_LLM_output.csv'
output_path = 'E:\\bishe\MNER\HZPGIM\\NC\\converted_data.json'

data = load_data(filepath)
structured_data = generate_structure(data)
save_to_json(structured_data, output_path)
