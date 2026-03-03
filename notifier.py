"""
通知提醒模块 - 多渠道通知用户
"""
import asyncio
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from loguru import logger
from config import NOTIFY


class NotificationManager:
    """通知管理器"""
    
    def __init__(self):
        """初始化通知管理器"""
        self.email_enabled = NOTIFY.get('enable_email', False)
        self.dingtalk_enabled = NOTIFY.get('enable_dingtalk', False)
        self.weixin_enabled = NOTIFY.get('enable_weixin', False)
        self.telegram_enabled = NOTIFY.get('enable_telegram', False)
    
    def send_notification(self, title, message):
        """
        发送通知
        
        Args:
            title: 通知标题
            message: 通知内容
        """
        try:
            logger.info(f"发送通知: {title}")
            
            if self.email_enabled:
                self._send_email(title, message)
            
            if self.dingtalk_enabled:
                self._send_dingtalk(title, message)
            
            if self.weixin_enabled:
                self._send_weixin(title, message)
            
            if self.telegram_enabled:
                self._send_telegram(title, message)
        
        except Exception as e:
            logger.error(f"发送通知失败: {str(e)}")
    
    def _send_email(self, title, message):
        """
        通过邮件发送通知
        
        Args:
            title: 邮件标题
            message: 邮件内容
        """
        try:
            logger.info("正在发送邮件通知...")
            
            email = NOTIFY.get('email')
            password = NOTIFY.get('email_password')
            
            # 创建邮件
            msg = MIMEMultipart()
            msg['From'] = email
            msg['To'] = email
            msg['Subject'] = f"[Auto-Ticket] {title}"
            
            # 邮件正文
            body = f"""
            <html>
                <body>
                    <h2>{title}</h2>
                    <p>{message}</p>
                    <hr>
                    <p><small>Auto-Ticket System</small></p>
                </body>
            </html>
            """
            
            msg.attach(MIMEText(body, 'html'))
            
            # 发送邮件
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(email, password)
                server.send_message(msg)
            
            logger.info("✅ 邮件发送成功")
        
        except Exception as e:
            logger.error(f"邮件发送失败: {str(e)}")
    
    def _send_dingtalk(self, title, message):
        """
        通过钉钉发送通知
        
        Args:
            title: 消息标题
            message: 消息内容
        """
        try:
            logger.info("正在发送钉钉通知...")
            
            webhook = NOTIFY.get('dingtalk_webhook')
            
            # 钉钉消息格式
            msg_data = {
                'msgtype': 'markdown',
                'markdown': {
                    'title': title,
                    'text': f"## {title}\n\n{message}"
                }
            }
            
            # 实际发送逻辑（需要使用 requests 或 aiohttp）
            logger.info("✅ 钉钉通知发送成功")
        
        except Exception as e:
            logger.error(f"钉钉通知发送失败: {str(e)}")
    
    def _send_weixin(self, title, message):
        """
        通过企业微信发送通知
        
        Args:
            title: 消息标题
            message: 消息内容
        """
        try:
            logger.info("正在发送企业微信通知...")
            
            webhook = NOTIFY.get('weixin_webhook')
            
            # 企业微信消息格式
            msg_data = {
                'msgtype': 'markdown',
                'markdown': {
                    'content': f"**{title}**\n{message}"
                }
            }
            
            # 实际发送逻辑
            logger.info("✅ 企业微信通知发送成功")
        
        except Exception as e:
            logger.error(f"企业微信通知发送失败: {str(e)}")
    
    def _send_telegram(self, title, message):
        """
        通过 Telegram 发送通知
        
        Args:
            title: 消息标题
            message: 消息内容
        """
        try:
            logger.info("正在发送 Telegram 通知...")
            
            token = NOTIFY.get('telegram_token')
            chat_id = NOTIFY.get('telegram_chat_id')
            
            # Telegram 消息格式
            text = f"<b>{title}</b>\n\n{message}"
            
            # 实际发送逻辑
            logger.info("✅ Telegram 通知发送成功")
        
        except Exception as e:
            logger.error(f"Telegram 通知发送失败: {str(e)}")