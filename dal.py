from langchain_community.document_loaders import PyPDFLoader #PDF加载器
from langchain.indexes.vectorstore import VectorstoreIndexCreator
from langchain.text_splitter import RecursiveCharacterTextSplitter # 分割文档
from langchain_community.vectorstores import Chroma # 量化文档数据库
from config import *
import shutil
import os


# 文档操作类：将./data下所有PDF文件全部量化保存到./choma_db
class DocumentProcessor:
    def __init__(self, data_path, db_path, oembed_server):
        self.data_path = data_path
        self.db_path = db_path
        self.oembed_server = oembed_server

    def get_all_files(self):
        """
        递归遍历指定目录下的所有文件，并返回文件路径列表
        """
        all_files = []
        for root, dirs, files in os.walk(self.data_path):
            for file in files:
                file_path = os.path.join(root, file)
                all_files.append(file_path)
                print(all_files)
        return all_files

    def load_documents(self):
        loaders = []
        for file_name in self.get_all_files():
            loaders.append(PyPDFLoader(file_name))

        docs = []
        for loader in loaders:
            docs.extend(loader.load())
        return docs

    def split_documents(self, docs):
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
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
        print("数据已更新，保存在：", self.db_path)

# 使用示例
processor = DocumentProcessor(data_path, db_path, oembed_server) #实列化类
processor.update_database() #执行类的方法