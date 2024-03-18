from langchain_community.vectorstores import Chroma # 量化文档数据库
from langchain.chains import RetrievalQA #链

from langchain_core.runnables import RunnablePassthrough
from langchain.schema import StrOutputParser
from langchain import hub

import shutil
import os
from config import *


#加载embedding
vectorstore_from_db = Chroma(
    persist_directory = db_path,         # Directory of db
    embedding_function = oembed_server   # Embedding model
)
retriever = vectorstore_from_db.as_retriever()
# print(retriever)



# # 准备问题
# #question=input("请输入问题：")
# question="李四是多少分？"
# docs = vectorstore_from_db.similarity_search(question)
# print("===============将在这些词块中匹配：=================\r\n",docs)


# #运行链
# qachain=RetrievalQA.from_chain_type(ollama_server, retriever=retriever)
# ans = qachain.invoke({"query": "请根据上下文回答：" + question})
# print(ans["result"])




# 设置问题和ChatModel
prompt = hub.pull("rlm/rag-prompt")

# 创建RAG链
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)
rag_chain = (
    {"context": retriever, "question": RunnablePassthrough()}  # 
    | prompt
    | ollama_server
    | StrOutputParser()
)


# 回答问题
def make_answer(question):
    #question = "李四的分数是多少?"
    answer = rag_chain.invoke("请用中文回答我：" + question)
    return answer


while True:
    question = input("请输入问题：")
    ans = make_answer(question)
    print(ans)
    
#清理
vectorstore_from_db.delete_collection()