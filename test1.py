from langchain_community.document_loaders import PyPDFLoader #PDF加载器
from langchain.indexes.vectorstore import VectorstoreIndexCreator
from langchain.text_splitter import RecursiveCharacterTextSplitter # 分割文档
from langchain_community.vectorstores import Chroma # 量化文档数据库
from config import *
import shutil
import os


all_files = []
for root, dirs, files in os.walk("./data"):
    for file in files:
        file_path = os.path.join(root, file)
        file_name, file_extension = os.path.splitext(file)
        all_files.append({"file_full_name": file_path, "file_extension": file_extension})
print(all_files)



loaders = []
for file_name in all_files:
    print(file_name["file_full_name"])
    loaders.append(PyPDFLoader(file_name["file_full_name"]))
    
docs = []
for loader in loaders:
    docs.extend(loader.load())
print(docs)