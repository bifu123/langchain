from langchain_community.document_loaders import PyPDFLoader #PDF加载器
from langchain.indexes.vectorstore import VectorstoreIndexCreator
from langchain.text_splitter import RecursiveCharacterTextSplitter # 分割文档
from langchain_community.vectorstores import Chroma # 量化文档数据库
from config import *
import shutil
import os



# 加载./data下的所有文档
def get_all_files(data_path):
    """
    递归遍历指定目录下的所有文件，并返回文件路径列表
    """
    all_files = []
    for root, dirs, files in os.walk(data_path):
        for file in files:
            file_path = os.path.join(root, file)
            all_files.append(file_path)
    return all_files

loaders = []
for file_name in get_all_files(data_path):
    loaders.append(PyPDFLoader(file_name))
    
docs = []
for loader in loaders:
    docs.extend(loader.load())
# print(len(docs))



# 分割文档
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
all_splits = text_splitter.split_documents(docs)
# print(all_splits)



# 检查文件夹是否存在
if os.path.exists(db_path) and os.path.isdir(db_path):
    # 删除文件夹及其所有内容
    try:
        shutil.rmtree(db_path)
        print(f"文件夹 '{db_path}' 已成功删除。")
    except OSError as e:
        print(f"删除文件夹 '{db_path}' 时发生错误：{e}")
else:
    print(f"文件夹 '{db_path}' 不存在，无需删除。")



#量化文档存入数据库
vectorstore_to_db = Chroma.from_documents(
    documents = all_splits,           # Data
    embedding = oembed_server,        # Embedding model
    persist_directory = db_path       # Directory to save data
)
print("数据己更新，保存在：",db_path)