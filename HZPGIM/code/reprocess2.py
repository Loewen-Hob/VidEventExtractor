import json


def split_arguments(event):
    recguid, eventname, eventdict = event
    max_length = max(len(v) if isinstance(v, list) else 1 for v in eventdict.values())

    split_events = []
    for i in range(max_length):
        new_eventdict = {}
        for key, value in eventdict.items():
            if isinstance(value, list):
                new_eventdict[key] = value[i] if i < len(value) else None
            else:
                new_eventdict[key] = value

        split_events.append([recguid + i, eventname, new_eventdict])
    return split_events


def process_event_list(event_list):
    split_event_list = []
    for event in event_list:
        split_event_list.extend(split_arguments(event))
    return split_event_list


def process_data(data):
    processed_data = []
    for entry in data:
        guid, details = entry
        if 'recguid_eventname_eventdict_list' in details:
            details['recguid_eventname_eventdict_list'] = process_event_list(
                details['recguid_eventname_eventdict_list'])
        processed_data.append([guid, details])
    return processed_data


def main(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    processed_data = process_data(data)

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(processed_data, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    files = ['train.json', 'dev.json', 'test.json']
    for file in files:
        input_file = f'E:\\bishe\\MNER\\HZPGIM\\{file}'
        output_file = f'E:\\bishe\\MNER\\HZPGIM\\output1\\{file}'
        main(input_file, output_file)
