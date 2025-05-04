from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

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


pdf_loader = PyPDFLoader("data/demo.pdf")
pdf_docs = pdf_loader.load()
print(f"Loaded {len(pdf_docs)} PDF pages")

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, chunk_overlap=200, add_start_index=True
)
all_splits = text_splitter.split_documents(pdf_docs)


vector_store = InMemoryVectorStore(embeddings)
ids = vector_store.add_documents(documents=documents)


results = vector_store.similarity_search("什么是解释性语言")


results = vector_store.similarity_search_with_score("什么是解释性语言")

print(results[0])

embedding = embeddings.embed_query("什么是解释性语言")
results = vector_store.similarity_search_by_vector(embedding)
print(results[0])
