from diffusers import StableDiffusionPipeline

device = 'cuda'
pipe = StableDiffusionPipeline.from_pretrained("SkyWork/SkyPaint").to(device)

prompts = [
    '机械狗',
    '城堡 大海 夕阳 宫崎骏动画',
    '花落知多少',
    '鸡你太美',
]

for prompt in prompts:
    prompt = 'sai-v1 art, ' + prompt
    image = pipe(prompt).images[0]  
    image.save("%s.jpg" % prompt)
