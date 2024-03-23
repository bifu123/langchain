from fastapi import FastAPI, File, UploadFile, HTTPException, Request, Response
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse

from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
import shutil
from fastapi import status
from fastapi import Request


from dal import *



app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


templates = Jinja2Templates(directory="templates")


# 设置文件存储目录
file_directory = Path("data")
file_directory.mkdir(parents=True, exist_ok=True)



@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):  # 添加 request 参数
    return templates.TemplateResponse("index.html", {"request": request})  # 将 request 添加到上下文中

@app.post("/")
async def dummy_post():
    # 这是一个空的POST路由，用于处理根路径的POST请求
    pass




# 显示文件夹下所有文件的函数
def get_files_in_directory(directory: Path):
    files = []
    for item in directory.iterdir():
        if item.is_file():
            files.append(str(item.resolve()))  # 将文件的绝对路径添加到列表中
            #files.append(str(item.relative_to(file_directory)))  # 将文件的相对路径添加到列表中
        elif item.is_dir():
            files.extend(get_files_in_directory(item))  # 递归获取子文件夹中的文件
    return files

# 管理文档
@app.get("/manager_files")
async def read_files(request: Request):
    files_names = get_files_in_directory(file_directory)

    files = list(file_directory.glob("*"))

    # 获取文件名列表
    # files_names = [file.name for file in file_directory.glob("*")]  
    # 获取名为 "from" 的查询参数
    from_value = request.query_params.get("type", None)  
    if from_value == "api":
        return JSONResponse(content={"files": files_names})
    
    else:
        return templates.TemplateResponse("manager_files.html", {"request": request, "files": files})


# 从WEB上传文档
@app.post("/upload/")
async def upload_file(request: Request, file: UploadFile = File(...)):
    # 将文件保存到指定目录
    file_path = file_directory / file.filename
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    #重新量化文档
    processor = DocumentProcessor(data_path, db_path, embedding)
    processor.update_database()
    # 跳转
    return RedirectResponse(url="/manager_files", status_code=status.HTTP_303_SEE_OTHER)


# 删除文档
@app.delete("/delete/{file_name}")
async def delete_file(file_name: str):
    file_path = file_directory / file_name
    if file_path.exists():
        file_path.unlink()
        #重新量化文档
        processor = DocumentProcessor(data_path, db_path, embedding)
        processor.update_database()
        return {"message": f"文件 {file_name} 删除成功"}
        
    else:
        raise HTTPException(status_code=404, detail=f"文件 {file_name} 未找到")
    

# 从QQ接收文档
@app.get("/upload_api/")
async def upload_file(request: Request):
    # 将文件保存到指定目录

    
    # 从请求数据中获取参数值
    file_name = request.query_params.get("file_name", None)
    file_url = request.query_params.get("file_url", None)
    file_user = request.query_params.get("file_user", None)

    print(file_url)
    
    # 下载文档到用户文件夹
    file_save_path = os.path.join(data_path, file_user)
    download_file(file_url, file_name, file_save_path)

    #重新量化文档
    processor = DocumentProcessor(data_path, db_path, embedding)
    processor.update_database()

    return JSONResponse(content={"msg": "文档量化完成"})






if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)
