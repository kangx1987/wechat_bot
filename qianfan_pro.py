# coding=utf-8
import os
import time
import json
import qianfan
import yaml

# 环境设置
def load_config():
    with open('config.yaml', 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)

def setup_environment():
    """设置环境变量"""
    config = load_config()
    os.environ["QIANFAN_AK"] = config.get('qianfan_ak', '')
    os.environ["QIANFAN_SK"] = config.get('qianfan_sk', '')

def get_response(messages):
    setup_environment()
    """发送API请求并获取响应结果"""
    try:
        resp = qianfan.ChatCompletion().do(
            endpoint="completions",
            messages=messages,
            temperature=0.95,
            top_p=0.8,
            penalty_score=1,
            disable_search=False,
            enable_citation=False
        )
        # 确保响应体中包含 result 键
        if 'result' in resp.body:
            print(resp.body['result'])
            return {"result": resp.body['result']}
        else:
            return {"result": "No result in response"}
    except Exception as e:
        print("API call failed:", e)
        return {"result": "Error occurred"}

if __name__ == "__main__":
    get_response([
    {
        "role": "user",
        "content": "请限制你回复的字数，以后你回复的内容不要超过100个汉字。"
    },
    ])
