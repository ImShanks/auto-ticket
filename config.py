"""
配置文件 - 自动抢票系统配置
"""
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# ==================== 账户配置 ====================
ACCOUNT = {
    'username': os.getenv('TICKET_USERNAME', 'your_username'),
    'password': os.getenv('TICKET_PASSWORD', 'your_password'),
    'platform': os.getenv('TICKET_PLATFORM', 'ticketmaster'),  # 票务平台
}

# ==================== 监控配置 ====================
MONITOR = {
    'check_interval': 5,  # 检查间隔（秒）
    'event_id': 'your_event_id',  # 活动ID
    'max_retries': 3,  # 最大重试次数
    'timeout': 30,  # 请求超时时间
}

# ==================== 抢票配置 ====================
GRABBER = {
    'quantity': 2,  # 购票数量
    'auto_pay': True,  # 是否自动支付
    'max_attempts': 5,  # 最大尝试次数
}

# ==================== 通知配置 ====================
NOTIFY = {
    'enable_email': True,
    'email': os.getenv('NOTIFY_EMAIL', 'your_email@example.com'),
    'email_password': os.getenv('EMAIL_PASSWORD', ''),
    
    'enable_dingtalk': False,
    'dingtalk_webhook': os.getenv('DINGTALK_WEBHOOK', ''),
    
    'enable_weixin': False,
    'weixin_webhook': os.getenv('WEIXIN_WEBHOOK', ''),
    
    'enable_telegram': False,
    'telegram_token': os.getenv('TELEGRAM_TOKEN', ''),
    'telegram_chat_id': os.getenv('TELEGRAM_CHAT_ID', ''),
}

# ==================== 代理配置 ====================
PROXY = {
    'enable': False,
    'http': 'http://proxy.example.com:8080',
    'https': 'https://proxy.example.com:8080',
}

# ==================== 日志配置 ====================
LOGGING = {
    'level': 'INFO',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'file': 'logs/auto_ticket.log',
}

# ==================== 浏览器配置 ====================
BROWSER = {
    'headless': False,  # 是否无头模式
    'browser_type': 'chrome',  # chrome, firefox, edge
    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
}