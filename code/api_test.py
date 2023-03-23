import requests

urls = [
    'https://localhost:8000/image2image',
    'https://localhost:8000/text2image'
    # 'http://10.161.228.126:8000/image2image',
    # 'http://10.161.228.126:8000/text2image'
]
datas = [
    {
        "request_id": "i2i_test",
        "style": "日漫",
        "image": [r"../input_images/test2.jpeg"]
    },
    {
        "request_id": "t2i_test",
        "style": "太乙通用",
        "sequence": "清晨,田野,白云,清晰的,田园画"
    }
]
headers = {'Content-Type': 'application/json'}

for url, data in zip(urls, datas):
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        result = response.json()
    else:
        print(f'Request failed with status code: {response.status_code}')
