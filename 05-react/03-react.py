# 基础依赖引用
import os

from dotenv import load_dotenv
from langchain import hub
from langchain.agents import (
    AgentExecutor,
    create_openai_functions_agent,
    create_openai_tools_agent,
    create_react_agent,
    create_structured_chat_agent,
)
from langchain.chat_models import init_chat_model
from langchain_community.chat_models import ChatOllama
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.utils.function_calling import convert_to_openai_function

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


# 定义工具
def get_current_weather(location: str, unit: str = "fahrenheit"):
    """Get the current weather in a given location"""
    return "It is raining today in Ann Arbor, Michigan, USA"


def search_web(query: str):
    """Search the web for the latest information"""
    return "The latest information on the topic"


search = TavilySearchResults(max_results=2)
tools = [search]


def react(question):
    # 定义提示词
    prompt_template = """
 按照给定的格式回答以下问题。你可以使用下面这些工具：

    {tools}

 回答时需要遵循以下用---括起来的格式：

    ---
    Question: 我需要回答的问题
    Thought: 回答这个问题我需要做些什么
    Action: {tool_names} 中的其中一个工具名
    Action Input: 选择工具所需要的输入
    Observation: 选择工具返回的结果
    ...（这个思考/行动/行动输入/观察可以重复N次）
    Thought: 我现在知道最终答案
    Final Answer: 原始输入问题的最终答案
    ---

 现在开始回答，记得在给出最终答案前多按照指定格式进行一步一步的推理。

    Question: {input}
    {agent_scratchpad}
    """

    prompt = ChatPromptTemplate.from_template(prompt_template)
    # 大模型： llm = ChatOpenAI(model=local_model,api_key=api_key,base_url=local_api_base,**kwargs)
    # tools(get_current_weather: 基于高德的查询某个城市当前天气的api， search_web：基于百度搜索的api)
    #  高德查询天气的api调用方法：https://restapi.amap.com/v3/weather/weatherInfo?city=110101&key=<用户key>
    # 注意：stop_sequence=True 这个参数用于控制大模型执行过程中避免把Observation:加入到工具的输入参数中，但有的大模型好使，有的不好使。
    agent = create_react_agent(
        llm=model, tools=tools, prompt=prompt, stop_sequence=True
    )
    agent_executor = AgentExecutor.from_agent_and_tools(
        agent=agent, tools=tools, verbose=True, handle_parsing_errors=True
    )

    inputs = {"input": question}

    result = agent_executor.invoke(inputs)
    return result.get("output")


if __name__ == "__main__":
    question = "北京和上海，哪个冬天更冷，分步骤进行查询"
    result = react(question)
    print(f"react:{result}")
