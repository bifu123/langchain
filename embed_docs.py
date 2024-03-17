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
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=200)
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


