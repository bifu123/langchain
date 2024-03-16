# from langchain_community.document_loaders import DirectoryLoader

# from langchain.indexes.vectorstore import VectorstoreIndexCreator
# from langchain.text_splitter import RecursiveCharacterTextSplitter # 分割文档
# from langchain_community.vectorstores import Chroma # 量化文档数据库
# from config import *
# import shutil
# import os



# loader = DirectoryLoader('./data', show_progress=True, use_multithreading=True)
# docs = loader.load()
# print(docs)

############# pdf #############
#pip install pypdf
from langchain_community.document_loaders import PyPDFLoader #PDF加载器
# PyPDFLoader(file_name)

############# csv #############
from langchain_community.document_loaders.csv_loader import CSVLoader
# loader = CSVLoader(file_path='./example_data/mlb_teams_2012.csv')

############# html #############
from langchain_community.document_loaders import UnstructuredHTMLLoader
# loader = UnstructuredHTMLLoader("example_data/fake-content.html")

############# json #############
# #!pip install jq
from langchain_community.document_loaders import JSONLoader
# file_path='./example_data/facebook_chat.json'
# data = json.loads(Path(file_path).read_text())

############# Markdown #############
# !pip install unstructured > /dev/null
from langchain_community.document_loaders import UnstructuredMarkdownLoader
# markdown_path = "../../../../../README.md"
# loader = UnstructuredMarkdownLoader(markdown_path)

from langchain.indexes.vectorstore import VectorstoreIndexCreator
from langchain.text_splitter import RecursiveCharacterTextSplitter # 分割文档
from langchain_community.vectorstores import Chroma # 量化文档数据库
from config import *
import shutil
import os



# 加载./data下的所有文档
def get_all_files(data_path):
    """
    递归遍历指定目录下的所有文件，并返回文件路径列表
    """
    all_files = []
    for root, dirs, files in os.walk(data_path):
        for file in files:
            file_path = os.path.join(root, file)
            all_files.append(file_path)
    return all_files

loaders = []
for file_name in get_all_files(data_path):
    loaders.append(PyPDFLoader(file_name))
    
docs = []
for loader in loaders:
    docs.extend(loader.load())
print(docs)



# 分割文档
text_splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=0)
all_splits = text_splitter.split_documents(docs)
# print(all_splits)



# 检查文件夹是否存在
if os.path.exists(db_path) and os.path.isdir(db_path):
    # 删除文件夹及其所有内容
    try:
        shutil.rmtree(db_path)
        print(f"文件夹 '{db_path}' 已成功删除。")
    except OSError as e:
        print(f"删除文件夹 '{db_path}' 时发生错误：{e}")
else:
    print(f"文件夹 '{db_path}' 不存在，无需删除。")



#量化文档存入数据库
vectorstore_to_db = Chroma.from_documents(
    documents = all_splits,           # Data
    embedding = oembed_server,        # Embedding model
    persist_directory = db_path       # Directory to save data
)
print("数据己更新，保存在：",db_path)