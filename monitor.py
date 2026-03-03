"""
票务监控模块 - 实时监控票务信息变化
"""
import asyncio
from datetime import datetime
from loguru import logger


class TicketMonitor:
    """票务监控类"""
    
    def __init__(self, monitor_config):
        """
        初始化监控器
        
        Args:
            monitor_config: 监控配置字典
        """
        self.check_interval = monitor_config.get('check_interval', 5)
        self.event_id = monitor_config.get('event_id')
        self.max_retries = monitor_config.get('max_retries', 3)
        self.timeout = monitor_config.get('timeout', 30)
        self.last_status = None
        self.check_count = 0
    
    async def check_tickets(self, session):
        """
        检查票务状态
        
        Args:
            session: aiohttp 会话对象
        
        Returns:
            bool: 票务是否可用
        """
        try:
            self.check_count += 1
            logger.info(f"[检查 #{self.check_count}] 正在检查票务状态...")
            
            # 构建请求 URL
            url = f"https://www.ticketmaster.com/api/events/{self.event_id}/tickets"
            
            # 发送请求
            async with session.get(url, timeout=self.timeout) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    # 检查是否有可用票
                    available = self._parse_ticket_data(data)
                    
                    # 记录状态变化
                    if available != self.last_status:
                        status_text = "✅ 有票" if available else "❌ 无票"
                        logger.info(f"票务状态: {status_text}")
                        self.last_status = available
                    
                    return available
                else:
                    logger.warning(f"获取票务信息失败，状态码: {response.status}")
                    return False
        
        except asyncio.TimeoutError:
            logger.error("检查票务超时")
            return False
        except Exception as e:
            logger.error(f"检查票务时出错: {str(e)}")
            return False
    
    def _parse_ticket_data(self, data):
        """
        解析票务数据
        
        Args:
            data: API 响应数据
        
        Returns:
            bool: 是否有可用票
        """
        try:
            # 根据实际 API 响应格式解析
            if 'tickets' in data:
                tickets = data['tickets']
                
                # 检查是否有库存大于 0 的票
                for ticket_type in tickets:
                    if ticket_type.get('inventory', 0) > 0:
                        logger.debug(f"发现可用票: {ticket_type.get('name', 'Unknown')} (库存: {ticket_type.get('inventory')})")
                        return True
            
            return False
        
        except Exception as e:
            logger.error(f"解析票务数据失败: {str(e)}")
            return False
    
    async def monitor_continuously(self, session, callback):
        """
        持续监控票务
        
        Args:
            session: aiohttp 会话对象
            callback: 票务可用时的回调函数
        """
        try:
            while True:
                available = await self.check_tickets(session)
                
                if available:
                    logger.warning("🎉 检测到可用票务！")
                    await callback()
                    break
                
                await asyncio.sleep(self.check_interval)
        
        except Exception as e:
            logger.error(f"监控过程中出错: {str(e)}")
    
    def get_stats(self):
        """
        获取监控统计信息
        
        Returns:
            dict: 统计信息
        """
        return {
            'total_checks': self.check_count,
            'last_status': self.last_status,
            'check_interval': self.check_interval
        }