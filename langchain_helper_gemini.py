#################### 导入包 ##################
# 文档加工
from langchain_community.document_loaders import PyPDFLoader #PDF加载器
from langchain.indexes.vectorstore import VectorstoreIndexCreator
from langchain.text_splitter import RecursiveCharacterTextSplitter # 分割文档
from langchain_community.vectorstores import Chroma # 量化文档数据库

# ollama模型
from langchain_community.embeddings import OllamaEmbeddings # 量化文档
from langchain_community.llms import Ollama #模型

# 链结构
from langchain.chains import RetrievalQA #链

# gemini模型
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI

# 语义检索
from langchain.schema.runnable import RunnableMap
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser

import os
import shutil


# 本地文档
file_path = "./data/tesla_p40.pdf"
# 量化数据存储路径
db_path = "./chroma_db"

os.environ['GOOGLE_API_KEY'] = '你的GEMINI API' #将GOOGLE_API_KEY加载到环境变量中


# 量化模型
#embedding = OllamaEmbeddings(base_url="http://192.168.66.24:11434", model="nomic-embed-text") #线上google量化模型
embedding = GoogleGenerativeAIEmbeddings(model="models/embedding-001") #本地ollama量化模型
#embedding.embed_query("hello, world!")
'''
不同的量化模型量化结果是不一样的，原则是你选择哪家的量化模型，读取时必须使用相同的量化模型逆向读取，否则推理出错
'''


# 线上模型
#llm = Ollama(base_url='http://192.168.66.26:11434', model="test:7b") #本地ollama语言模型
llm = ChatGoogleGenerativeAI(model="gemini-pro") #线上google gemini语言模型



# 加载文档
loader = PyPDFLoader(file_path)
docs = loader.load()
# print(docs)


# 分割文档
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=128)
all_splits = text_splitter.split_documents(docs)
# print(all_splits)


#如果存在数据库目录则先删除
def delete_chroma_db(db_path):
    if os.path.exists(db_path):
        if os.path.isfile(db_path):
            os.remove(db_path)
            print("File 'chroma_db' deleted.")
        elif os.path.isdir(db_path):
            shutil.rmtree(db_path)
            print("Directory 'chroma_db' deleted.")
    else:
        print("File or directory 'chroma_db' does not exist.")

# 调用函数以删除 'chroma_db'
delete_chroma_db(db_path)

#量化文档存入数据库
vectorstore_to_db = Chroma.from_documents(
    documents = all_splits,           # Data
    embedding = embedding,        # Embedding model
    persist_directory = db_path       # Directory to save data
)


#加载embedding
vectorstore_from_db = Chroma(
    persist_directory = db_path,         # Directory of db
    embedding_function = embedding   # Embedding model
)
print(vectorstore_from_db)



# # 准备问题
# question="最大显存是多少？"
# docs = vectorstore_from_db.similarity_search(question)
# #print(docs)

# #运行链
# qachain=RetrievalQA.from_chain_type(llm, retriever=vectorstore_from_db.as_retriever())
# ans = qachain.invoke({"query": "请用中文回答我：" + question})
# print(ans["result"])
'''
以上写法并不兼容线上模型，仅对本地模型有用
'''



#################### 问答推理 ##################
#创建prompt模板
template = """Answer the question a full sentence, based only on the following context and tel me the answer in Chinese:
{context}
Question: {question}
"""
#由模板生成prompt
prompt = ChatPromptTemplate.from_template(template) 


retriever=vectorstore_from_db.as_retriever()
output_parser = StrOutputParser()
query = {"question": "最大显存是多少?"}
 
#创建chain
chain = RunnableMap({
    "context": lambda x: retriever.get_relevant_documents(x["question"]),
    "question": RunnablePassthrough()
}) | prompt | llm | output_parser
 
print(chain.invoke(query))
