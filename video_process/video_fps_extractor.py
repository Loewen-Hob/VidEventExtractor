import ffmpeg
import os
import pickle

def get_fps(video_path):
    """提取视频的帧率"""
    try:
        probe = ffmpeg.probe(video_path)
        video_streams = [stream for stream in probe['streams'] if stream['codec_type'] == 'video']
        fps = eval(video_streams[0]['r_frame_rate'])
        return fps
    except (ffmpeg.Error, ZeroDivisionError) as e:
        print(f"Error with video {video_path}: {e}")
        return None

def extract_fps_from_videos(directory_path):
    """遍历文件夹，提取所有视频的帧率，并按新的数据结构保存"""
    video_fps_dict = {}
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith(".mp4"):
                video_name = os.path.splitext(file)[0]  # 去除文件扩展名
                video_path = os.path.join(root, file)
                fps = get_fps(video_path)
                if fps is not None:
                    video_fps_dict[video_name] = {'fps': fps}
    return video_fps_dict

def save_fps_data(video_fps_dict, output_path):
    """将视频帧率数据保存到Pickle文件"""
    with open(output_path, 'wb') as f:
        pickle.dump(video_fps_dict, f)

def process_and_save_fps_data(directory_path, output_path):
    """提取帧率并保存的高级接口函数"""
    video_fps_dict = extract_fps_from_videos(directory_path)
    save_fps_data(video_fps_dict, output_path)
    print(f"Video FPS data saved to {output_path}")
    
if __name__ == '__main__':
    directory_path = '/root/bishe/DDM/data/test/video_data/虚假宣传'
    output_path = '/root/bishe/DDM/data/test/虚假宣传fps.pkl'
    process_and_save_fps_data(directory_path, output_path)