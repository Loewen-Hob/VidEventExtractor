import json


def count_sentences(input_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    sentence_count = sum(len(entry[1]['sentences']) for entry in data)
    return sentence_count


def main():
    files = {
        'train': 'E:\\bishe\\MNER\\HZPGIM\\output\\train.json',
        'dev': 'E:\\bishe\\MNER\\HZPGIM\\output\\dev.json',
        'test': 'E:\\bishe\\MNER\\HZPGIM\\output\\test.json'
    }

    for key, file_path in files.items():
        count = count_sentences(file_path)
        print(f"The number of sentences in {key} file: {count}")


if __name__ == "__main__":
    main()
