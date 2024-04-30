import json
import requests
import yaml

def load_config():
    with open('config.yaml', 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)

def send_message(wxid, msg):
    config = load_config()
    url = config['message_api_url']  # 加载配置文件中的 URL
    data = {
        "type": "Q0001",
        "data": {
            "wxid": wxid,  # 这里是目标微信的wxid
            "msg": msg    # 这里是要发送的消息
        }
    }
    # 发送POST请求
    response = requests.post(url, json=data)
    return response.text

# 测试发送消息
if __name__ == "__main__":
    send_message('example_wxid', 'Hello, World!')
