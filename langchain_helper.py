import langchain
from langchain_community.document_loaders import PyPDFLoader
from langchain.indexes.vectorstore import VectorstoreIndexCreator

# 加载文档
file_path = "./data/tesla_p40.pdf"
# !pip install pypdf
loader = PyPDFLoader(file_path)
docs = loader.load()
# print(docs)

# 分割文档
from langchain.text_splitter import RecursiveCharacterTextSplitter
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
all_splits = text_splitter.split_documents(docs)
# print(all_splits)

# 量化文档存入数据库
from langchain.embeddings import OllamaEmbeddings
from langchain.vectorstores import Chroma
oembed = OllamaEmbeddings(base_url="http://192.168.66.24:11434", model="nomic-embed-text")
vectorstore = Chroma.from_documents(documents=all_splits, embedding=oembed)
# print(vectorstore)


# 准备问题
question="最大显存是多？"
# question="Who is Neleus and who is in Neleus' family?"
docs = vectorstore.similarity_search(question)
#print(docs)


# 准备模型
#from langchain.llms import Ollama 以弃用
from langchain_community.llms import Ollama
ollama = Ollama(base_url='http://192.168.66.24:11434',
model="gemma:7b")
# print(ollama("你好"))


from langchain.chains import RetrievalQA
qachain=RetrievalQA.from_chain_type(ollama, retriever=vectorstore.as_retriever())
ans = qachain.invoke({"query": "请用中文回答我：" + question})
print(ans["result"])
