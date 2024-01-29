from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import JSONResponse
from starlette.templating import Jinja2Templates
from pytesseract import image_to_string
from PIL import Image
import io

app = FastAPI()

# Создайте экземпляр класса Jinja2Templates и укажите папку с шаблонами
templates = Jinja2Templates(directory="app/templates")


@app.get("/")
async def index(request: Request):
    # Отправьте шаблон вместо HTML файла
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/uploadfile/")
async def upload_file(file: UploadFile):
    try:
        # Считывание изображения из запроса и распознавание текста
        img = Image.open(io.BytesIO(file.file.read()))
        text = image_to_string(img, lang="rus+eng")
        print(text)
        return JSONResponse(content={"text": text}, status_code=200)
    except Exception as e:
        print(e)
        return JSONResponse(content={"error": "File processing failed"}, status_code=500)

