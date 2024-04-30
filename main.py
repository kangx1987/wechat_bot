# coding=utf-8
import time
import os
import json
import threading
import queue
from receive import receive_message
from qianfan_pro import get_response
from send import send_message
import yaml

def load_config():
    with open('config.yaml', 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)

def load_messages(filepath):
    """从文件中加载消息列表"""
    if not os.path.exists(filepath):
        return []
    with open(filepath, 'r', encoding='utf-8') as file:
        return json.load(file)

def save_messages(filepath, messages):
    """将消息列表保存到文件中"""
    with open(filepath, 'w', encoding='utf-8') as file:
        json.dump(messages, file, indent=4, ensure_ascii=False)

def process_messages(msg_queue):
    """处理接收到的消息队列"""
    print("Message processing thread started")
    while True:
        from_wxid, message = msg_queue.get()
        print(f"Received message from {from_wxid}: {message}")
        filepath = f'dialogue_{from_wxid}.json'
        messages = load_messages(filepath)
        messages.append({"role": "user", "content": message}) # 保存用户消息
        save_messages(filepath, messages)
        print(f"Message from {from_wxid} saved to {filepath}")

def monitor_and_respond(from_wxid, filepath):
    """监控对话文件并响应变化"""
    last_modified = None
    while True:
        try:
            current_modified = os.path.getmtime(filepath)
            if current_modified != last_modified:
                messages = load_messages(filepath)
                if messages and messages[-1]['role'] == 'user':
                    response = get_response(messages)
                    messages.append({
                        "role": "assistant",
                        "content": response['result']
                    })
                    save_messages(filepath, messages)
                    send_message(from_wxid, response['result'])
                    print("Response added and sent:", response['result'])
                last_modified = current_modified
            time.sleep(10)
        except Exception as e:
            print("Error monitoring/responding:", e)
            time.sleep(10)

def main():
    config = load_config()
    robot_config = config['robot_config']
    wxid_list = config['wxid_list']
    monitored_users = set()  # 用来跟踪已经启动监控的用户
    messages01 = [
        {
        "role": "user",
        "content": "请限制你回复的字数，以后你回复的内容不要超过100个汉字。"
        },
        {
        "role": "assistant",
        "content": "好的。我会尽量简洁明了地回答您的问题，确保每次回复的字数不超过50个字。请你输入你想要的角色prompt"
        },
    ]

    # 启动消息接收
    threading.Thread(target=receive_message, args=(robot_config,)).start()

    # 初始化对话文件并监控所有初始用户
    for from_wxid in wxid_list:
        dialogue_filepath = f'dialogue_{from_wxid}.json'
        if not os.path.exists(dialogue_filepath):
            save_messages(dialogue_filepath, [])
            save_messages(dialogue_filepath, messages01)
        monitored_users.add(from_wxid)
        threading.Thread(target=monitor_and_respond, args=(from_wxid, dialogue_filepath)).start()

    # 检查新用户并为他们启动监控
    while True:
        time.sleep(10)  # 每5分钟检查一次配置文件的变化
        new_config = load_config()
        new_wxid_list = new_config['wxid_list']

        for from_wxid in new_wxid_list:
            if from_wxid not in monitored_users:
                print(f"发现新用户 {from_wxid}，开始监控")
                dialogue_filepath = f'dialogue_{from_wxid}.json'
                if not os.path.exists(dialogue_filepath):
                    save_messages(dialogue_filepath, [])
                    save_messages(dialogue_filepath, messages01)
                monitored_users.add(from_wxid)
                threading.Thread(target=monitor_and_respond, args=(from_wxid, dialogue_filepath)).start()


if __name__ == "__main__":
    main()



