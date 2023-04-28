import os
import io
import traceback
import json
from config import DataConfig
from typing import Optional, List, Any
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel
import uvicorn
from utils import encode_image_to_base64, save_image_from_base64, simplify_list
from get_pipeline import image2Image, text2Image
from image2image import main as i2i_main
from text2image import main as t2i_main
from stylized_face import main as face_main


class Image2ImageRequest(BaseModel):
    request_id: str
    style: str
    image: Any

class Text2ImageRequest(BaseModel):
    request_id: str
    sequence: str
    style: Optional[str] = "太乙通用"
    language: Optional[str] = "chinese"

app = FastAPI()

@app.post("/image2image")
async def i2i(data: dict):
    if "request_id" not in data or "image" not in data or "style" not in data:
        return "Request Param Error"

    try:
        request_id = data["request_id"]
        style = data["style"]
        image = data["image"]
        img_path = None
        if isinstance(image, list):
            img_path = i2i_main(
                image2image=image2Image,
                request_id=request_id, 
                style=style, 
                image_list=image
            )

        else:#base64格式
            image_save_path = os.path.join(
                DataConfig.input_images,
                request_id + "_" + style + ".png"
            )
            save_image_from_base64(image, output_path=image_save_path)

            img_path = i2i_main(
                image2image=image2Image,
                request_id=request_id, 
                style=style, 
                image_list=[image_save_path]
            )

        if img_path is not None:
            return {
                "text": "Image2Image, successfully",
                #"base64": encode_image_to_base64(img_path),
                "url": img_path,
                "absUrl": os.path.abspath(img_path)
            }
        # None
        return {"text": "Image2Image, exception"}
    
    except Exception:
        traceback.print_exc()
        return {"text": "Image2Image, exception"}

@app.post("/style-face")
async def i2i(data: dict):
    if "request_id" not in data or "image" not in data:
        return "Request Param Error"

    try:
        request_id = data["request_id"]
        image = data["image"]
        face_path_list = []
        if isinstance(image, list):
            face_path_list = face_main(
                image2image=image2Image,
                request_id=request_id,
                image_list=image)

        else:#base64格式
            image_save_path = os.path.join(
                DataConfig.input_images,
                request_id + ".png"
            )
            save_image_from_base64(image, output_path=image_save_path)

            face_path_list = face_main(
                image2image=image2Image,
                request_id=request_id,
                image_list=[image_save_path])

        face_path_list = simplify_list(face_path_list)
        if face_path_list:
            return {
                "text": "Style Face, successfully",
                #"base64": encode_image_to_base64(img_path),
                "urls": face_path_list,
                "absUrls": [os.path.abspath(img_path) for img_path in face_path_list]
            }
        # []
        return {"text": "Style Face, exception"}
    
    except Exception:
        traceback.print_exc()
        return {"text": "Style Face, exception"}

@app.post("/text2image")
async def t2i(data: dict):
    if "request_id" not in data or "sequence" not in data:
        return "Request Param Error"
    
    if "style" not in data:
        style = "太乙通用"
    
    if "language" not in data:
        language = "chinese"

    try:
        request_id = data["request_id"]
        sequence = data["sequence"]
        style = data.get("style", "太乙通用")
        language = data.get("language", "chinese")

        img_path = t2i_main(
            text2image=text2Image,
            request_id=request_id,
            style=style,
            sequence=sequence,
            language=language
        )
        
        if img_path is not None:
            return {
                "text": "Text2Image, successfully",
                #"base64": encode_image_to_base64(img_path),
                "url": img_path,
                "absUrl": os.path.abspath(img_path)
            }
        # None
        return {"text": "Text2Image, exception"}
    
    except Exception:
        traceback.print_exc()
        return {"text": "Text2Image, exception"}

@app.post("/status")
async def status(data: dict):
    print(data)
    return {"text": "magic image serivce is running, successfully"}

@app.post("/downloadPost")
async def download_file_byFile(data: dict):
    if "file_path" not in data:
        return None
    if not os.path.exists(data["file_path"]):
        return None
    return FileResponse(data["file_path"])

@app.get('/download')
async def download_file(file_path: str):
    if not os.path.exists(file_path):
        return None
    return FileResponse(file_path)

@app.post('/feedback')
async def download_file(data: dict):
    if "star" not in data or "suggestion" not in data or "absUrl" not in data:
        return "Request Param Error"

    save_dir = DataConfig.feedback
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)
    file_path = os.path.join(save_dir, data["absUrl"].split("/")[-1] + ".txt")
    star = str(data["star"])
    suggestion = data["suggestion"]
    with open(file_path, "w") as fw:
        fw.write(f"{star}\t{suggestion}")

    return "Feedback, successfully"

if __name__ == '__main__':
    # http, port is 8000
    uvicorn.run(app, host="0.0.0.0", port=8000)
    
