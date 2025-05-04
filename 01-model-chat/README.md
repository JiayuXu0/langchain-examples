# 01-LangChain 聊天模型示例

这个项目展示了如何使用 LangChain 结合 OpenRouter 创建一个简单的聊天交互程序。

## 功能概述

该程序具有以下特性：

- 持续监听用户输入
- 输入 `exit` 命令可终止程序
- 自动调用 OpenRouter 模型生成回答
- 支持完整的对话上下文维护

## 运行指南

在终端执行以下命令启动程序：

```bash
python main.py
```

### 消息角色映射

| 消息类型       | 角色标识  |
|----------------|-----------|
| HumanMessage   | user      |
| AIMessage      | assistant |
| SystemMessage  | system    |

## 对话历史构建方式

### 方式一：Message 对象列表

```python
messages = [
    SystemMessage("Translate the following from English into Italian"),
    HumanMessage("hi!"),
]
```

### 方式二：字典对象列表

```python
messages = [
    {"role": "system", "content": "Translate the following from English into Italian"},
    {"role": "user", "content": "hi!"},
]
```

### 方式三：模板构建方式

```python
system_message_prompt = SystemMessagePromptTemplate.\
                        from_template(system_template)
human_message_prompt = HumanMessagePromptTemplate.from_template("{text}")

prompt_template = ChatPromptTemplate.from_messages(
    [system_message_prompt, human_message_prompt]
)

prompt = prompt_template.invoke({"language": "Italian", "text": "hi!"})
```

## 使用提示

- 在交互界面中直接输入您的问题
- 输入 `exit` 并回车可随时退出程序
- 确保已配置有效的 API 密钥和模型参数
