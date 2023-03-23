import os
os.environ["CUDA_VISIBLE_DEVICES"] = "0"
import cv2
from modelscope.pipelines import Pipeline
from modelscope.outputs import OutputKeys
from typing import Dict, List
from config import *
from utils import generate_request_id
from get_pipeline import Text2Image

def get_translation_result(pipeline: Pipeline, input_sequence: str) -> str:
    outputs = pipeline(input=input_sequence)
    return outputs["translation"]

def get_text2image_result(
    request_id: str,
    pipeline: Pipeline,
    input_dict: Dict,
    image_name: str,
    save_dir: str = r"../gen_images"
):
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)
    
    output = pipeline(input_dict)
    save_path = os.path.join(save_dir, "%s_%s%s" % (request_id, image_name, ".png"))
    cv2.imwrite(save_path, output['output_imgs'][0])

    print("File: %s is saved, done!" % save_path)


def main(
    text2image: Text2Image,
    request_id: str,
    style: str,
    sequence: str,
    language: str = "chinese",
):
    if language not in ["chinese", "english"]:
        raise ValueError("lanage must be chinese or english")

    if style not in text2image.pipeline_dict:
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

    input_dict = {
        "text": sequence,
        "height": 512,
        "width": 768,
        'num_inference_steps': 25,
        "guidance_scale": 9
    }
    if negative_prompt in this_config:
        input_dict[negative_prompt] = this_config[negative_prompt]

    get_text2image_result(
        request_id=request_id,
        pipeline=this_pipeline,
        input_dict=input_dict,
        image_name=sequence
    )
    print("Text2Image Processing is Done!")


if __name__=="__main__":
    language = "chinese"
    styles = text2img_model_config_dict["chinese"].keys()
    sequence_list = [
        "大漠孤烟直,中国画",
        "白日依山尽,中国画",
        "飞流直下三千尺,中国画"
    ]
    
    for style in styles:
        for sequence in sequence_list:
            main(text2image=Text2Image(), request_id=generate_request_id(), style=style, sequence=sequence, language=language)
