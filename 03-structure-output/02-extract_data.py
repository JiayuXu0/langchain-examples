import os
from typing import List, Optional

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field


class Person(BaseModel):
    """Information about a person."""

    name: Optional[str] = Field(
        default=None, description="The name of the person"
    )
    hair_color: Optional[str] = Field(
        default=None, description="The color of the person's hair if known"
    )
    height_in_meters: Optional[str] = Field(
        default=None, description="Height measured in meters"
    )


prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an expert extraction algorithm. "
            "Only extract relevant information from the text. "
            "If you do not know the value of an attribute asked to extract, "
            "return null for the attribute's value.",
        ),
        ("human", "{text}"),
    ]
)
# 加载.env文件
load_dotenv()
# 获取环境变量
api_key = os.getenv("OPENROUTER_API_KEY")
model_name = os.getenv("MODEL_NAME")

# 修改为使用OpenRouter
model = init_chat_model(
    model="openai/gpt-4.1-mini",
    model_provider="openai",
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
    temperature=0,
)


class Data(BaseModel):
    """Extracted data about people."""

    # Creates a model so that we can extract multiple entities.
    people: List[Person]


structured_llm = model.with_structured_output(schema=Data)

text = "Alan Smith is 6 feet tall and has blond hair."
prompt = prompt_template.invoke({"text": text})
print(structured_llm.invoke(prompt))


messages = [
    ("human", "2 🦜 2"),
    ("ai", "4"),
    ("human", "2 🦜 10"),
    ("ai", "12"),
    ("human", "3 🦜 4"),
]

response = model.invoke(messages)
print(response.content)
