from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, \
                                    MessagesPlaceholder
from langchain_core.messages import HumanMessage

# 主要包括prompts和messages，其中prompttemplate是一个通用模板，chatprompttemplate是一个聊天模板
# 消息message包括AIMessage，HumanMessage，SystemMessage，ChatMessage，FunctionMessage，ToolMessage
# MessagesPlaceholder是一个占位符，用于在聊天模板中插入消息

prompt_template = PromptTemplate.from_template("Tell me a joke about {topic}")

print(prompt_template.invoke({"topic": "cats"}))

prompt_template = ChatPromptTemplate([
    ("system", "You are a helpful assistant"),
    ("user", "Tell me a joke about {topic}")
])

print(prompt_template.invoke({"topic": "cats"}))


prompt_template = ChatPromptTemplate([
    ("system", "You are a helpful assistant"),
    MessagesPlaceholder("msgs")
])

print(prompt_template.invoke({"msgs": [HumanMessage(content="hi!")]}))
