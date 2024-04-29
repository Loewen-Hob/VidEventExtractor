import os
import re
import pandas as pd
from tqdm import tqdm
import openpyxl
# 目录结构基路径
base_path = '/root/bishe/end_output/虚假宣传/'  # 使用你的根目录路径

excel_path = '/root/bishe/end_output/虚假宣传/videos_info.xlsx'  # 输出文件路径
# 初始化一个空的DataFrame，用于存储所有信息
df_columns = ['虚假宣传/序号', '原视频ID', '视频分段后ID', 'ASR', 'OCR', '合并去重文本', '时间', '地点', '不符合规定产品名称', '不符合规定产品类别', '不符合规定品牌', '生产厂商', '不符合规定原因', '检验机构']
df = pd.DataFrame(columns=df_columns)

# 指定需要遍历的目录
folders_to_check = ['ASR', 'OCR', 'merged']
folder_path = os.path.join(base_path, 'ASR')

for sub_folder in tqdm(os.listdir(folder_path), desc=f'Processing {folder_path}'):
        sub_folder_path = os.path.join(folder_path, sub_folder)
        if os.path.isdir(sub_folder_path):
            # 视频分段后ID就是文件夹的名称
            video_segment_id = sub_folder
            # 遍历文件夹内的所有文件
            for file_name in tqdm(os.listdir(sub_folder_path), desc=f'Reading files in {sub_folder}'):
                ASR_file_path = os.path.join(sub_folder_path, file_name)
                # OCR和merged文件需要将srt文件名替换为txt文件名
                OCR_file_path = os.path.join(base_path, 'OCR', sub_folder, file_name.replace('.srt', '.txt'))
                
                merged_file_path = os.path.join(base_path,'merged', sub_folder, file_name.replace('.srt', '.txt'))
                # 读取ASR文件
                with open(ASR_file_path, 'r', encoding='utf-8') as f:
                    ASR_text = f.read()
                    # 对于srt文件，提取文字部分
                    if file_name.endswith('.srt'):
                        ASR_text = re.sub(r'\d+\n\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}\n', '', ASR_text)
                        ASR_text = re.sub(r'\n+', ' ', ASR_text).strip()
                # 读取OCR文件
                with open(OCR_file_path, 'r', encoding='utf-8') as f:
                    OCR_text = f.read()
                # 读取合并去重文件
                with open(merged_file_path, 'r', encoding='utf-8') as f:    
                    merged_text = f.read()

                # 从文件路径提取视频分段后ID和原视频ID
                video_segment_id = file_name.replace('.srt', '').replace('.txt', '')
                original_video_id = sub_folder
                
                # 查找或创建对应视频分段后ID的行
                row_idx = df.index[df['视频分段后ID'] == video_segment_id]
                if len(row_idx) == 0:
                    # 如果不存在，则创建新行
                    new_row = {'虚假宣传/序号': len(df) + 1, '原视频ID': original_video_id, '视频分段后ID': video_segment_id, 'ASR': ASR_text, 'OCR': OCR_text, '合并去重文本': merged_text}
                    df = df._append(new_row, ignore_index=True)
                else:
                    # 如果存在，则更新对应行
                    df.loc[row_idx[0], 'ASR'] = ASR_text
                    df.loc[row_idx[0], 'OCR'] = OCR_text
                    df.loc[row_idx[0], '合并去重文本'] = merged_text                    


df.to_excel(excel_path, index=False)
