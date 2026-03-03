"""
主程序入口 - 自动抢票系统
"""
import logging
import asyncio
from datetime import datetime
from loguru import logger

from config import LOGGING, ACCOUNT, MONITOR
from auth import TicketAuthenticator
from monitor import TicketMonitor
from grabber import TicketGrabber
from notifier import NotificationManager


class AutoTicketSystem:
    """自动抢票系统主类"""
    
    def __init__(self):
        """初始化系统"""
        self.setup_logger()
        self.authenticator = TicketAuthenticator(ACCOUNT)
        self.monitor = TicketMonitor(MONITOR)
        self.grabber = TicketGrabber()
        self.notifier = NotificationManager()
        self.is_running = False
        
    def setup_logger(self):
        """设置日志"""
        logger.add(
            LOGGING['file'],
            level=LOGGING['level'],
            format=LOGGING['format'],
            rotation="10 MB",
            retention="7 days"
        )
        logger.info("=" * 50)
        logger.info(f"Auto-Ticket System Started at {datetime.now()}")
        logger.info("=" * 50)
    
    async def run(self):
        """运行系统"""
        try:
            logger.info("开始初始化系统...")
            
            # 1. 自动登录
            logger.info("步骤 1: 自动登录")
            session = await self.authenticator.login()
            if not session:
                logger.error("登录失败，系统退出")
                self.notifier.send_notification("❌ 登录失败", "无法登录到票务系统")
                return
            
            logger.info("✅ 登录成功")
            self.notifier.send_notification(
                "✅ 登录成功", 
                f"已成功登录到票务系统 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            )
            
            # 2. 开始监控票务
            logger.info("步骤 2: 开始监控票务信息")
            self.is_running = True
            
            while self.is_running:
                try:
                    # 检查票务状态
                    ticket_available = await self.monitor.check_tickets(session)
                    
                    if ticket_available:
                        logger.warning("🎉 检测到可用票务！开始抢票...")
                        self.notifier.send_notification(
                            "🎉 票务可用", 
                            "检测到可用票务，开始自动抢票！"
                        )
                        
                        # 3. 自动抢票
                        logger.info("步骤 3: 自动抢票")
                        success = await self.grabber.grab_tickets(session)
                        
                        if success:
                            logger.info("🎊 抢票成功！")
                            self.notifier.send_notification(
                                "🎊 抢票成功",
                                f"恭喜！已成功抢到票务 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                            )
                            self.is_running = False
                        else:
                            logger.warning("⚠️ 抢票失败，继续监控...")
                            self.notifier.send_notification(
                                "⚠️ 抢票失败",
                                "抢票失败，系统将继续监控"
                            )
                    
                    # 等待下次检查
                    await asyncio.sleep(MONITOR['check_interval'])
                    
                except Exception as e:
                    logger.error(f"监控过程中出错: {str(e)}")
                    await asyncio.sleep(MONITOR['check_interval'])
                    continue
            
            logger.info("系统完成执行")
            
        except Exception as e:
            logger.error(f"系统运行出错: {str(e)}")
            self.notifier.send_notification(
                "❌ 系统错误",
                f"系统运行出错: {str(e)}"
            )
    
    def stop(self):
        """停止系统"""
        logger.info("收到停止信号，系统退出中...")
        self.is_running = False


def main():
    """主函数"""
    system = AutoTicketSystem()
    
    try:
        asyncio.run(system.run())
    except KeyboardInterrupt:
        logger.info("用户中断了程序")
        system.stop()
    except Exception as e:
        logger.error(f"程序异常退出: {str(e)}")
        system.stop()


if __name__ == "__main__":
    main()