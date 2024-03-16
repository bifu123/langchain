from langchain_community.document_loaders import PyPDFLoader #PDF加载器
from langchain.indexes.vectorstore import VectorstoreIndexCreator
from langchain.text_splitter import RecursiveCharacterTextSplitter # 分割文档
from langchain_community.embeddings import OllamaEmbeddings # 量化文档
from langchain_community.vectorstores import Chroma # 量化文档数据库
from langchain_community.llms import Ollama #模型
from langchain.chains import RetrievalQA #链
import os



#file_path = "./data/tesla_p40.pdf"
oembed_server = OllamaEmbeddings(base_url="http://192.168.66.24:11434", model="nomic-embed-text")
ollama_server = Ollama(base_url='http://192.168.66.26:11434', model="gemma:7b")
db_path = "./chroma_db"



# 加载./data下的所有文档
def get_all_files(directory):
    """
    递归遍历指定目录下的所有文件，并返回文件路径列表
    """
    all_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            all_files.append(file_path)
    return all_files

loaders = []
for file_name in get_all_files("./data"):
    loaders.append(PyPDFLoader(file_name))
    
docs = []
for loader in loaders:
    docs.extend(loader.load())
# print(len(docs))




# 分割文档
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
all_splits = text_splitter.split_documents(docs)
# print(all_splits)




#量化文档存入数据库
vectorstore_to_db = Chroma.from_documents(
    documents = all_splits,           # Data
    embedding = oembed_server,        # Embedding model
    persist_directory = db_path       # Directory to save data
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