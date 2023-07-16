import os
import random
import traceback
from PIL import Image
import face_recognition
from image2image import main as i2i_main
from get_pipeline import Image2Image
from typing import List


def is_small_face(
    image_width: int,
    image_height: int,
    face_width: int,
    face_height: int,
    scale: int = 3
):
    """
        判断人脸在原图中比例是否很小
        0: 原图高宽均大于等于3*人脸高宽
        1: 仅原图高>=3*人脸高
        2: 仅原图宽>=3*人脸宽
        3: 原图高宽均<3*人脸高宽
    
    """
    if image_height >= face_height * scale and image_width >= face_width * scale:
        return 0
    elif image_height >= face_height * scale and image_width < face_width * scale:
        return 1
    elif image_height < face_height * scale and image_width >= face_width * scale:
        return 2
    #< & <
    return 3

def relocation_face(
    image_width: int,
    image_height: int,
    face_top: int,
    face_bottom: int,
    face_left: int,
    face_right: int,
    bias_width: int,
    bias_height: int
):
    # bias表示偏移量
    face_top = face_top - bias_height if face_top - bias_height >= 0 else 0
    face_bottom = face_bottom + bias_height if face_bottom + bias_height <= image_height else image_height
    face_left = face_left - bias_width if face_left - bias_width >= 0 else 0
    face_right = face_right + bias_width if face_right + bias_width <= image_width else image_width

    return face_top, face_bottom, face_left, face_right

def clip_face(image_path: str, face_save_path: str):
    origin_width, origin_height = Image.open(image_path).size
    print("origin image size: width = {}, height = {}.".format(origin_width, origin_height))
    image = face_recognition.load_image_file(image_path)
    # Find all the faces in the image using the default HOG-based model.
    # This method is fairly accurate, but not as accurate as the CNN model and not GPU accelerated.
    # See also: find_faces_in_picture_cnn.py
    face_locations = face_recognition.face_locations(image)

    print("I found {} face(s) in this photograph.".format(len(face_locations)))
    if len(face_locations) >= 2:
        raise ValueError("输入图像人脸数量应等于1")

    # Print the location of each face in this image
    top, right, bottom, left = face_locations[0]
    print("face coordinate is: left-top = ({},{}), right-bottom = ({},{})".format(left, top, right, bottom))
    face_width, face_height = right - left, bottom - top
    print("face size: width = {}, height = {}.".format(face_width, face_height))

    if is_small_face(origin_width, origin_height, face_width, face_height) == 0:
        top, bottom, left, right = relocation_face(
            origin_width,
            origin_height,
            top,
            bottom,
            left,
            right,
            bias_width=face_width,
            bias_height=face_height)
    
    elif is_small_face(origin_width, origin_height, face_width, face_height) == 1:
        top, bottom, left, right = relocation_face(
            origin_width,
            origin_height,
            top,
            bottom,
            left,
            right,
            bias_width=int(face_width / 2),
            bias_height=face_height)
    
    elif is_small_face(origin_width, origin_height, face_width, face_height) == 2:
        top, bottom, left, right = relocation_face(
            origin_width,
            origin_height,
            top,
            bottom,
            left,
            right,
            bias_width=face_width,
            bias_height=int(face_height / 2))
    
    else:
        top, bottom, left, right = relocation_face(
            origin_width,
            origin_height,
            top,
            bottom,
            left,
            right,
            bias_width= int(face_width / 2),
            bias_height= int(face_height / 2))
    print("After relocation, the face is located at pixel location Top: {}, Left: {}, Bottom: {}, Right: {}"
          .format(top, left, bottom, right))

    # You can access the actual face itself like this:
    face_image = image[int(top):int(bottom), int(left):int(right)]
    pil_image = Image.fromarray(face_image)
    pil_image.save(face_save_path)
    # pil_image.show()


def main(
    image2image: Image2Image,
    request_id: str,
    image_list: List[str],
    styles: List[str] = ["3D漫画", "手绘", "插画", "日漫", "艺术"],
    generate_one: bool = True
):
    face_path_list = []
    if generate_one:
        # 随机选择一个风格
        style = random.choice(seq=styles)
        img_path = i2i_main(image2image=image2image, request_id=request_id, style=style, image_list=image_list)
        if img_path is not None:
            (file_name, ext) = os.path.splitext(img_path)
            face_path = file_name + "_face" + ext
            try:
                clip_face(image_path=img_path, face_save_path=face_path)
                face_path_list.append(face_path)
            except:
                traceback.print_exc()
    else:#False
        for style in styles:
            img_path = i2i_main(image2image=image2image, request_id=request_id, style=style, image_list=image_list)
            if img_path is not None:
                (file_name, ext) = os.path.splitext(img_path)
                face_path = file_name + "_face" + ext
                try:
                    clip_face(image_path=img_path, face_save_path=face_path)
                    face_path_list.append(face_path)
                except:
                    traceback.print_exc()

    return face_path_list


if __name__=="__main__":
    from utils import generate_request_id
    image2image = Image2Image()
    image_list = [r"../test/pengYuYan.jpeg"]
    face_path_list = main(image2image, generate_request_id(), image_list)
    print(face_path_list)


