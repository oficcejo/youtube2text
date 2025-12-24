# YouTube视频转文字工具

## 功能说明
本程序可以将YouTube视频中的音频转换为文字，支持中文识别。

## 使用前准备

### 1. 安装Python 3.8或更高版本
https://www.python.org/downloads/

### 2. 安装FFmpeg
- 访问: https://ffmpeg.org/download.html
- 下载Windows版本并解压
- 将ffmpeg的bin目录添加到系统PATH环境变量中
- 验证安装: 在命令行输入 `ffmpeg -version`

## 快速开始

### Windows用户
双击运行 `run.bat` 文件

### 命令行使用
1. 安装依赖:
   ```bash
   pip install -r requirements.txt
   ```

2. 运行程序:
   ```bash
   python youtube_to_text.py
   ```

3. 输入YouTube视频地址，选择模型，等待转换完成

4. 查看输出文件 `output.txt`

### 命令行参数
```bash
python youtube_to_text.py <YouTube视频URL>
```

## Whisper模型说明
| 模型 | 说明 | 大小 |
|------|------|------|
| tiny | 最小最快，适合快速测试 | ~1GB |
| base | 小型，推荐使用 | ~1.5GB |
| small | 中型，准确性更高 | ~2.5GB |
| medium | 大型，更准确 | ~5GB |
| large | 最大最准确 | ~10GB |

首次运行会自动下载模型，需要联网。

## 输出说明
程序会生成 `output.txt` 文件，包含简体中文文本，自动添加标点符号分隔句子。

## 注意事项
1. 确保网络畅通，首次需要下载Whisper模型
2. 大型视频下载和转录可能需要较长时间
3. 音频质量影响识别准确度

## 故障排查
1. **FFmpeg未安装**: 请先安装FFmpeg并添加到PATH
2. **网络错误**: 检查网络连接和代理设置
3. **内存不足**: 尝试使用更小的模型 (tiny 或 base)
