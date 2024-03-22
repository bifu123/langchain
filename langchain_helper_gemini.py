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


#################### 定义常量 ##################
# 文档路径
file_path = "./data/tesla_p40.pdf"
# 矢量存储路径
db_path = "./chroma_db"

#################### 准备模型 ##################
# 将GOOGLE_API_KEY加载到环境变量中
os.environ['GOOGLE_API_KEY'] = '你的GEMINI API'
# 量化模型
embedding = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
# embedding.embed_query("hello, world!")
# 推理模型
llm = ChatGoogleGenerativeAI(model="gemini-pro")

# embedding = OllamaEmbeddings(base_url="http://192.168.66.24:11434", model="nomic-embed-text")
# llm = Ollama(base_url='http://192.168.66.26:11434', model="gemma:7b")

#################### 加载文档 ##################
# 加载文档
loader = PyPDFLoader(file_path)
docs = loader.load()
print(docs)

#################### 分割文档 ##################
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
all_splits = text_splitter.split_documents(docs)
print(all_splits)

#################### 量化存入 ##################
vectorstore_from_db = Chroma(
    persist_directory = db_path,         # Directory of db
    embedding_function = embedding   # Embedding model
)
print(vectorstore_from_db)

#################### 问答推理 ##################
# 创建prompt模板
template = """Answer the question a full sentence, based only on the following context and in Chinese:
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
