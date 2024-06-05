from video_to_images import process_video_to_images
from video_fps_extractor import process_and_save_fps_data
import yaml

def main():
    with open('config.yaml', encoding='utf-8') as f:
        config = yaml.load(f.read(), Loader=yaml.FullLoader)

    video_folder_path = config['input_folder']
    mp3_folder_path = config['output_folder']
    srt_folder_path = config['srt_folder']
    # 设置视频和图片文件夹路径
    video_root = "/root/bishe/end_output/data/video"  # 更改为你的视频文件夹路径
    frame_root = "/root/bishe/end_output/data/frame"  # 更改为你的输出图片文件夹路径

    # 调用函数
    process_video_to_images(video_root, frame_root)


    # 设置目录路径和输出文件路径
    directory_path = '/root/bishe/end_output/data/video'
    output_path = '/root/bishe/end_output/data/video_fps_data.pkl'

    # 调用函数提取帧率并保存
    process_and_save_fps_data(directory_path, output_path)


if __name__ == "__main__":
    main()







''' 
video_to_image

video_to_fps

python tools/generate_pickle.py /root/bishe/DDM/data/test/frame_data/虚假宣传 --split test

python DDM-Net/test.py \
--dataset kinetics_multiframes \
--val-split test \
-b 192 \
--resume checkpoint.pth.tar

python3 /root/bishe/VidEventExtractor/video_process/get_submission.py /root/bishe/DDM/multif-pred_outputs/checkpoint.pth.tar_虚假宣传_kinetics_multiframes_scores.pkl /root/bishe/DDM/data/test/虚假宣传fps.pkl

video_segment
'''