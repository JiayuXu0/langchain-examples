import os
from typing import TypedDict

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import END, StateGraph


# 定义状态
class ChatState(TypedDict):
    user_input: str
    response: str
    is_positive: bool


load_dotenv()
# 获取环境变量
api_key = os.getenv("OPENROUTER_API_KEY")
model_name = os.getenv("MODEL_NAME")

# 修改为使用OpenRouter
llm = init_chat_model(
    model="openai/gpt-4o-mini",
    model_provider="openai",
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
    temperature=0,
)


# 节点 1：处理用户输入并生成回复
def generate_response(state: ChatState) -> ChatState:
    prompt = ChatPromptTemplate.from_template("回复用户输入：{input} ")
    response = llm.invoke(prompt.format(input=state["user_input"])).content
    return {"response": response, "is_positive": "好" in response}


# 节点 2：处理积极回复
def handle_positive(state: ChatState) -> ChatState:
    return {"response": state["response"] + " 很高兴听到这个！"}


# 节点 3：处理非积极回复
def handle_negative(state: ChatState) -> ChatState:
    return {"response": state["response"] + " 有什么我可以帮助的吗？"}


# 条件函数：根据 is_positive 决定跳转
def check_sentiment(state: ChatState) -> str:
    return "positive" if state["is_positive"] else "negative"


# 创建状态图
graph = StateGraph(ChatState)

# 添加节点
graph.add_node("generate_response", generate_response)
graph.add_node("handle_positive", handle_positive)
graph.add_node("handle_negative", handle_negative)
graph.add_node("check_sentiment", lambda state: None)  # 添加空节点

# 添加边
graph.add_edge("generate_response", "check_sentiment")
graph.add_conditional_edges(
    "check_sentiment",
    check_sentiment,
    {"positive": "handle_positive", "negative": "handle_negative"},
)
graph.add_edge("handle_positive", END)
graph.add_edge("handle_negative", END)

# 设置入口点
graph.set_entry_point("generate_response")

# 编译图
app = graph.compile()

# 运行工作流
input_state = {"user_input": "今天这个榴莲不好吃"}
result = app.invoke(input_state)
print(result)
