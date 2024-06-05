import subprocess
import os

def process_video_to_images(video_root, frame_root):
    """
    批量处理指定文件夹中的所有视频文件，将每个视频转换为一系列图片。

    参数:
    - video_root: 视频文件的根目录路径。
    - frame_root: 图片输出的根目录路径。
    """
    # 确保输出目录存在
    if not os.path.exists(frame_root):
        os.makedirs(frame_root)

    # 获取所有视频文件
    video_files = [f for f in os.listdir(video_root) if f.endswith((".mp4", ".avi", ".mov"))]
    total_videos = len(video_files)

    # 遍历视频根目录
    for idx, video_file in enumerate(video_files, start=1):
        video_path = os.path.join(video_root, video_file)
        # 创建视频对应的图片目录
        video_name = os.path.splitext(video_file)[0]
        image_dir = os.path.join(frame_root, video_name)
        if not os.path.exists(image_dir):
            os.makedirs(image_dir)

        # 构建ffmpeg命令
        command = [
            "ffmpeg",
            "-i", video_path,
            "-f", "image2",
            "-qscale:v", "2",
            "-loglevel", "quiet",
            os.path.join(image_dir, "image_%05d.png")
        ]

        print(f"Processing {video_file} ({idx}/{total_videos})...")
        # 执行ffmpeg命令
        subprocess.run(command)
        print(f"Finished {video_file}")

if __name__ == "__main__":
    video_root = "/root/bishe/DDM/data/test/video_data/虚假宣传"  # 更改为你的视频文件夹路径
    frame_root = "/root/bishe/DDM/data/test/frame_data/虚假宣传"  # 更改为你的输出图片文件夹路径
    process_video_to_images(video_root, frame_root)
