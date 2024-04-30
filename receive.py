# coding=utf-8
import qianxun.Emoji as Emoji
from qianxun.SDK import Robot
import json
import os
from send import send_message
import yaml

def load_config():
    with open('config.yaml', 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)

def callback(request):
    print('=' * 50 + '回调事件' + '=' * 50, end='\n\n')
    print(request)
    config = load_config()
    from_wxid_list = config['wxid_list']
    print("当前from_wxid_list=", from_wxid_list)
    if request['event'] == 10009:
        from_wxid_event = request['data']['data']['fromWxid']
        message = request['data']['data']['msg']
        print(f"收到来自用户 {from_wxid_event} 的私聊消息: {message}")
        if from_wxid_event in from_wxid_list:
            if message.strip() == "\\\\del":
                print('收到删除指令，将重置聊天记录')
                handle_deletion(from_wxid_event)
                response_message = "我现在已经删除了咱俩的聊天记录，请输入你想要的角色的名字、性格特点等信息。同时我将尽量简洁明了地与您对话，确保每次回复的字数不超过100个字。"
                send_message(from_wxid_event, response_message)
                save_message_to_file(from_wxid_event, {"role": "assistant", "content": response_message})
            else:
                print('用户在列表中，将记录聊天消息')
                save_message_to_file(from_wxid_event, {"role": "user", "content": message})
        else:
            print('用户不在列表中，忽略消息')

def handle_deletion(from_wxid):
    filepath = f'dialogue_{from_wxid}.json'
    reset_content = [
        {
            "role": "user",
            "content": "请限制你回复的字数，以后你回复的内容不要超过100个汉字。"
        }
    ]
    with open(filepath, 'w', encoding='utf-8') as file:
        json.dump(reset_content, file, indent=4)

# def save_message_to_file(from_wxid, message):
#     filepath = f'dialogue_{from_wxid}.json'
#     if not os.path.exists(filepath):
#         messages = []
#     else:
#         with open(filepath, 'r', encoding='utf-8') as file:
#             messages = json.load(file)
#     messages.append(message)
#     with open(filepath, 'w', encoding='utf-8') as file:
#         json.dump(messages, file, indent=4, ensure_ascii=False)


# def handle_deletion(from_wxid):
#     filepath = f'dialogue_{from_wxid}.json'
#     if os.path.exists(filepath):
#         with open(filepath, 'r', encoding='utf-8') as file:
#             messages = json.load(file)
#         # 保留前两条消息
#         messages_to_keep = messages[:1] if len(messages) > 1 else messages
#         with open(filepath, 'w', encoding='utf-8') as file:
#             json.dump(messages_to_keep, file, indent=4)

def save_message_to_file(from_wxid, message):
    filepath = f'dialogue_{from_wxid}.json'
    if not os.path.exists(filepath):
        messages = []
    else:
        with open(filepath, 'r', encoding='utf-8') as file:
            messages = json.load(file)
    messages.append(message)
    with open(filepath, 'w', encoding='utf-8') as file:
        json.dump(messages, file, indent=4, ensure_ascii=False)

def receive_message(robot_config):
    config = load_config()
    robot_config = config['robot_config']
    robot = Robot(host=robot_config['host'], port=robot_config['port'], bot_wxid=robot_config['bot_wxid'])
    robot.bot_wxid = robot.getWeChatList()['result'][0]['wxid']
    robot.callbackEvents(callback_fun=callback, port=robot_config['callback_port'])
    robot.sendTextMessage(wxid='filehelper', msg=f'你好 {Emoji.小丑脸} 测试 {Emoji.表情_捂脸}')
    return robot

if __name__ == '__main__':
    config = load_config()
    robot_config = config['robot_config']
    receive_message(robot_config)

