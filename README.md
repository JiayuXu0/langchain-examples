# 🚀 LangChain 示例项目

![LangChain Version](https://img.shields.io/badge/LangChain-0.0.340-blue)
![Python Version](https://img.shields.io/badge/Python-3.10%2B-green)

本项目为LangChain框架的实践示例集合，包含多种常见AI应用场景的实现，适合开发者学习与参考。

## 📖 目录
- [功能特性](#✨-功能特性)
- [快速开始](#🚀-快速开始)
- [项目结构](#📁-项目结构)
- [使用示例](#🎯-使用示例)
- [API配置](#🔑-api配置)
- [贡献指南](#🤝-贡献指南)
- [许可证](#📄-许可证)

## ✨ 功能特性
- 基础聊天机器人实现
- 语义搜索系统搭建
- 结构化输出处理
- 自定义聊天代理开发
- 多模态数据处理

## 🚀 快速开始

### 环境准备
```shell
# 创建虚拟环境
uv venv .venv
source .venv/bin/activate

# 安装依赖
uv pip install "langchain[all]" python-dotenv

# 配置API密钥
cp .env.example .env
```

### 运行示例
```python
# 进入示例目录
cd 01-model-chat

# 运行基础聊天程序
python 01-basic-chat.py
```

## 📁 项目结构
```
.
├── 01-model-chat/        # 基础聊天模块
├── 02-semantic-search/   # 语义搜索系统
├── 03-structure-output/  # 结构化输出处理
├── 04-chatbot/           # 高级聊天机器人
├── data/                  # 示例数据
└── .env.example           # 环境配置模板
```

## 🔑 API配置
1. 访问 [OpenRouter密钥管理](https://openrouter.ai/settings/keys) 获取API Key
2. 将密钥填入`.env`文件：
```ini
OPENROUTER_API_KEY=your_api_key_here
MODEL_NAME=gpt-3.5-turbo
```

## 🤝 贡献指南
欢迎通过Issue提交问题或Pull Request贡献代码，请确保：
1. 遵循现有代码风格
2. 包含必要的单元测试
3. 更新相关文档

## 📄 许可证
本项目采用 [MIT License](LICENSE)
