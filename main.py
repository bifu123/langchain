
# # pip install fastap
# # pip install "uvicorn[standard]"
# # uvicorn main:app --reload
# from fastapi import FastAPI

# app = FastAPI()

# @app.get("/")
# def read_root():
#     return "hello world"
    
    
    
from langchain.llms import Ollama
# 翻译引擎
ollama = Ollama(base_url='http://192.168.66.26:11434',
model="gemma:7b")
print(ollama("你好"))