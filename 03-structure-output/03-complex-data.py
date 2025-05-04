import os
from typing import List, Optional

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.utils.function_calling import tool_example_to_messages
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


class Data(BaseModel):
    """Extracted data about people."""

    # Creates a model so that we can extract multiple entities.
    people: List[Person]


examples = [
    (
        "The ocean is vast and blue. It's more than 20,000 feet deep.",
        Data(people=[]),
    ),
    (
        "Fiona traveled far from France to Spain.",
        Data(
            people=[
                Person(name="Fiona", height_in_meters=None, hair_color=None)
            ]
        ),
    ),
]

examples = [
    (
        "The ocean is vast and blue. It's more than 20,000 feet deep.",
        Data(people=[]),
    ),
    (
        "Fiona traveled far from France to Spain.",
        Data(
            people=[
                Person(name="Fiona", height_in_meters=None, hair_color=None)
            ]
        ),
    ),
]


messages = []

for txt, tool_call in examples:
    if tool_call.people:
        # This final message is optional for some providers
        ai_response = "Detected people."
    else:
        ai_response = "Detected no people."
    messages.extend(
        tool_example_to_messages(txt, [tool_call], ai_response=ai_response)
    )

for message in messages:
    message.pretty_print()


message_no_extraction = {
    "role": "user",
    "content": "The solar system is large, but earth has only 1 moon.",
}


# 加载.env文件
load_dotenv()
# 获取环境变量
api_key = os.getenv("OPENROUTER_API_KEY")
model_name = os.getenv("MODEL_NAME")

# 修改为使用OpenRouter
model = init_chat_model(
    model="openai/gpt-4o-mini",
    model_provider="openai",
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
    temperature=0,
)

structured_llm = model.with_structured_output(schema=Data)
response = structured_llm.invoke([message_no_extraction])
print(response)

response = structured_llm.invoke(messages + [message_no_extraction])
print(response)
