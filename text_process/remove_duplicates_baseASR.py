import os
from tqdm import tqdm
def extract_text_from_srt(srt_file_path):
    # 异常捕获，防止文件不存在
    try:        
        with open(srt_file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        text_lines = []
        for line in lines:
            if line.strip() and not line.strip().isdigit() and '-->' not in line:
                text_lines.append(line)
        return text_lines
    except FileNotFoundError:
        print(f"File not found: {srt_file_path}")
        return []

def merge_and_remove_duplicates(txt_file_path, srt_text_lines):
    try:
        with open(txt_file_path, 'r', encoding='utf-8') as file:
            txt_lines = file.readlines()
    except FileNotFoundError:
        txt_lines = []

    all_lines = srt_text_lines + txt_lines
    seen = set()
    unique_lines = []
    for line in all_lines:
        words = line.strip().split()
        unique_words = []
        for word in words:
            if word.lower() not in seen:
                seen.add(word.lower())
                unique_words.append(word)
        if unique_words:
            unique_lines.append(" ".join(unique_words) + " ")
    return unique_lines

def write_output(output_file_path, lines):
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.writelines(lines)

def process_folders(input_txt_base_folder, input_srt_base_folder, output_base_folder):
    # 首先，计算总的文件数量
    total_files = sum([len(files) for _, _, files in os.walk(input_srt_base_folder) if any(file.endswith('.srt') for file in files)])
    
    # 使用 tqdm 创建一个进度条
    pbar = tqdm(total=total_files, desc="Processing files")
    
    for subdir, _, files in os.walk(input_srt_base_folder):
        for file in files:
            srt_file_path = os.path.join(subdir, file)
            txt_file_name = file.replace('.srt', '.txt')
            txt_subdir = subdir.replace("ASR", "OCR")
            txt_file_path = os.path.join(txt_subdir, txt_file_name)
            output_file_path = os.path.join(output_base_folder, os.path.relpath(subdir, input_srt_base_folder), txt_file_name)
            
            srt_text_lines = extract_text_from_srt(srt_file_path)
            unique_lines = merge_and_remove_duplicates(txt_file_path, srt_text_lines)
            write_output(output_file_path, unique_lines)
            
            # 更新进度条
            pbar.update(1)
    
    # 关闭进度条
    pbar.close()
# 请根据你的文件夹路径进行修改
input_txt_base_folder = '/root/bishe/end_output/虚假宣传/OCR'
input_srt_base_folder = '/root/bishe/end_output/虚假宣传/ASR'
output_base_folder = '/root/bishe/end_output/虚假宣传/merged'
process_folders(input_txt_base_folder, input_srt_base_folder, output_base_folder)
