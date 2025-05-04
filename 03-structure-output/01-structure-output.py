import os

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

# 加载.env文件
load_dotenv()
# 获取环境变量
api_key = os.getenv("OPENROUTER_API_KEY")
model_name = os.getenv("MODEL_NAME")

# 修改为使用OpenRouter
model = init_chat_model(
    model="openai/gpt-4.1-mini",  # 或其他OpenRouter支持的模型
    model_provider="openai",
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
    temperature=0,
)


tagging_prompt = ChatPromptTemplate.from_template(
    """
Extract the desired information from the following passage.

Only extract the properties mentioned in the 'Classification' function.

Passage:
{input}
"""
)


class Classification(BaseModel):
    sentiment: str = Field(..., enum=["happy", "neutral", "sad"])
    aggressiveness: int = Field(
        ...,
        description="describes how aggressive the statement is, the higher the"
        "number the more aggressive",
        enum=[1, 2, 3, 4, 5],
    )
    language: str = Field(
        ..., enum=["spanish", "english", "french", "german", "italian"]
    )


# Structured LLM
structured_llm = model.with_structured_output(Classification)

inp = "Estoy increiblemente contento de haberte conocido! Creo que seremos muy\
       buenos amigos!"
prompt = tagging_prompt.invoke({"input": inp})
print(model.invoke(prompt))
response = structured_llm.invoke(prompt)

print(response)
