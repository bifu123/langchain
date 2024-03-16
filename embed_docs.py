#########################################
#当文档数较多时，请注意加大chunk_size=800的值
#########################################
from config import *
import os
import shutil
from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma

class DocumentProcessor:
    def __init__(self, data_path, db_path, oembed_server):
        self.data_path = data_path
        self.db_path = db_path
        self.oembed_server = oembed_server

    def load_documents(self):
        print("正在加载" + self.data_path + "下的所有文档...")
        loader = DirectoryLoader(self.data_path, show_progress=True, use_multithreading=True)
        return loader.load()

    def split_documents(self, docs):
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=0)
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
            embedding=self.oembed_server,
            persist_directory=self.db_path
        )
        print("==========================================\n数据已更新，保存在：", self.db_path)

# 使用示例
processor = DocumentProcessor(data_path, db_path, oembed_server)
processor.update_database()




# from langchain_community.document_loaders import PyPDFLoader #PDF加载器
# from langchain.indexes.vectorstore import VectorstoreIndexCreator
# from langchain.text_splitter import RecursiveCharacterTextSplitter # 分割文档
# from langchain_community.vectorstores import Chroma # 量化文档数据库
# from config import *
# import shutil
# import os



# # 加载./data下的所有文档
# def get_all_files(data_path):
#     """
#     递归遍历指定目录下的所有文件，并返回文件路径列表
#     """
#     all_files = []
#     for root, dirs, files in os.walk(data_path):
#         for file in files:
#             file_path = os.path.join(root, file)
#             all_files.append(file_path)
#     return all_files

# loaders = []
# for file_name in get_all_files(data_path):
#     loaders.append(PyPDFLoader(file_name))
    
# docs = []
# for loader in loaders:
#     docs.extend(loader.load())
# # print(len(docs))



# # 分割文档
# text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
# all_splits = text_splitter.split_documents(docs)
# # print(all_splits)



# # 检查文件夹是否存在
# if os.path.exists(db_path) and os.path.isdir(db_path):
#     # 删除文件夹及其所有内容
#     try:
#         shutil.rmtree(db_path)
#         print(f"文件夹 '{db_path}' 已成功删除。")
#     except OSError as e:
#         print(f"删除文件夹 '{db_path}' 时发生错误：{e}")
# else:
#     print(f"文件夹 '{db_path}' 不存在，无需删除。")



# #量化文档存入数据库
# vectorstore_to_db = Chroma.from_documents(
#     documents = all_splits,           # Data
#     embedding = oembed_server,        # Embedding model
#     persist_directory = db_path       # Directory to save data
# )
# print("数据己更新，保存在：",db_path)