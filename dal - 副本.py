#################### 导入包 ##################
# 文档加工
from langchain_community.document_loaders import DirectoryLoader, UnstructuredWordDocumentLoader
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

from config import *


######################################
# 量化文档
######################################
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
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=128)
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
# processor = DocumentProcessor(data_path, db_path, oembed_server)
# processor.update_database()




######################################
# 生成站点地图
######################################
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



