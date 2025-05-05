import os

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel

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

 重要提示：你最多只能使用工具 {max_tool_uses} 次。在使用工具 {max_tool_uses} 次后，你必须给出最终答案。
 当前已使用工具次数：{current_tool_uses}, 需要拆分问题查询，不要一起查询。

 现在开始回答，记得在给出最终答案前多按照指定格式进行一步一步的推理。如果根据信息，可以直接输出最终答案Final Answer。

    Question: {input}
    {history}
    """
prompt = ChatPromptTemplate.from_template(prompt_template)


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


def run_agent(user_input, max_tool_uses=2):
    search = TavilySearchResults(max_results=2)
    tools_string = "\n".join(
        [f"{tool.name}: {tool.description}" for tool in [search]]
    )
    tool_names_string = ", ".join([tool.name for tool in [search]])

    # 初始化对话历史
    conversation_history = []
    current_tool_uses = 0

    while True:
        # 如果已经达到最大工具使用次数，强制要求模型给出最终答案
        if current_tool_uses >= max_tool_uses:
            conversation_history.append(
                "\nYou have used the maximum number of tool calls. You must provide a Final Answer now."
            )

        # 生成当前步骤的提示
        current_prompt = prompt.format(
            input=user_input,
            tools=tools_string,
            tool_names=tool_names_string,
            max_tool_uses=max_tool_uses,
            current_tool_uses=current_tool_uses,
            history="\n".join(conversation_history),
        )

        # 调用模型（带停止词）
        response = model.invoke(current_prompt, stop=["Observation:"])

        # 解析模型输出
        last_response = response.content
        lines = [
            line.strip() for line in last_response.split("\n") if line.strip()
        ]

        # 提取关键信息
        action = None
        action_input = None
        final_answer = None

        for line in lines:
            if line.startswith("Action:"):
                action = line.split(":", 1)[1].strip()
            elif line.startswith("Action Input:"):
                action_input = line.split(":", 1)[1].strip()
            elif line.startswith("Final Answer:"):
                final_answer = line.split(":", 1)[1].strip()
                return final_answer  # 如果有最终答案，直接返回

        # 执行工具调用
        if action and action_input and current_tool_uses < max_tool_uses:
            # 调用搜索工具
            observation = search.invoke({"query": action_input})
            # 添加观察结果到历史
            conversation_history.append(response.content)
            conversation_history.append(f"\nObservation: {observation}")
            current_tool_uses += 1
            print(f"工具使用次数: {current_tool_uses}/{max_tool_uses}")
        else:
            # 如果没有找到Action但也没有最终答案，那么强制再次请求最终答案
            conversation_history.append(response.content)
            conversation_history.append("\n你必须给出最终答案。")

            # 如果已经达到最大尝试次数但仍没有最终答案，手动提取或生成一个
            if current_tool_uses >= max_tool_uses:
                # 尝试最后一次获取最终答案
                final_prompt = prompt.format(
                    input=user_input,
                    tools=tools_string,
                    tool_names=tool_names_string,
                    max_tool_uses=max_tool_uses,
                    current_tool_uses=current_tool_uses,
                    history="\n".join(conversation_history)
                    + "\n你已达到最大工具使用次数，现在必须直接给出最终答案，格式为'Final Answer: 你的答案'",
                )

                final_response = model.invoke(final_prompt)
                for line in final_response.content.split("\n"):
                    if line.startswith("Final Answer:"):
                        return line.split(":", 1)[1].strip()

                # 如果还是没有找到最终答案，返回整个响应
                return (
                    "无法获取明确的最终答案，以下是模型的最后响应：\n"
                    + final_response.content
                )


# 示例使用
if __name__ == "__main__":
    user_question = "北京，上海，南京哪个纬度比较高"
    max_tools = 4  # 设置最大工具使用次数

    answer = run_agent(user_question, max_tools)
    print(f"\n最终答案: {answer}")
