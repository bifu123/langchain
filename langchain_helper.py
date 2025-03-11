from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings, ChatOllama

# from langchain_community.vectorstores import Chroma
# 替换旧的导入
from langchain_chroma import Chroma

from langchain.chains import RetrievalQA



oembed_server = OllamaEmbeddings(
    base_url="http://192.168.66.24:11434",
    model="nomic-embed-text"  # 确认模型名称正确 all-MiniLM-L6-v2 nomic-embed-text
)

ollama_server = ChatOllama(
    base_url="http://192.168.66.26:11434",
    model="llama3:latest",
    temperature=0.8,
    num_predict=256
)

file_path = "./data/tesla_p40.pdf"

db_path = "./chroma_db"

# 加载文档
loader = PyPDFLoader(file_path)
docs = loader.load()

# 分割文档
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
all_splits = text_splitter.split_documents(docs)

# 量化文档存入数据库
vectorstore_to_db = Chroma.from_documents(
    documents=all_splits,
    embedding=oembed_server,
    persist_directory=db_path
)



#加载embedding
vectorstore_from_db = Chroma(
    persist_directory = db_path,         # Directory of db
    embedding_function = oembed_server   # Embedding model
)
#print(vectorstore_from_db)



# 准备问题
question="最大显存是多少？"
docs = vectorstore_from_db.similarity_search(question)
#print(docs)


#运行链
qachain=RetrievalQA.from_chain_type(ollama_server, retriever=vectorstore_from_db.as_retriever())
ans = qachain.invoke({"query": "请用中文回答我：" + question})
print(ans["result"])





