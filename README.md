- 结构示意
<img src="./images/文档对话示意.jpg">

- 文档内容
<img src="./images/文档内容.png">

- 问题
<img src="./images/问题.png">

- 问答结果
<img src="./images/问答结果.png">

## 使用方法
### 安装 Visual Studio Build Tools 
- 您可以从 Microsoft 的官方网站上下载 Visual Studio Build Tools。以下是下载的步骤：

- 打开您的 Web 浏览器并访问 Microsoft 的 Visual Studio 下载页面：https://visualstudio.microsoft.com/downloads/。

- 在该页面上，您会看到不同版本的 Visual Studio 可供下载。您可以滚动页面找到 "All downloads" 部分，或者直接在搜索栏中搜索 "Build Tools"。

- 找到 "Tools for Visual Studio" 或者 "Build Tools for Visual Studio"。点击进入该部分。

- 您会看到不同版本的 Visual Studio Build Tools。选择您想要的版本，并点击相应的下载按钮。

- 在下载页面上，您可能需要登录您的 Microsoft 帐户。如果您还没有 Microsoft 帐户，可以免费注册一个。

- 下载完成后，运行安装程序，并按照提示完成安装过程。您可以根据您的需要选择要安装的组件和工作负载。

- 请注意，下载的过程可能会因您所在的地区、网络速度和其他因素而有所不同。确保您的计算机满足 Visual Studio Build Tools 的系统要求，并在安装之前备份重要数据。

### 安装环境依赖
```bash
git clone https://github.com/bifu123/langchain
cd langchain
conda create -n langchain python=3.11
conda activate langchain
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```
- 修改配置文件
编辑 config.py 各项配置，关于 ollama 可参见
ollama入门：https://github.com/ollama/ollama <br>
ollama文档：https://github.com/ollama/ollama/tree/main/docs

- 量化文档
```bash
python embed_docs.py
```

- 执行问答
```bash
python langchain_helper.py
```

- 文档管理
```bash
python main.py
```
然后访问 http://ip:8001
<br>*** 上传或删除文档时都会触发自动量化文档 ***

## 交流讨论
QQ号：415135222
QQ群：222302526 

<hr>

*** 2023-3-23 重要更新 ***
- 更正了依赖环境安装错误
- 增加gemini api的支持。

*** 2023-3-19 重要更新 ***
- 模型首选chinese-alpaca-llama2：https://github.com/ymcui/Chinese-LLaMA-Alpaca-2，中文理解能力强些。导入方法详见ollama入门文档。还没试过 chatGLM,不知道效果如何。
- 增加对 world 、excel 等办公文档的支持。

*** 2023-3-18 重要更新 ***
- 增加从 web 页上传和管理文档并自动量化功能