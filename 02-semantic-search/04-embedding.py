from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-mpnet-base-v2"
)
documents = [
    Document(
        page_content="Python是一种解释型语言",
        metadata={"type": "编程语言", "difficulty": "初级"},
    ),
    Document(
        page_content="机器学习需要大量数据",
        metadata={"type": "AI技术", "difficulty": "高级"},
    ),
]

vector_1 = embeddings.embed_query(documents[0].page_content)
vector_2 = embeddings.embed_query(documents[1].page_content)

assert len(vector_1) == len(vector_2)
print(f"Generated vectors of length {len(vector_1)}\n")
print(vector_1[:10])
