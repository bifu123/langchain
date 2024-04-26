import chromadb
import json
import time




from langchain_community.document_loaders import PyPDFLoader #PDF加载器
from langchain.indexes.vectorstore import VectorstoreIndexCreator
from langchain.text_splitter import RecursiveCharacterTextSplitter # 分割文档
from langchain_community.embeddings import OllamaEmbeddings # 量化文档
from langchain_community.vectorstores import Chroma # 量化文档数据库
from langchain_community.llms import Ollama #模型
from langchain.chains import RetrievalQA #链

from langchain_community.embeddings import CohereEmbeddings 
from langchain_community.vectorstores import FAISS

import os
os.environ["COHERE_API_KEY"] = "YOUR COHERE_API_KEY" # Cohere这家公司是加拿大的，可以申请使用他们的在线向量重排模型 API，地址是：https://dashboard.cohere.ai/ 也可以本地架设，huggingface有很多。





file_path = "./data/中华人民共和国公司法.pdf"
oembed_server = OllamaEmbeddings(base_url="http://192.168.66.24:11434", model="mofanke/dmeta-embedding-zh")
ollama_server = Ollama(base_url='http://192.168.66.26:11434', model="llama3:8b")
db_path = "./chroma_db"



def pretty_print_docs(docs):
    print(
        f"\n{'-' * 100}\n".join(
            [
                f"Document {i+1}:\n\n{d.page_content}\nMetadata: {d.metadata}"
                for i, d in enumerate(docs)
            ]
        )
    )



# # 加载文档
# loader = PyPDFLoader(file_path)
# docs = loader.load()
# # print(docs)


# # 分割文档
# text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
# all_splits = text_splitter.split_documents(docs)
# # print(all_splits)


# #量化文档存入数据库
# vectorstore_to_db = Chroma.from_documents(
#     documents = all_splits,           # Data
#     embedding = oembed_server,        # Embedding model
#     persist_directory = db_path       # Directory to save data
# )

#加载embedding
vectorstore_from_db = Chroma(
    persist_directory = db_path,         # Directory of db
    embedding_function = oembed_server   # Embedding model
)
# print(vectorstore_from_db)

# 准备问题
question="公司经理从事与公司有竟争性的商业项目，违反了哪些条款，应该怎样惩罚？"

# 把问题带入向量中检索
docs = vectorstore_from_db.similarity_search(question)
print("\n重排前召回：")
pretty_print_docs(docs)
# print(docs)

# 检索结果
retriever=vectorstore_from_db.as_retriever()
# print(retriever)






print("\n******************* 未进行向量重排 ********************\n")
start_time = time.time()
# 定义一个链、检索内容为未重排的向量
qachain = RetrievalQA.from_chain_type(ollama_server, retriever=retriever)
# 检索答案
ans = qachain.invoke("请用中文回答我：" + question)
# 输出结果
print(f'\n问题：{question}\n答案：{ans["result"]}\n')
# 结束计时
end_time = time.time()
# 计算执行耗时
execution_time = end_time - start_time
print("\n程序执行耗时：", execution_time, "秒")




print("\n************************ 向量重排 *********************\n")
start_time = time.time()
from langchain.retrievers.contextual_compression import ContextualCompressionRetriever
from langchain_cohere import CohereRerank
from langchain_community.llms import Cohere
# 定义重排模型
llm = Cohere(temperature=0)
compressor = CohereRerank()
compression_retriever = ContextualCompressionRetriever(
    base_compressor = compressor, 
    base_retriever = retriever # 未重排前的检索结果
)
# 用重排模型对向量进行重排
compressed_docs = compression_retriever.invoke(question)
print("\n重排后召回：")
pretty_print_docs(compressed_docs)
# # 用Cohere的LLM定义一个新链
# rerank_chain = RetrievalQA.from_chain_type( 
#     llm=Cohere(temperature=0), retriever=compression_retriever
# )
# 用本地LLM定义一个新链
rerank_chain = RetrievalQA.from_chain_type(ollama_server, retriever=compression_retriever)
# 检索答案
ans_rerank = rerank_chain("请用中文回答我：" + question)
# 输出结果
print(f'\n问题：{question}\n答案：{ans_rerank["result"]}\n')
# 结束计时
end_time = time.time()
# 计算执行耗时
execution_time = end_time - start_time
print("\n程序执行耗时：", execution_time, "秒")
