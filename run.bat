@echo off
chcp 65001 >nul
echo ========================================
echo   多平台发布助手 - 启动脚本
echo ========================================
echo.

cd /d "%~dp0"

REM 检查 Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到 Python，请先安装 Python 3.9+
    pause
    exit /b 1
)

echo [检查] Python 已安装
echo.

REM 检查依赖
echo [检查] 检查依赖...
python -c "import PyQt5" >nul 2>&1
if errorlevel 1 (
    echo [安装] 正在安装依赖...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo [错误] 依赖安装失败
        pause
        exit /b 1
    )
)

echo [完成] 依赖检查通过
echo.

REM 启动应用
echo [启动] 正在启动多平台发布助手...
echo.

python app.py

pause
