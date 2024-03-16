from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
from starlette.requests import Request
from starlette.responses import StreamingResponse
import os
from dal import *

app = FastAPI()

file_upload_path = "./data"


# HTML form for uploading files
html_form_bakjson = """
<!DOCTYPE html>
<html>
    <head>
        <title>文件上传表单</title>
    </head>
    <body>
        <h2>上传文件</h2>
        <form action="/upload" method="post" enctype="multipart/form-data">
            <label for="file">选择文件:</label>
            <input type="file" id="file" name="file"><br><br>
            <br><br>
            <button type="submit">上传</button>
        </form>
    </body>
</html>
"""

html_form = """
<!DOCTYPE html>
<html>
    <head>
        <title>文件上传表单</title>
    </head>
    <body>
        <h2>上传文件</h2>
        <form action="/upload" method="post" enctype="multipart/form-data">
            <label for="file">选择文件:</label>
            <input type="file" id="file" name="file"><br><br>
            <progress id="progressBar" value="0" max="100" style="width: 300px;"></progress>
            <br><br>
            <button type="submit">上传</button>
        </form>

        <script>
            const form = document.querySelector('form');
            const progressBar = document.querySelector('#progressBar');

            form.addEventListener('submit', async (e) => {
                e.preventDefault();
                const formData = new FormData(form);
                const response = await fetch('/upload', {
                    method: 'POST',
                    body: formData,
                });
                const reader = response.body.getReader();
                const contentLength = +response.headers.get('Content-Length');

                let receivedLength = 0;
                while (true) {
                    const { done, value } = await reader.read();

                    if (done) {
                        break;
                    }

                    receivedLength += value.length;
                    progressBar.value = (receivedLength / contentLength) * 100;

                    console.log(`Received ${receivedLength} of ${contentLength}`);
                }
            });
        </script>
    </body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def read_form():
    return HTMLResponse(content=html_form, status_code=200)

async def save_file(file: UploadFile, file_path: str):
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)

@app.post("/upload")
async def upload_file(request: Request, file: UploadFile = File(...)):
    # 设置文件保存路径
    file_upload_target_path = os.path.join(file_upload_path, file.filename)
    await save_file(file, file_upload_target_path)
    # 量化文档
    processor = DocumentProcessor(data_path, db_path, oembed_server)
    processor.update_database()
    return {"filename": file.filename, "status": "ok"}

if __name__ == "__main__":
    import nest_asyncio
    nest_asyncio.apply()
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
