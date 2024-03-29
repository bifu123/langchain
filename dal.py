#################### 导入包 ##################
import os
import shutil

from config import *


# 文档加工
from langchain_community.document_loaders import DirectoryLoader, UnstructuredWordDocumentLoader
from langchain.indexes.vectorstore import VectorstoreIndexCreator
from langchain.text_splitter import RecursiveCharacterTextSplitter # 分割文档
from langchain_community.vectorstores import Chroma # 量化文档数据库

# ollama模型
from langchain_community.embeddings import OllamaEmbeddings # 量化文档
from langchain_community.llms import Ollama #模型

# gemini模型
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI


# 链结构
from langchain.chains import RetrievalQA #链

# 语义检索
from langchain.schema.runnable import RunnableMap
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser




##############站点地图###############
import xml.dom.minidom
import datetime
from urllib import request
from bs4 import BeautifulSoup


##############文件下载###############
import requests


os.environ['GOOGLE_API_KEY'] = GOOGLE_API_KEY #将GOOGLE_API_KEY加载到环境变量中

# 本地量化模型
embedding_ollama = OllamaEmbeddings(
    base_url = embedding_ollama_conf["base_url"], 
    model = embedding_ollama_conf["model"]
) 
# #线上google量化模型
embedding_google = GoogleGenerativeAIEmbeddings(
    model=embedding_google_conf["model"]
) 
# #embedding_google.embed_query("hello, world!")


# 本地语言模型
llm_ollama = Ollama(
    base_url = llm_ollama_conf["base_url"], 
    model = llm_ollama_conf["model"]
)
# 在线语言模型
llm_gemini = ChatGoogleGenerativeAI(
    model="gemini-pro"
) 


# 选择量化模型
if model_choice["embedding"] == "ollama":
    embedding = embedding_ollama
else:
    embedding = embedding_google


# 选择语言模型
if model_choice["llm"] == "ollama":
    llm = llm_ollama
else:
    llm = llm_gemini




######################################
# 量化文档
class DocumentProcessor:
    def __init__(self, data_path, db_path, embedding):
        self.data_path = data_path
        self.db_path = db_path
        self.embedding = embedding

    # 加载文档
    def load_documents(self):
        print("正在加载" + self.data_path + "下的所有文档...")
        loader = DirectoryLoader(self.data_path, show_progress=True, use_multithreading=True)
        return loader.load()
    
    # 分割文档
    def split_documents(self, docs):
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=128)
        return text_splitter.split_documents(docs)
    
    # 删除旧向量
    def clean_db_path(self):
        if os.path.exists(self.db_path) and os.path.isdir(self.db_path):
            try:
                shutil.rmtree(self.db_path)
                print(f"文件夹 '{self.db_path}' 已成功删除。")
            except OSError as e:
                print(f"删除文件夹 '{self.db_path}' 时发生错误：{e}，你需要在程序重新加载且未进行任何任务时进行")
        else:
            print(f"文件夹 '{self.db_path}' 不存在，无需删除。")
    
    # 写入新向量
    def update_database(self):
        docs = self.load_documents()
        all_splits = self.split_documents(docs)
        self.clean_db_path()
        vectorstore_to_db = Chroma.from_documents(
            documents=all_splits,
            embedding=self.embedding,
            persist_directory=self.db_path
        )
        print("==========================================\n数据已更新，保存在：", self.db_path)

# 使用示例
# processor = DocumentProcessor(data_path, db_path, embedding)
# processor.update_database()


# 定义下载文件的函数
def download_file(url: str, file_name: str, download_path: str):
    # 下载文件
    response = requests.get(url)

    if response.status_code == 200:
        # 检查下载目录是否存在，如果不存在则创建
        if not os.path.exists(download_path):
            os.makedirs(download_path)
        
        # 将文件保存到指定路径
        file_path = os.path.join(download_path, file_name)
        with open(file_path, 'wb') as f:
            f.write(response.content)
        
        print(f"File downloaded successfully: {file_path}")
    else:
        print(f"Failed to download file from {url}")


######################################
# 生成站点地图
'''要执行的url'''
URL = 'http://cho.freesky.sbs'

def build_sitemap(url):
    '''所有url列表'''
    URL_LIST = {}

    '''模拟header'''
    HEADER = {
        'Cookie': 'AD_RS_COOKIE=20080917',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \ AppleWeb\Kit/537.36 (KHTML, like Gecko)\ '
                      'Chrome/58.0.3029.110 Safari/537.36'}

    def get_http(url, headers=None, charset='utf8'):
        """
        发送请求
        :param url:
        :param headers:
        :param charset:
        :return:
        """
        if headers is None:
            headers = {}
        try:
            return request.urlopen(request.Request(url=url, headers=headers)).read().decode(charset)
        except Exception:
            pass
        return ''

    def open_url(url):
        """
        打开链接，并返回该链接下的所有链接
        :param url:
        :return:
        """
        soup = BeautifulSoup(get_http(url=url, headers=HEADER), 'html.parser')

        all_a = soup.find_all('a')
        url_list = {}
        for a_i in all_a:
            href = a_i.get('href')
            if href is not None and foreign_chain(href):
                url_list[href] = href
                URL_LIST[href] = href
        return url_list

    def foreign_chain(url):
        """
        验证是否是外链
        :param url:
        :return:
        """
        return url.find(URL) == 0

    '''首页'''
    home_all_url = open_url(URL)

    '''循环首页下的所有链接'''
    if isinstance(home_all_url, dict):
        # 循环首页下的所有链接
        for home_url in home_all_url:
            # 验证是否是本站域名
            if foreign_chain(home_url) is True:
                open_url(home_url)

    URL_LIST_COPY = URL_LIST.copy()

    for copy_i in URL_LIST_COPY:
        open_url(copy_i)

    # 创建文件
    doc = xml.dom.minidom.Document()
    root = doc.createElement('urlset')
    # 设置根节点的属性
    root.setAttribute('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
    root.setAttribute('xmlns', 'http://www.sitemaps.org/schemas/sitemap/0.9')
    root.setAttribute('xsi:schemaLocation', 'http://www.sitemaps.org/schemas/sitemap/0.9 '
                                             'http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd')
    doc.appendChild(root)

    for url_list_i in URL_LIST:
        nodeUrl = doc.createElement('url')
        nodeLoc = doc.createElement('loc')
        nodeLoc.appendChild(doc.createTextNode(str(url_list_i)))
        nodeLastmod = doc.createElement("lastmod")
        nodeLastmod.appendChild(doc.createTextNode(str(datetime.datetime.now().date())))
        nodePriority = doc.createElement("priority")
        nodePriority.appendChild(doc.createTextNode('1.0'))
        nodeUrl.appendChild(nodeLoc)
        nodeUrl.appendChild(nodeLastmod)
        nodeUrl.appendChild(nodePriority)
        root.appendChild(nodeUrl)

    with open('sitemap.xml', 'w', encoding="utf-8") as fp:
        doc.writexml(fp, indent='\t', addindent='\t', newl='\n')

    return {"url":url, "sitemap":"./sitemap.xml"}

# # 调用函数并输出结果
# print(build_sitemap(URL))



