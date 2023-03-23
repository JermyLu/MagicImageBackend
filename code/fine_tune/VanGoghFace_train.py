import os
import unittest
import cv2
from modelscope.exporters.cv import CartoonTranslationExporter
from modelscope.msdatasets import MsDataset
from modelscope.outputs import OutputKeys
from modelscope.pipelines import pipeline
from modelscope.pipelines.base import Pipeline
from modelscope.trainers.cv import CartoonTranslationTrainer
from modelscope.utils.constant import Tasks
from modelscope.utils.test_utils import test_level

model_id = 'damo/cv_unet_person-image-cartoon_compound-models'
data_dir = MsDataset.load(
            'dctnet_train_clipart_mini_ms',
            namespace='menyifang',
            split='train').config_kwargs['split_config']['train']

data_photo = os.path.join(data_dir, 'face_photo')
data_cartoon = r"./dataSet/VanGoghFace"
work_dir = r"./model/VanGoghFace"
max_steps = 10
trainer = CartoonTranslationTrainer(
            model=model_id,
            work_dir=work_dir,
            photo=data_photo,
            cartoon=data_cartoon,
            max_steps=max_steps)
trainer.train()
