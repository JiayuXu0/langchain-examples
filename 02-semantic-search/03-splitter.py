from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

pdf_loader = PyPDFLoader("data/demo.pdf")
pdf_docs = pdf_loader.load()
print(f"Loaded {len(pdf_docs)} PDF pages")

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, chunk_overlap=200, add_start_index=True
)
all_splits = text_splitter.split_documents(pdf_docs)

for i, doc in enumerate(all_splits, 1):
    print(f"\n文档 {i}:")
    print(f"内容: {doc.page_content}")
    print(f"元数据: {doc.metadata}")
