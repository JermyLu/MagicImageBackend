import os
os.environ['CUDA_VISIBLE_DEVICES'] = "0"
import torch
from typing import Optional, Dict
from modelscope.pipelines import pipeline, Pipeline
from modelscope.utils.constant import Tasks, DEFAULT_MODEL_REVISION
from config import *

def get_img2img_pipeline(
    task: str,
    model_name: str,
    model_revision: Optional[str] = DEFAULT_MODEL_REVISION
):
    return pipeline(
        task=task,
        model=model_name,
        model_revision=model_revision)

def get_translation_pipeline(model_name: str = "damo/nlp_csanmt_translation_zh2en"):
    return pipeline(
        task=Tasks.translation,
        model=model_name)

def get_text2image_pipeline(
    model_name: str,
    model_revision: Optional[str] = DEFAULT_MODEL_REVISION
):
    return pipeline(
        task=Tasks.text_to_image_synthesis,
        model=model_name,
        model_revision=model_revision,
        torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32)


class ThisPipeline:
    def __init__(
        self,
        pipeline: Pipeline,
        config: Dict
    ):
        self.pipeline = pipeline
        self.config = config

class Image2Image:
    def __init__(
        self,
        config_dict: Dict = img2img_model_config_dict
    ):
        self.config_dict = config_dict
        self.pipeline_dict = self.build()#key is str, value is ThisPipeline instance

    def build(self) -> Dict:
        pipeline_dict = {}
        for style, style_config in self.config_dict.items():
            thisPipeline = ThisPipeline(
                pipeline=get_img2img_pipeline(task=style_config[task],
                                              model_name=style_config[model_name],
                                              model_revision=style_config[model_revision] if model_revision in style_config else DEFAULT_MODEL_REVISION),
                config=style_config
            )
            pipeline_dict[style] = thisPipeline

        return pipeline_dict
    

class Text2Image:
    def __init__(
        self,
        config_dict: Dict = text2img_model_config_dict["chinese"]
    ):
        self.config_dict = config_dict
        # self.translation_pipeline = get_translation_pipeline()
        self.translation_pipeline = None
        self.pipeline_dict = self.build()#key is str, value is ThisPipeline instance

    def build(self) -> Dict:
        pipeline_dict = {}
        for style, style_config in self.config_dict.items():
            thisPipeline = ThisPipeline(
                pipeline=get_text2image_pipeline(model_name=style_config[model_name],
                                                 model_revision=style_config[model_revision] if model_revision in style_config else DEFAULT_MODEL_REVISION),
                config=style_config
            )
            pipeline_dict[style] = thisPipeline

        return pipeline_dict


if __name__=="__main__":
    image2image = Image2Image()
    text2image = Text2Image()

