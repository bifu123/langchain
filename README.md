- 文档内容
<img src="./文档内容.png">

- 问题
<img src="./问题.png">

- 问答结果
<img src="./问答结果.png">

## 使用方法
```bash
git clone https://github.com/bifu123/langchain
cd langchain
conda create -n langchain python=3.11
conda activate langchain
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

## 注意事项
```python
oembed_server = OllamaEmbeddings(base_url="http://192.168.66.24:11434", model="nomic-embed-text")
ollama_server = Ollama(base_url='http://192.168.66.26:11434', model="gemma:7b")
```
为内建的ollama服务器，详情参见ollama文档

## 交流讨论
QQ号：415135222
QQ群：222302526 
<<<<<<< HEAD
=======



>>>>>>> c76f85e64042be01890a943f25b87aa0471e3f19
