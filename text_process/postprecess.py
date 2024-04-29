import pandas as pd


def preprocess(file_path):
    # 读取Excel文件
    df = pd.read_excel(file_path)

    # 解析“视频分段后ID”中的秒数和微秒，用于排序
    def parse_segment_id(segment_id):
        parts = segment_id.split('_')
        seconds = int(parts[-4])
        microseconds = int(parts[-2])
        return seconds * 1000000 + microseconds

    # 解析“原视频ID”中的数字
    def parse_original_id(original_id):
        # 假设格式总是“文字+数字”的形式
        return int(''.join(filter(str.isdigit, original_id)))

    # 添加两个新列用于排序
    df['原视频ID数字'] = df['原视频ID'].apply(parse_original_id)
    df['排序键'] = df['视频分段后ID'].apply(parse_segment_id)

    # 根据“原视频ID数字”和“排序键”进行排序
    df_sorted = df.sort_values(by=['原视频ID数字', '排序键'])

    # 排序后将 虚假宣传/序号 这个列重新排序从1开始
    df_sorted['虚假宣传/序号'] = range(1, len(df_sorted) + 1)
    # 删除辅助排序列
    df_sorted = df_sorted.drop(columns=['原视频ID数字', '排序键'])

    return df_sorted
file_path = '/root/bishe/end_output/虚假宣传/videos_info.xlsx'
df_processed = preprocess(file_path)

df_processed.to_excel('/root/bishe/end_output/虚假宣传/processed_videos_info.xlsx', index=False)
