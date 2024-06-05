
# VidEventExtractor

VidEventExtractor是一个先进的视频事件抽取工具，旨在自动识别和提取视频中的关键事件。通过利用最新的深度学习和图像处理技术，VidEventExtractor能够准确地从各种视频源中检测特定事件，为视频分析和内容创造提供强大支持。

## 特点

- **高效的事件识别**：快速识别视频中的关键事件。
- **支持多种视频格式**：兼容常见的视频格式，如MP4、AVI等。
- **灵活的应用场景**：适用于视频监控、内容分析、媒体生产等多个领域。

## 开始使用

### 环境要求

- Python 3.6+
- ffmpeg
- 其他依赖，请查看`requirements.txt`文件。

### 安装

首先，克隆仓库到本地：

```bash
git clone https://github.com/Loewen-Hob/VidEventExtractor.git
cd VidEventExtractor
```

安装所需的Python依赖：

```bash
pip install -r requirements.txt
```

## 如何使用

### 第一步：数据集构建

1. 将视频转换为图像序列：

```bash
python video_process/video_to_images.py --video_path your_video.mp4 --output_path frames_folder
```

2. 提取视频的帧率信息：

```bash
python video_process/video_fps_extractor.py --video_path your_video.mp4 --output_path fps_info.json
```

3. 生成数据集的pickle文件：

```bash
python tools/generate_pickle.py /DDM/data/test/frame_data/虚假宣传 --split test
```

4. 进行模型推理：

```bash
python DDM/DDM-Net/test.py --dataset kinetics_multiframes --val-split test -b 192 --resume checkpoint.pth.tar
```

5. 提取视频事件的提交文件：

```bash
python video_process/get_submission.py /DDM/multif-pred_outputs/checkpoint.pth.tar_虚假宣传_kinetics_multiframes_scores.pkl /DDM/data/test/虚假宣传fps.pkl
```

6. 对视频进行分段处理：

```bash
python video_process/video_segment.py --input_path your_video.mp4 --output_path segmented_videos
```

7. 对分段后视频提取OCR文本：

```bash
python image_OCR/get_ocr.py
```

8. 提取分段后视频ASR文本：

```bash
python auto_VideoToAudioToText/main.py
```

9. 合并OCR和ASR文本：

```bash 
python text_process/get_excel.py
```

### 第二步：多模态命名实体识别

1. 使用HZPGIM中的脚本对数据集进行处理，得到训练集、验证集、测试集：

```bash
python HZPGIM/code/..
```

2. 修改/root/bishe/VidEventExtractor/adaseq/examples/HZPGIM/HZPGIM.yaml中的数据集路径。

3. 训练模型：

```bash
python -m scripts.train -c examples/HZPGIM/HZPGIM.yaml
```

### 第三步：事件抽取
1. 使用HZPGIT中的脚本进行训练与预测
## 贡献

我们欢迎所有形式的贡献，包括错误报告、功能请求和代码提交。请通过GitHub issue或pull request提交你的贡献。

## 许可证

本项目采用MIT许可证。有关详细信息，请查看[LICENSE](LICENSE)文件。

## 致谢

特别感谢所有为这个项目做出贡献的开发者和研究人员。

---

欢迎使用VidEventExtractor，开始探索视频中未被发现的事件吧！