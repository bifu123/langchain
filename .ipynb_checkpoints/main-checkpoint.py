
# pip install fastap
# pip install "uvicorn[standard]"
# uvicorn main:app --reload
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return "hello world"
    
    
