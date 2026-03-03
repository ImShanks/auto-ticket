# Auto-Ticket 自动抢票系统

一个功能强大的 Python 自动抢票系统，支持自动登录、实时监控票务信息、自动抢票和多渠道通知提醒。

## 功能特性

- ✅ 自动登录 - 支持多种账户登录方式
- ✅ 票务监控 - 实时监控票务信息变化
- ✅ 自动抢票 - 一旦检测到票务可用自动下单
- ✅ 通知提醒 - 支持邮件、钉钉、企业微信等多渠道通知

## 快速开始

### 环境要求
- Python 3.7+
- pip

### 安装

```bash
git clone https://github.com/ImShanks/auto-ticket.git
cd auto-ticket
pip install -r requirements.txt
```

### 配置

编辑 `config.py` 文件，配置你的账户信息和通知设置：

```python
# 账户配置
ACCOUNT = {
    'username': 'your_username',
    'password': 'your_password'
}

# 通知配置
NOTIFY = {
    'email': 'your_email@example.com',
    'dingtalk': 'your_dingtalk_webhook',
    'weixin': 'your_weixin_webhook'
}
```

### 运行

```bash
python main.py
```

## 项目结构

```
auto-ticket/
├── README.md              # 项目说明
├── requirements.txt       # 依赖包列表
├── config.py             # 配置文件
├── main.py               # 主程序入口
├── auth.py               # 自动登录模块
├── monitor.py            # 票务监控模块
├── grabber.py            # 自动抢票模块
├── notifier.py           # 通知提醒模块
└── utils.py              # 工具函数
```

## 使用示例

```python
from auto_ticket import TicketGrabber

# 初始化
grabber = TicketGrabber('config.py')

# 开始监控和抢票
grabber.start()
```

## 注意事项

⚠️ 本项目仅供学习和研究使用，请遵守相关法律法规和平台使用协议。

## License

MIT