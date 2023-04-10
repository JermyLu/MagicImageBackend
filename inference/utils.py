import cv2
import random
import string
import base64
from io import BytesIO
from typing import List
from PIL import Image

"""
    图像分辨率若大于max_height * max_width
    则按照最大像素值进行等比例放缩
"""
def resize_image_shape(
    max_height: int,
    max_width: int,
    image_path: str
):
    img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    height, width, _ = img.shape
    print("original image shape: " + str(img.shape))

    if height <= max_height and width <= max_width:
        print("Do not need resize!")
    # 进行放缩
    else:
        if max_height / height <= max_width / width:
            resize = cv2.resize(
                img, 
                (int(width * max_height / height), int(height * max_height / height)), 
                interpolation = cv2.INTER_AREA
            )
        else:
            resize = cv2.resize(
                img,
                (int(width * max_width / width), int(height * max_width / width)),
                interpolation = cv2.INTER_AREA
            )
        
        cv2.imwrite(image_path, resize)
        print("Resizing image is done, resized image shape: " + str())

# 图片编码成 base64 格式
def encode_image_to_base64(image_path: str):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
        return encoded_string.decode('utf-8')
    
# 解码为原始图像，进行存储
def save_image_from_base64(b64str, output_path: str):
    img_data = base64.b64decode(b64str)
    img = Image.open(BytesIO(img_data))
    img.save(output_path)

def generate_request_id(length_list: List[int] = [8, 4, 4, 8]) -> str:
    """
        for example, "333f1a25-1252-4f9c-12345678"
    """
    nums_pool = [str(i) for i in range(0, 9)]
    chars_pool = list(string.ascii_lowercase)

    request_id = ""
    for length in length_list:
        for i in range(length):
            request_id += random.choice(nums_pool + chars_pool)
        request_id += "-"
    
    return request_id[:-1]


if __name__=="__main__":
    image_path = r"../test/test.jpeg"
    print(encode_image_to_base64(image_path)[:100])
