from modelscope.utils.constant import Tasks

# 常数变量
source = "source"
model_name = "model_name"
model_revision = "model_revision"
prompt = "prompt"
position = "position"
negative_prompt = "negative_prompt"
task = "task"
# image_nums must be len(param_list)
image_nums = "image_nums"
image_shape = "image_shape"
param_list = "param_list"

"""
    model_config:
        language: englisht / chinese
        position: begin / end, begin表示prompt +  生成词, end表示生成词 + prompt
        negative_prompt存在, 生成时增加该参数

"""
text2img_model_config_dict = {
    # "english": {
    #     # 渲染
    #     "redshift": {
    #         model_name: "dienstag/redshift-diffusion",
    #         model_revision: "v1.0",
    #         prompt: "redshift style ",
    #         position: "begin"
    #     },
    #     # 剪贴画
    #     "clipart": {
    #         model_name: "damo/cv_cartoon_stable_diffusion_clipart",
    #         model_revision: "v1.0.0",
    #         prompt: "archer style, a portrait painting of ",
    #         position: "begin"

    #     },
    #     # 扁平
    #     "flat": {
    #         model_name: "damo/cv_cartoon_stable_diffusion_flat",
    #         model_revision: "v1.0.0",
    #         prompt: "sks style, a portrait painting of ",
    #         position: "begin"
    #     },
    #     # 水彩
    #     "watercolor": {
    #         model_name: "damo/cv_cartoon_stable_diffusion_watercolor",
    #         model_revision: "v1.0.0",
    #         prompt: "sks style, a portrait painting of ",
    #         position: "begin"
    #     },
    #     # 漫画
    #     "illustration": {
    #         model_name: "damo/cv_cartoon_stable_diffusion_illustration",
    #         model_revision: "v1.0.0",
    #         prompt: "sks style, a portrait painting of ",
    #         position: "begin"
    #     },
    #     # 插画
    #     "design": {
    #         model_name: "damo/cv_cartoon_stable_diffusion_design",
    #         model_revision: "v1.0.0",
    #         prompt: "sks style, a portrait painting of ",
    #         position: "begin"
    #     },
    #     # 国画
    #     "guohua": {
    #         model_name: "langboat/Guohua-Diffusion",
    #         model_revision: "v1.0",
    #         prompt: " in guohua style",
    #         position: "end"
    #     },
    #     # 迪士尼
    #     "disney": {
    #         model_name: "dienstag/mo-di-diffusion",
    #         model_revision: "v1.0.1",
    #         prompt: ", modern disney style",
    #         position: "end"
    #     },
    #     # 胶片
    #     "analog": {
    #         model_name: "dienstag/Analog-Diffusion",
    #         model_revision: "v1.0",
    #         prompt: "analog style ",
    #         position: "begin",
    #         negative_prompt: "blur haze"
    #     }
    # },
    "chinese": {
        # 通用风格
        # "通用": {
        #     model_name: "damo/multi-modal_chinese_stable_diffusion_v1.0",
        #     negative_prompt: "模糊的"
        # },
        # # 太乙动漫
        # "太乙动漫": {
        #     model_name: "Fengshenbang/Taiyi-Stable-Diffusion-1B-Anime-Chinese-v0.1",
        #     model_revision: "v1.0.0",
        #     negative_prompt: "模糊的,失真的"
        # },
        # 太乙通用
        "太乙通用": {
            model_name: "Fengshenbang/Taiyi-Stable-Diffusion-1B-Chinese-v0.1",
            model_revision: "v1.0.0",
            negative_prompt: "广告, ，, ！, 。, ；, 资讯, 新闻, 水印"
        },
        # "天工巧绘": {
        #     source: "sd",
        #    model_name: "SkyWork/SkyPaint"
        # }
    }
}


img2img_model_config_dict = {
    "人像美肤": {
       model_name: "damo/cv_unet_skin-retouching",
       task: Tasks.skin_retouching,
       image_shape: (5000, 5000)
    },
    "人像美型": {
        model_name: "damo/cv_flow-based-body-reshaping_damo",
        task: Tasks.image_body_reshaping,
        image_shape: (3000, 3000)
    },
    # "人像修复": {
    #     model_name: "damo/cv_gpen_image-portrait-enhancement",
    #     task: Tasks.image_portrait_enhancement,
    #     image_shape: (512, 512)
    # },
    # "图像上色": {
    #     model_name: "damo/cv_ddcolor_image-colorization",
    #     task: Tasks.image_colorization
    # },
    # "饱和度增强": {
    #     model_name: "damo/cv_csrnet_image-color-enhance-models",
    #     task: Tasks.image_color_enhancement
    # },
    # "清晰化": {
    #     model_name: "damo/cv_nafnet_image-deblur_gopro",
    #     task: Tasks.image_deblurring
    # },
    # "图像超分": {
    #     model_name: "damo/cv_rrdb_image-super-resolution",
    #     task: Tasks.image_super_resolution
    # },
    # "人像抠图": {
    #     model_name: "damo/cv_unet_image-matting",
    #     task: Tasks.portrait_matting,
    #     image_shape: (2000, 2000)
    # },
    # "通用抠图": {
    #     model_name: "damo/cv_unet_universal-matting",
    #     task: Tasks.universal_matting,
    #     image_shape: (2000, 2000)
    # },
    # "天空替换": {
    #     model_name: "damo/cv_hrnetocr_skychange",
    #     task: Tasks.image_skychange,
    #     image_nums: 2,
    #     param_list: [
    #         "sky_image",
    #         "scene_image"
    #     ],
    #     image_shape: (5000, 5000)
    # },
    # "风格迁移": {
    #     model_name: "damo/cv_aams_style-transfer_damo",
    #     task: Tasks.image_style_transfer,
    #     image_nums: 2,
    #     param_list: [
    #         "content",
    #         "style"
    #     ],
    #     image_shape: (1200, 1200)

    # },
    # "人脸融合": {
    #     model_name: "damo/cv_unet-image-face-fusion_damo",
    #     task: Tasks.image_face_fusion,
    #     image_nums: 2,
    #     param_list: [
    #         "template",
    #         "user"
    #     ],
    #     image_shape: (4000, 4000)
    # },
    "日漫": {
         model_name: "damo/cv_unet_person-image-cartoon_compound-models",
         task: Tasks.image_portrait_stylization,
         image_shape: (3000, 3000)
    },
    "手绘": {
        model_name: "damo/cv_unet_person-image-cartoon-handdrawn_compound-models",
        task: Tasks.image_portrait_stylization,
        image_shape: (3000, 3000)
    },
    "3D漫画": {
        model_name: "damo/cv_unet_person-image-cartoon-3d_compound-models",
        task: Tasks.image_portrait_stylization,
        image_shape: (3000, 3000)
    },
    "艺术": {
        model_name: "damo/cv_unet_person-image-cartoon-artstyle_compound-models",
        task: Tasks.image_portrait_stylization,
        image_shape: (3000, 3000)
    },
    #"素描": {
    #    model_name: "damo/cv_unet_person-image-cartoon-sketch_compound-models",
    #    task: Tasks.image_portrait_stylization,
    #    image_shape: (3000, 3000)
    #},
    "插画": {
        model_name: "damo/cv_unet_person-image-cartoon-sd-design_compound-models",
        model_revision: "v1.0.0",
        task: Tasks.image_portrait_stylization,
        image_shape: (3000, 3000)
    },
    "漫画": {
        model_name: "damo/cv_unet_person-image-cartoon-sd-illustration_compound-models",
        model_revision: "v1.0.0",
        task: Tasks.image_portrait_stylization,
        image_shape: (3000, 3000)
    }
   
}

class DataConfig:
    input_images = "/root/magic.image/input_images"
    gen_images = "/root/magic.image/gen_images"
    feedback = "/root/magic.image/feedback"
