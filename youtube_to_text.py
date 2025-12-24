import os
import sys
import whisper
import yt_dlp
import subprocess

def check_ffmpeg():
    """检查ffmpeg是否安装"""
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def download_audio(url, output_dir="temp"):
    """从YouTube下载音频"""
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)
    
    # 配置下载选项
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': os.path.join(output_dir, 'audio'),
        'quiet': False,
        'no_warnings': False,
    }
    
    print(f"\n正在从 {url} 下载音频...")
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        audio_path = os.path.join(output_dir, 'audio.mp3')
        if os.path.exists(audio_path):
            print(f"音频下载成功: {audio_path}")
            return audio_path
        else:
            print("音频下载失败")
            return None
    except Exception as e:
        print(f"下载音频时出错: {e}")
        return None

def transcribe_audio(audio_path, model_size="base"):
    """使用Whisper进行语音转文字"""
    print(f"\n正在加载Whisper模型 ({model_size})...")
    try:
        model = whisper.load_model(model_size)
        print("模型加载成功")
        
        print("正在进行语音识别...")
        result = model.transcribe(audio_path, language="zh", verbose=True)
        
        return result
    except Exception as e:
        print(f"语音识别时出错: {e}")
        return None

def save_result(result, video_url, output_file="output.txt"):
    """保存转录结果到文件"""
    if not result:
        return

    with open(output_file, "w", encoding="utf-8") as f:
        # 遍历segments，用标点符号连接
        for i, segment in enumerate(result['segments']):
            text = segment['text'].strip()
            if not text:
                continue
            
            # 写入文本
            f.write(text)
            
            # 检查文本结尾是否有标点符号
            if not text[-1] in '。？！，,；;、':
                # 如果没有标点，根据是否是最后一个segment添加标点
                if i == len(result['segments']) - 1:
                    f.write('。')
                else:
                    f.write('，')

    print(f"\n结果已保存到: {output_file}")

def main():
    print("=" * 60)
    print("YouTube视频转文字工具")
    print("=" * 60)
    
    # 检查ffmpeg
    if not check_ffmpeg():
        print("\n错误: 未检测到ffmpeg，请先安装ffmpeg")
        print("Windows安装方法:")
        print("  1. 访问 https://ffmpeg.org/download.html")
        print("  2. 下载并解压ffmpeg")
        print("  3. 将ffmpeg的bin目录添加到系统PATH环境变量中")
        sys.exit(1)
    
    # 获取用户输入
    if len(sys.argv) > 1:
        video_url = sys.argv[1]
    else:
        video_url = input("\n请输入YouTube视频地址: ").strip()
    
    if not video_url:
        print("错误: 请提供有效的YouTube视频地址")
        sys.exit(1)
    
    # 选择模型
    print("\n可用的Whisper模型:")
    print("  tiny   - 最小最快 (推荐快速测试)")
    print("  base   - 小型 (推荐)")
    print("  small  - 中型")
    print("  medium - 大型")
    print("  large  - 最大最准")
    
    model_choice = input("\n请选择模型 (默认: base): ").strip().lower() or "base"
    
    if model_choice not in ["tiny", "base", "small", "medium", "large"]:
        print(f"无效的模型选择，使用默认模型: base")
        model_choice = "base"
    
    # 下载音频
    audio_path = download_audio(video_url)
    if not audio_path:
        sys.exit(1)
    
    # 语音识别
    result = transcribe_audio(audio_path, model_size=model_choice)
    if not result:
        sys.exit(1)
    
    # 保存结果
    save_result(result, video_url)
    
    print("\n完成！")
    print("=" * 60)

if __name__ == "__main__":
    main()
