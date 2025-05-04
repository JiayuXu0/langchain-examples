from langchain.document_loaders import (
    Docx2txtLoader,
    PyPDFLoader,
    WebBaseLoader,
)

# 1. 网页内容加载
web_loader = WebBaseLoader(
    ["https://k.sina.com.cn/article_1686546714_6486a91a02002rjw8.html"]
)
web_docs = web_loader.load()
print(f"Loaded {len(web_docs)} web documents")

# 2. PDF文件加载
pdf_loader = PyPDFLoader("data/demo.pdf")
pdf_docs = pdf_loader.load()
print(f"Loaded {len(pdf_docs)} PDF pages")

# 3. Word文档加载
docx_loader = Docx2txtLoader("data/demo.docx")
docx_docs = docx_loader.load()
print(f"Loaded {len(docx_docs)} Word documents")

# 合并所有文档
all_docs = web_docs + pdf_docs + docx_docs
print(f"Total documents loaded: {len(all_docs)}")

# 新增内容：打印每个文档的详细内容
print("\n文档详情:")
for i, doc in enumerate(all_docs, 1):
    print(f"\n文档 {i}:")
    print(f"内容: {doc.page_content}")
    print(f"元数据: {doc.metadata}")
