# 英文语篇深度研读系统
English Discourse Deep Reading System V1.0

## 项目简介
基于 Python 后端 + 前端页面的面向初高中的AI英语阅读辅助工具，集成 DeepSeek 大模型接口，实现文本解析、阅读理解答疑、长文本精读分析，最终输出语篇分析报告，帮助初高中教师备课。

## 本地启动步骤
1. 克隆项目
git clone git@github.com:pulinyi601-stack/english-discourse-reading.git
cd english-discourse-reading

2. 配置密钥
在项目根目录新建 `.env` 文件，填入内容：
DEEPSEEK_API_KEY=你的密钥

3. 一键运行
双击 start.bat 启动前后端服务，访问本地网页即可使用。

## 目录说明
- backend：后端服务、数据库、AI调用逻辑
- frontend：前端页面静态资源
- start.bat：一键启动脚本
- .gitignore：过滤缓存、密钥、本地数据库
