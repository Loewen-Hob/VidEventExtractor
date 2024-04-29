def remove_OCR(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    new_lines = []
    for line in lines:
        # 查找标点符号的位置
        period_idx = line.find('。')
        exclamation_idx = line.find('！')
        question_idx = line.find('？')

        # 确定最早出现的标点符号位置
        indices = [idx for idx in [period_idx, exclamation_idx, question_idx] if idx != -1]
        if indices:
            cut_off_idx = min(indices) + 1  # 包括标点本身
            new_lines.append(line[:cut_off_idx].strip())
        else:
            new_lines.append(line.strip())

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(new_lines))   

    print('{} OCR removed.'.format(file_path))


if __name__ == '__main__':
    import os
    raw_file_path = '/root/bishe/end_output/虚假宣传/ASR copy'
    for file_name in os.listdir(raw_file_path):
        file_path = os.path.join(raw_file_path, file_name)
        if os.path.isdir(file_path):  # 确保file_path是一个目录
            for file in os.listdir(file_path):
                full_file_path = os.path.join(file_path, file)
                remove_OCR(full_file_path)