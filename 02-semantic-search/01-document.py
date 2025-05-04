from langchain_core.documents import Document

# 基础用法：仅包含内容
doc1 = Document(page_content="这是文档的主要内容")
print(f"基础文档:\n{doc1}\n")

# 完整用法：内容+元数据
doc2 = Document(
    page_content="LangChain是一个用于构建AI应用的框架",
    metadata={
        "source": "技术文档",
        "author": "AI团队",
        "version": 1.2
    }
)
print(f"带元数据的文档:\n{doc2}\n")
print("元数据内容:", doc2.metadata)

# 实际应用场景示例
documents = [
    Document(
        page_content="Python是一种解释型语言",
        metadata={"type": "编程语言", "difficulty": "初级"}
    ),
    Document(
        page_content="机器学习需要大量数据",
        metadata={"type": "AI技术", "difficulty": "高级"}
    )
]

print("\n文档集合示例:")
for idx, doc in enumerate(documents, 1):
    print(f"{idx}. {doc.page_content} (标签: {doc.metadata['type']})")
