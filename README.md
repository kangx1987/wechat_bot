# wechat_bot
假装我有男朋友/女朋友
## 为何要写这个文件？
    母亲年纪大了，耳朵不好，身体也不好，在家喜欢看微信，但微信里也没啥朋友，所以写个自动聊天的机器人，来和她聊天。
## 可以做什么？
    可以添加一个微信机器人朋友，做你的贴心伴侣，或者假装是你的男女朋友，让她和你聊天，告诉自己的爸爸妈妈，你已经有女朋友了，不用他们担心了。而且这个朋友永远不会和你吵架哈
    当然，它也可以作为你的私人助理，生活中遇到任何问题，它都可以告诉你。但目前仅限于文字聊天。
## 如何使用？
    需要安装千寻框架，地址https://gitee.com/daenmax/pc-wechat-hook-http-api?_from=gitee_search
    并安装该地址提供的微信版本，不可以用其他版本
    申请百度千帆大模型API接口
    千寻框架登陆你的微信小号，将该微信号添加为好友，并将该好友的微信号和接口信息填入config.yaml文件中
    完成后将以上信息填写到config.yaml文件中，运行main.py文件即可
    如果想重置你的朋友，只需要给他发送信息“\\del”即可让他消失，并重新换个朋友
