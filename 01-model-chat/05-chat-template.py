from dotenv import load_dotenv
import os
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate, \
    SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage

# 加载.env文件
load_dotenv()

# 获取环境变量
api_key = os.getenv("OPENROUTER_API_KEY")
model_name = os.getenv("MODEL_NAME")

model = init_chat_model(
    model=model_name,  # 或其他OpenRouter支持的模型
    model_provider="openai",
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key
)

# 第一种构建历史对话的方法
messages = [
    SystemMessage("Translate the following from English into Italian"),
    HumanMessage("hi!"),
]


# for token in model.stream(messages):
#     print(token.content, end="|")

system_template = "Translate the following from English into {language}"


system_message_prompt = SystemMessagePromptTemplate.\
                        from_template(system_template)
human_message_prompt = HumanMessagePromptTemplate.from_template("{text}")

# 第二种构建历史对话的方法
prompt_template = ChatPromptTemplate.from_messages(
    [system_message_prompt, human_message_prompt]
)

prompt = prompt_template.invoke({"language": "Italian", "text": "hi!"})
print(prompt.to_messages())
for token in model.stream(prompt):
    print(token.content, end="|")
