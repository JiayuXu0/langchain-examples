from dotenv import load_dotenv
import os
from langchain.chat_models import init_chat_model
from langchain.callbacks.base import BaseCallbackHandler


# 定义自定义回调类
class CustomCallbackHandler(BaseCallbackHandler):
    def on_llm_start(self, serialized, prompts, **kwargs):
        print("开始生成回答...")

    def on_llm_new_token(self, token, **kwargs):
        print(token, end="", flush=True)

    def on_llm_end(self, response, **kwargs):
        print("\n回答生成结束。")


# 加载.env文件
load_dotenv()

# 获取环境变量
api_key = os.getenv("OPENROUTER_API_KEY")
model_name = os.getenv("MODEL_NAME")

# 修改为使用OpenRouter并启用流式输出，使用自定义回调
model = init_chat_model(
    model=model_name,  # 或其他OpenRouter支持的模型
    model_provider="openai",
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
    callbacks=[CustomCallbackHandler()],
    streaming=True
)

while True:
    user_input = input("请输入您的问题：")
    if user_input.lower() == "exit":
        break
    # 流式输出会在回调中处理，不需要再打印响应内容
    model.invoke(user_input)
