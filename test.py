from langchain_community.document_loaders import PyPDFLoader #PDF加载器
from langchain.indexes.vectorstore import VectorstoreIndexCreator
from langchain.text_splitter import RecursiveCharacterTextSplitter # 分割文档
from langchain_community.embeddings import OllamaEmbeddings # 量化文档
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma # 量化文档数据库
from langchain_community.llms import Ollama #模型
from langchain.chains import RetrievalQA #链
import os
from dotenv import load_dotenv

load_dotenv()

file_path = "./data/tesla_p40.pdf"
db_path= "./chroma_db"

def get_index_path(index_name):
    return os.path.join(db_path, index_name)

def load_pdf_and_save_to_index(file_path, index_name):
    loader = PyPDFLoader(file_path)
    index = VectorstoreIndexCreator(vectorstore_kwargs={"persist_directory": get_index_path(index_name)}).from_loaders([loader])
    index.vectorstore.persist()

load_pdf_and_save_to_index(file_path, "test")
