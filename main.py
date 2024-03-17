from fastapi import FastAPI, File, UploadFile, HTTPException, Request, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
import shutil
from fastapi import status
from dal import *

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

# 设置文件存储目录
file_directory = Path("data")
file_directory.mkdir(parents=True, exist_ok=True)

from fastapi import Request

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):  # 添加 request 参数
    return templates.TemplateResponse("index.html", {"request": request})  # 将 request 添加到上下文中

@app.post("/")
async def dummy_post():
    # 这是一个空的POST路由，用于处理根路径的POST请求
    pass


@app.get("/manager_files", response_class=HTMLResponse)
async def read_files(request: Request):
    files = list(file_directory.glob("*"))
    return templates.TemplateResponse("manager_files.html", {"request": request, "files": files})


@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    # 将文件保存到指定目录
    file_path = file_directory / file.filename
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    #重新量化文档
    processor = DocumentProcessor(data_path, db_path, oembed_server)
    processor.update_database()
    return RedirectResponse(url="/manager_files", status_code=status.HTTP_303_SEE_OTHER)


@app.delete("/delete/{file_name}")
async def delete_file(file_name: str):
    file_path = file_directory / file_name
    if file_path.exists():
        file_path.unlink()
        #重新量化文档
        processor = DocumentProcessor(data_path, db_path, oembed_server)
        processor.update_database()
        return {"message": f"文件 {file_name} 删除成功"}
        
    else:
        raise HTTPException(status_code=404, detail=f"文件 {file_name} 未找到")
    


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)
