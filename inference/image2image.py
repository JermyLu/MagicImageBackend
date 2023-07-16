import os
# os.environ["CUDA_VISIBLE_DEVICES"] = "-1"#-1: using cpu inference for img2img
import cv2
import traceback
from modelscope.pipelines import Pipeline
from modelscope.outputs import OutputKeys
from typing import Dict, List
from config import *
from utils import resize_image_shape, generate_request_id
from get_pipeline import Image2Image

def get_img2img_result(
    request_id: str,
    style: str,
    pipeline: Pipeline,
    input_image_path: str = None,
    input_image_dict: Dict = None,
    save_dir: str = DataConfig.gen_images
):
    try:
        if not os.path.exists(save_dir):
            os.mkdir(save_dir)
    
        # 优先级: input_image_path > input_image_dict
        if input_image_path is not None:
            result = pipeline(input_image_path)
        elif input_image_dict is not None:
            result = pipeline(input_image_dict)
        else:
            raise ValueError("input_image_path or input_image_dict must have value!!!")

        save_path = os.path.join(save_dir, "%s_%s.png" % (request_id, style))
        cv2.imwrite(save_path, result[OutputKeys.OUTPUT_IMG])
        print("File: %s is saved, done!" % save_path)
        return save_path
    
    except:
        traceback.print_exc()
        return None


def main(
    image2image: Image2Image,
    request_id: str,
    style: str,
    image_list: List[str]
):
    if image_list is None or len(image_list) == 0:
        raise ValueError("len of image list must greater than 1")

    if style not in image2image.pipeline_dict:
        raise ValueError("style must be in %s" % image2image.pipeline_dict.keys())

    this_pipeline = image2image.pipeline_dict[style].pipeline
    this_config = image2image.pipeline_dict[style].config

    img_path = None
    # 单图
    if len(image_list) == 1:
        input_image_path = image_list[0]
        if image_shape in this_config:
            resize_image_shape(
                this_config[image_shape][0],
                this_config[image_shape][1],
                input_image_path
            )
        
        img_path = get_img2img_result(
            request_id=request_id,
            style=style,
            pipeline=this_pipeline,
            input_image_path=input_image_path
        )
        
    # 多图, 如风格迁移...
    elif len(image_list) == 2 and image_nums in this_config and param_list in this_config:
        # 构建多图image-dict
        input_image_dict = {}
        for param, img in zip(this_config[param_list], image_list):
            input_image_dict[param] = img
        # 调整大小
        if image_shape in this_config:
            for _, img_path in input_image_dict.items():
                resize_image_shape(
                    this_config[image_shape][0],
                    this_config[image_shape][1],
                    img_path
                )
        
        img_path = get_img2img_result(
            request_id=request_id,
            style=style,
            pipeline=this_pipeline,
            input_image_dict=input_image_dict
        )
    
    if img_path is not None:
        print("Image2Image Processing is Done!")
    else:
        print("Image2Image Processing is Done, but it exists erros!")
    return img_path
    

if __name__=="__main__":
    
    image2image = Image2Image()
    styles = img2img_model_config_dict.keys()
    image_list = [r"../test/wuYanZu.jpeg"]

    for style in styles:
        main(image2image=image2image, request_id=generate_request_id(), style=style, image_list=image_list)
