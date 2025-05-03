from dotenv import load_dotenv
import os
from langchain.chat_models import init_chat_model
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

# 加载.env文件
load_dotenv()

# 获取环境变量
api_key = os.getenv("OPENROUTER_API_KEY")
model_name = os.getenv("MODEL_NAME")

# 修改为使用OpenRouter并启用流式输出
model = init_chat_model(
    model=model_name,  # 或其他OpenRouter支持的模型
    model_provider="openai",
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
    callbacks=[StreamingStdOutCallbackHandler()],
    streaming=True
)

while True:
    user_input = input("请输入您的问题：")
    if user_input.lower() == "exit":
        break
    # 流式输出会在回调中处理，不需要再打印响应内容
    model.invoke(user_input)
