import os
os.environ["CUDA_VISIBLE_DEVICES"] = "0"
import re
import cv2
import traceback
from modelscope.pipelines import Pipeline
from modelscope.outputs import OutputKeys
from diffusers import StableDiffusionInpaintPipelineLegacy
from typing import Dict, List
from config import *
from utils import generate_request_id
from get_pipeline import Text2Image

def get_translation_result(pipeline: Pipeline, input_sequence: str) -> str:
    outputs = pipeline(input=input_sequence)
    return outputs["translation"]

def get_text2image_result_bySdPipeline(
    request_id: str,
    pipeline: StableDiffusionInpaintPipelineLegacy,
    prompt: str,
    image_name: str,
    save_dir: str = DataConfig.gen_images
):
    try:
        if not os.path.exists(save_dir):
            os.mkdir(save_dir)
    
        # height=512, width=768会导致oom
        save_path = os.path.join(save_dir, "%s_%s%s" % (request_id, image_name, ".png"))
        output = pipeline(prompt, num_inference_steps=50, guidance_scale=7.5).images[0]
        output.save(save_path)

        print("File: %s is saved, done!" % save_path)
        return save_path
        
    except:
        traceback.print_exc()
        return None

def get_text2image_result(
    request_id: str,
    pipeline: Pipeline,
    input_dict: Dict,
    image_name: str,
    save_dir: str = DataConfig.gen_images
):
    try:
        if not os.path.exists(save_dir):
            os.mkdir(save_dir)
    
        output = pipeline(input_dict)
        save_path = os.path.join(save_dir, "%s_%s%s" % (request_id, image_name, ".png"))
        cv2.imwrite(save_path, output['output_imgs'][0])

        print("File: %s is saved, done!" % save_path)
        return save_path
        
    except:
        traceback.print_exc()
        return None


def main(
    text2image: Text2Image,
    request_id: str,
    style: str,
    sequence: str,
    language: str = "chinese",
):
    # 删除sequence中得任意标点符 & 空白字符
    sequence = re.sub(r'[^\w]', ',', sequence)
    # 将多个,替换为一个,
    sequence = re.sub(r',+', ',', sequence)
    if language not in ["chinese", "english"]:
        raise ValueError("lanage must be chinese or english")

    if style not in text2image.pipeline_dict:
        # print(text2image.pipeline_dict.keys())
        raise ValueError("style must be in %s" % text2image.pipeline_dict.keys())
    
    this_pipeline = text2image.pipeline_dict[style].pipeline
    this_config = text2image.pipeline_dict[style].config

    if language == "english":
        sequence = get_translation_result(
            pipeline=text2image.translation_pipeline,
            input_sequence=sequence
        )

    if position in this_config and prompt in this_config:
        if this_config[position] == "begin":
            sequence = this_config[prompt] + sequence
        elif this_config[position] == "end":
            sequence = sequence + this_config[prompt]
        else:
            raise ValueError("position muse be begin or end!")

    print("***********: Final sequence is %s **********" % sequence)
    if style == "太乙通用":
        input_dict = {
            "text": sequence,
            "height": 512,
            "width": 768,
            'num_inference_steps': 25,
            "guidance_scale": 9
        }
        if negative_prompt in this_config:
            input_dict[negative_prompt] = this_config[negative_prompt]

        img_path = get_text2image_result(
            request_id=request_id,
            pipeline=this_pipeline,
            input_dict=input_dict,
            image_name=sequence
        )

    elif style == "天工巧绘":
        img_path = get_text2image_result_bySdPipeline(
            request_id=request_id,
            pipeline=this_pipeline,
            prompt='sai-v1 art, ' + sequence,
            image_name=sequence
        )

    else:
        img_path = None
    
    if img_path is not None:
        print("Text2Image Processing is Done!")
    else:
        print("Text2Image Processing is Done, but it exists erros!")
    return img_path


if __name__=="__main__":
    language = "chinese"
    styles = ["太乙通用"]
    sequence_list = [
        "大漠孤烟直,插画",
        "白日依山尽,油画",
        "飞流直下三千尺,水彩"
    ]
    
    for style in styles:
        for sequence in sequence_list:
            main(text2image=Text2Image(), request_id=generate_request_id(), style=style, sequence=sequence, language=language)
