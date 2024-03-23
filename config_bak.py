from langchain_community.llms import Ollama #模型
from langchain_community.embeddings import OllamaEmbeddings # 量化文档

#量化文档服务器
oembed_server = OllamaEmbeddings(base_url="http://192.168.66.24:11434", model="nomic-embed-text")
# LLM模型服务器
ollama_server = Ollama(base_url='http://192.168.66.26:11434', model="llava")
#量化后数据保存路径
db_path = "./chroma_db"
#源文档路径
data_path = "./data"