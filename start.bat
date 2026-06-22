@echo off
chcp 65001 >nul
title AI 英文语篇深度研读系统

echo ========================================
echo  AI 英文语篇深度研读系统 - 启动中...
echo ========================================
echo.

:: 设置 Python 路径
set PATH=C:\Users\97452\AppData\Local\Programs\Python\Python312;%PATH%

:: 启动后端
echo [1/2] 启动后端服务...
start "Backend" cmd /c "cd /d %~dp0backend && python -m uvicorn app.main:app --host 0.0.0.0 --port 8000"

:: 等待后端启动
timeout /t 4 /nobreak >nul

:: 启动前端
echo [2/2] 启动前端服务...
start "Frontend" cmd /c "cd /d %~dp0frontend && npx vite --port 5173"

:: 等待前端启动
timeout /t 3 /nobreak >nul

:: 打开浏览器
echo 正在打开浏览器...
start http://localhost:5173

echo.
echo ========================================
echo  启动完成！
echo  前端地址：http://localhost:5173
echo  后端地址：http://localhost:8000
echo.
echo  关闭页面后，按任意键关闭服务...
echo ========================================
pause >nul

:: 关闭服务
taskkill /f /fi "WINDOWTITLE eq Backend" >nul 2>&1
taskkill /f /fi "WINDOWTITLE eq Frontend" >nul 2>&1

echo 服务已关闭。
timeout /t 2 /nobreak >nul
