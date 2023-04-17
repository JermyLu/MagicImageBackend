import random
import string
import requests
import time
import threading
from typing import Dict, List
from utils import generate_request_id

request_param_dict = {
    "http://www.magicimage.site/image2image": {
        "request_id": "",
        "style": "日漫",
        "image": [r"../test/test2.jpeg"]
    },
    "http://www.magicimage.site/text2image": {
        "request_id": "",
        "style": "太乙通用",
        "sequence": "黄河之水天上来,清晰的,概念插画"
    }
}

headers = {'Content-Type': 'application/json'}

def make_request(
    url: str,
    data: Dict, 
    headers: Dict = headers
):
    start_time = time.time()
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        result = response.json()
        status = True#执行成功
    else:
        print(f'Request failed with status code: {response.status_code}')
        status = False#执行出现异常
    end_time = time.time()

    return {
        "cost": float(end_time - start_time),
        "status": status
    }


def calculate_access_time_bySerial(nums: int, api: str):
    total_time = 0
    success_count = 0
    for i in range(nums):
        if api not in request_param_dict:
            raise ValueError("api not found")
        
        data = request_param_dict[api]
        data["request_id"] = generate_request_id()
        result = make_request(url=api, data=data, headers=headers)
        if result["status"]:#True
            total_time += result["cost"]
            success_count += 1
    
    print("Serial & API: %s, the average access timecost is %s" % (api, str(total_time / success_count)))
    return "Serial & API: %s, the average access timecost is %s" % (api, str(total_time / success_count))


class RequestThread(threading.Thread):
    def __init__(self, url: str, data: Dict, headers: Dict):
        super(RequestThread, self).__init__()
        self.url = url
        self.data = data
        self.headers = headers
        self._process_dict = {}

    def run(self):
        self._process_dict[self.ident] = make_request(url=self.url, data=self.data, headers=self.headers)
        print("thread {} is done!".format(self.ident))

    def join(self):#return time-cost
        super().join()
        return self._process_dict

def calculate_access_time_byParallel(nums: int, api: str):
    total_time = 0
    success_count = 0

    merged_process_dict = {}
    # 构建线程池
    thread_pool = []
    for i in range(nums):
        if api not in request_param_dict:
            raise ValueError("api not found")
        
        data = request_param_dict[api]
        data["request_id"] = generate_request_id()
        thread_pool.append(RequestThread(url=api, data=data, headers=headers))

    # 启动 & 执行
    for t in thread_pool:
        t.start()

    for t in thread_pool:
        process_dict = t.join()
        merged_process_dict.update(process_dict)

    # 统计time cost
    for tid, result in merged_process_dict.items():
        if result["status"]:#True
            total_time += result["cost"]
            success_count += 1
    
    print("Parallel & API: %s, the average access timecost is %s" % (api, str(total_time / success_count)))
    return "并发数: %s, Parallel & API: %s, the average access timecost is %s" % (nums, api, str(total_time / success_count))


log_list = []
for api in request_param_dict.keys():
    log_list.append(calculate_access_time_bySerial(nums=10, api=api))
    for nums in range(1, 11):
        log_list.append(calculate_access_time_byParallel(nums=nums, api=api))

# print(log_list)
with open(r"../log/qps_test.log", "w") as fw:
    for tmp in log_list:
        fw.write(tmp + "\n")
