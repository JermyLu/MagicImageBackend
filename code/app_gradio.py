import os
import random
import string
import cv2
import gradio as gr
from numpy import ndarray
from typing import List
from image2image import main as i2i_main
from text2image import main as t2i_main
from get_pipeline import image2Image, text2Image

def generate_request_id(length_list: List[int] = [8, 4, 4, 8]) -> str:
    """
        for example, "333f1a25-1252-4f9c-12345678-byGradio"
    """
    nums_pool = [str(i) for i in range(0, 9)]
    chars_pool = list(string.ascii_lowercase)

    request_id = ""
    for length in length_list:
        for i in range(length):
            request_id += random.choice(nums_pool + chars_pool)
        request_id += "-"

    return request_id + "byGradio"

image2image_types = [
    "3D漫画",
    "插画",
    "漫画",
    "手绘",
    "人像美肤",
    "人体美型",
    "日漫",
    "艺术"
]

text2image_types = [
    "艺术创想",
    "二次元",
    "漫画风",
    "中国画",
    "概念插画",
    "质感胶片",
    "赛博朋克",
    "梵高",
    "超现实主义",
    "毕加索"
]

def text2image(
    input_text: str = "",
    prompt: str = "",
    negative_prompt: str = "",
    t2i_type: str = "",
    request_id: str = generate_request_id()
):
    generate_file_path = t2i_main(
        text2image=text2Image,
        request_id=request_id,
        style="太乙通用",
        sequence="%s,%s,%s" % (input_text, prompt, t2i_type)
    )

    return generate_file_path
    # return "request_id is %s : style is %s : sequence is %s" % (request_id, t2i_type, "%s,%s" % (input_text, prompt))

def image2image(
    image: ndarray,
    i2i_type: str = "",
    request_id: str = generate_request_id()
):
    # 先保存ndarray -> fileImage
    file_path = os.path.join(
        r"../input_images",
        request_id + "_" + i2i_type + ".png"
    )
    cv2.imwrite(file_path, image)

    generate_file_path = i2i_main(
        image2image=image2Image,
        request_id=request_id,
        style=i2i_type,
        image_list=[file_path]
    )

    return generate_file_path

with gr.Blocks() as demo:
    gr.Markdown("Do magic image2image and text2image using this demo.")
    with gr.Tab("Image2Image"):
        with gr.Row():
            with gr.Column():
                image_input = gr.Image()
                i2i_type = gr.Radio(choices=image2image_types, type="value", label="风格")
            image_output = gr.Image()#gr.Textbox(lines=2)
        image_button = gr.Button("Image2Image")

    with gr.Tab("Text2Image"):
        with gr.Row():
            with gr.Column():
                input_text = gr.Textbox(lines=2, placeholder="输入你的创意...", label="Input")
                prompt = gr.Textbox(lines=2, placeholder="清晰、质感...", label="Prompt")
                negative_prompt = gr.Textbox(lines=2, placeholder="模糊、粗糙...", label="Negative-Prompt")
                t2i_type = gr.Radio(choices=text2image_types, type="value", label="风格")
            text_output = gr.Image()
        text_button = gr.Button("Text2Image")

    image_button.click(image2image, inputs=[image_input, i2i_type], outputs=image_output)
    text_button.click(text2image, inputs=[input_text, prompt, negative_prompt, t2i_type], outputs=text_output)
    
if __name__=="__main__":
    demo.queue()  # <-- Sets up a queue with default parameters
    demo.launch(share=True)
