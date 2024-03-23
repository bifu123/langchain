#################### 导入包 ##################
import os
import shutil

from config import *


# 文档加工
from langchain_community.document_loaders import DirectoryLoader, UnstructuredWordDocumentLoader
from langchain.indexes.vectorstore import VectorstoreIndexCreator
from langchain.text_splitter import RecursiveCharacterTextSplitter # 分割文档
from langchain_community.vectorstores import Chroma # 量化文档数据库

# ollama模型
from langchain_community.embeddings import OllamaEmbeddings # 量化文档
from langchain_community.llms import Ollama #模型

# gemini模型
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI









os.environ['GOOGLE_API_KEY'] = GOOGLE_API_KEY #将GOOGLE_API_KEY加载到环境变量中

# 本地量化模型
embedding_ollama = OllamaEmbeddings(
    base_url = embedding_ollama_conf["base_url"], 
    model = embedding_ollama_conf["model"]
) 
# #线上google量化模型
embedding_google = GoogleGenerativeAIEmbeddings(
    model=embedding_google_conf["model"]
) 
# #embedding_google.embed_query("hello, world!")


# 选择量化模型
if model_choice["embedding"] == "ollama":
    embedding = embedding_ollama
else:
    embedding = embedding_google




class DocumentProcessor:
    def __init__(self, data_path, db_path, embedding):
        self.data_path = data_path
        self.db_path = db_path
        self.embedding = embedding

    def load_documents(self):
        print("正在加载" + self.data_path + "下的所有文档...")
        loader = DirectoryLoader(self.data_path, show_progress=True, use_multithreading=True)
        print("半小时                                                                                                                                                                                                                                                                                          5")
        print(loader.load())
        return loader.load()

    def split_documents(self, docs):
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        return text_splitter.split_documents(docs)

    def clean_db_path(self):
        if os.path.exists(self.db_path) and os.path.isdir(self.db_path):
            try:
                shutil.rmtree(self.db_path)
                print(f"文件夹 '{self.db_path}' 已成功删除。")
            except OSError as e:
                print(f"删除文件夹 '{self.db_path}' 时发生错误：{e}")
        else:
            print(f"文件夹 '{self.db_path}' 不存在，无需删除。")

    def update_database(self):
        docs = self.load_documents()
        all_splits = self.split_documents(docs)
        self.clean_db_path()
        vectorstore_to_db = Chroma.from_documents(
            documents=all_splits,
            embedding=self.embedding,
            persist_directory=self.db_path
        )
        print("==========================================\n数据已更新，保存在：", self.db_path)

# 使用示例
processor = DocumentProcessor(data_path, db_path, embedding)
processor.update_database()


