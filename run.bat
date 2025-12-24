@echo off
chcp 65001 > nul
echo ========================================
echo YouTube视频转文字工具
echo ========================================
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未检测到Python，请先安装Python 3.8+
    pause
    exit /b 1
)

REM 检查虚拟环境
if not exist "venv" (
    echo 创建虚拟环境...
    python -m venv venv
)

REM 激活虚拟环境
echo 激活虚拟环境...
call venv\Scripts\activate.bat

REM 安装依赖
echo.
echo 检查依赖包...
pip install -r requirements.txt

REM 运行程序
echo.
echo 启动程序...
python youtube_to_text.py

pause
