from langchain_community.document_loaders import PyPDFLoader #PDF加载器
from langchain.indexes.vectorstore import VectorstoreIndexCreator
from langchain.text_splitter import RecursiveCharacterTextSplitter # 分割文档
from langchain_community.embeddings import OllamaEmbeddings # 量化文档
from langchain_community.vectorstores import Chroma # 量化文档数据库
from langchain_community.llms import Ollama #模型
from langchain.chains import RetrievalQA #链
import os


file_path = "./data/tesla_p40.pdf"
oembed_server = OllamaEmbeddings(base_url="http://192.168.66.24:11434", model="nomic-embed-text")
ollama_server = Ollama(base_url='http://192.168.66.26:11434', model="gemma:7b")
db_path = "./chroma_db/"
data_directory = "./data"



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

def vectorstore_to_db(file_paths, oembed_server, db_path):
    """
    将给定文件列表中的文档加工成向量，并存储到数据库中
    """
    for file_path in file_paths:
        # 提取文件名（不含后缀）
        file_name = os.path.splitext(os.path.basename(file_path))[0]

        # 加载文档
        loader = PyPDFLoader(file_path)
        docs = loader.load()

        # 分割文档
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
        all_splits = text_splitter.split_documents(docs)

        # 量化文档存入数据库
        Chroma.from_documents(
            documents=all_splits,
            embedding=oembed_server,
            persist_directory=os.path.join(db_path, file_name)
        )

# 获取所有文件路径
file_paths = get_all_files(data_directory)


# 执行处理
vectorstore_to_db(file_paths, oembed_server, db_path)

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

