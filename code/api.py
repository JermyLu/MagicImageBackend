import os
import traceback
import json
import ssl
from typing import Optional, List, Any
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.routing import APIRoute
from pydantic import BaseModel
import uvicorn
from utils import encode_image_to_base64, save_image_from_base64
from get_pipeline import Image2Image, Text2Image
from image2image import main as i2i_main
from text2image import main as t2i_main

image2Image = Image2Image()
text2Image = Text2Image()

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
        if isinstance(image, list):
            i2i_main(
                image2image=image2Image,
                request_id=request_id, 
                style=style, 
                image_list=image
            )

        else:#base64格式
            image_save_path = os.path.join(
                r"../input_images",
                request_id + "_" + style + ".png"
            )
            save_image_from_base64(image, output_path=image_save_path)

            i2i_main(
                image2image=image2Image,
                request_id=request_id, 
                style=style, 
                image_list=[image_save_path]
            )

        return "Image2Image, successfully"
    
    except Exception:
        traceback.print_exc()
        return "Image2Image, error"

# @app.post("/text2image")
# async def t2i(item: Text2ImageRequest):
#     t2i_main(
#         text2image=text2Image,
#         request_id=item.request_id,
#         style=item.style,
#         sequence=item.sequence,
#         language=item.language
#     )

#     return item

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

        t2i_main(
            text2image=text2Image,
            request_id=request_id,
            style=style,
            sequence=sequence,
            language=language
        )
        return "Text2Image, successfully"
    
    except Exception:
        traceback.print_exc()
        return "Image2Image, error"

@app.post("/status")
async def status(data: dict):
    print(data)
    return "magic image serivce is running, successfully"

if __name__ == '__main__':
    # https 
    # uvicorn.run(app, host="0.0.0.0", port=8000, ssl_keyfile= "./www.magicimage.site.key", ssl_certfile="./www.magicimage.site_bundle.crt")
    # http, port is 8000
    uvicorn.run(app, host="0.0.0.0", port=8000)
