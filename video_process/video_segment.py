import pickle
import os
from moviepy.editor import VideoFileClip

file_path = '/root/bishe/VidEventExtractor/不符合规定_0.8_submission.pkl'
with open(file_path, 'rb') as file:
    data = pickle.load(file)

video_directory = "/root/bishe/DDM/data/test/video_data/不符合规定"
output_directory = "/root/bishe/end_output/不符合规定/segment_video_0.8"

if not os.path.exists(output_directory):
    os.makedirs(output_directory)

for video_id, split_points in data.items():
    video_path = os.path.join(video_directory, f"{video_id}.mp4")
    video = VideoFileClip(video_path)
    
    # 为当前视频创建一个新的目录
    video_output_directory = os.path.join(output_directory, video_id)
    if not os.path.exists(video_output_directory):
        os.makedirs(video_output_directory)
    
    start = 0
    for end in split_points:
        # 格式化开始和结束时间，保留两位小数
        start_str = f"{start:.2f}".replace('.', '_')
        end_str = f"{end:.2f}".replace('.', '_')
        
        segment = video.subclip(start, end)
        # 更新文件名以包含开始和结束秒数，保存在对应视频名称的文件夹中
        segment_filename = f"{video_id}_segment_{start_str}_{end_str}.mp4"
        segment_path = os.path.join(video_output_directory, segment_filename)
        
        segment.write_videofile(segment_path, codec="libx264", audio_codec="aac")
        start = end

    # 最后一个片段到视频结束
    start_str = f"{start:.2f}".replace('.', '_')
    end_str = f"{video.duration:.2f}".replace('.', '_')
    segment_filename = f"{video_id}_segment_{start_str}_{end_str}.mp4"
    segment_path = os.path.join(video_output_directory, segment_filename)
    video.subclip(start, video.duration).write_videofile(segment_path, codec="libx264", audio_codec="aac")

    # 释放视频文件
    video.close()
