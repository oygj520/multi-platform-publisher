@echo off
chcp 65001 >nul
echo ========================================
echo   多平台发布助手 - 初始化脚本
echo ========================================
echo.

cd /d "%~dp0"

echo [1/3] 安装 Python 依赖...
py -m pip install PyQt5 PyQtWebEngine markdown playwright -q

echo [2/3] 安装 Playwright 浏览器...
py -m playwright install chromium

echo [3/3] 完成！
echo.
echo 现在可以运行 run.bat 启动应用

pause
