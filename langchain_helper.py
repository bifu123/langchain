from langchain_community.vectorstores import Chroma # 量化文档数据库
from langchain.chains import RetrievalQA #链
import shutil
import os
from config import *


#加载embedding
vectorstore_from_db = Chroma(
    persist_directory = db_path,         # Directory of db
    embedding_function = oembed_server   # Embedding model
)
print(vectorstore_from_db)


while True:
    # 准备问题
    question=input("请输入问题：")
    # question="最大显存是多少？"
    docs = vectorstore_from_db.similarity_search(question)
    #print(docs)


    #运行链
    qachain=RetrievalQA.from_chain_type(ollama_server, retriever=vectorstore_from_db.as_retriever())
    ans = qachain.invoke({"query": "请用中文回答我：" + question})
    print(ans["result"])