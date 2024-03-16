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
- 配置文件
编辑config.py
```python
oembed_server = OllamaEmbeddings(base_url="http://192.168.66.24:11434", model="nomic-embed-text")
ollama_server = Ollama(base_url='http://192.168.66.26:11434', model="gemma:7b")
```
oembed_server、ollama_server 为内建的ollama服务器，详情参见ollama文档

- 量化文档
```bash
python embed_docs.py
```
- 注意：当文档数较多时，请注意加大 embed_docs.py 中 chunk_size=800 的值

- 执行问答
```bash
python langchain_helper.py
```

## 交流讨论
QQ号：415135222
QQ群：222302526 