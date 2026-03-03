"""
自动抢票模块 - 处理抢票逻辑
"""
import asyncio
from loguru import logger
from config import GRABBER


class TicketGrabber:
    """自动抢票类"""
    
    def __init__(self):
        """初始化抢票器"""
        self.quantity = GRABBER.get('quantity', 2)
        self.auto_pay = GRABBER.get('auto_pay', True)
        self.max_attempts = GRABBER.get('max_attempts', 5)
        self.attempt_count = 0
    
    async def grab_tickets(self, session):
        """
        自动抢票
        
        Args:
            session: aiohttp 会话对象
        
        Returns:
            bool: 抢票是否成功
        """
        try:
            logger.info(f"开始抢票，数量: {self.quantity}")
            
            # 添加到购物车
            cart_success = await self._add_to_cart(session)
            if not cart_success:
                logger.error("添加到购物车失败")
                return False
            
            logger.info("✅ 已添加到购物车")
            
            # 自动结账
            if self.auto_pay:
                checkout_success = await self._auto_checkout(session)
                if not checkout_success:
                    logger.error("自动结账失败")
                    return False
                
                logger.info("✅ 自动结账成功")
            
            logger.info("🎊 抢票流程完成")
            return True
        
        except Exception as e:
            logger.error(f"抢票过程中出错: {str(e)}")
            return False
    
    async def _add_to_cart(self, session):
        """
        添加到购物车
        
        Args:
            session: aiohttp 会话对象
        
        Returns:
            bool: 是否成功
        """
        try:
            for attempt in range(self.max_attempts):
                try:
                    logger.info(f"尝试添加到购物车 (尝试 {attempt + 1}/{self.max_attempts})...")
                    
                    # 构建请求
                    url = "https://www.ticketmaster.com/api/cart/add"
                    
                    payload = {
                        'ticketTypeId': 'ticket_id',
                        'quantity': self.quantity
                    }
                    
                    async with session.post(url, json=payload) as response:
                        if response.status == 200:
                            logger.info("✅ 成功添加到购物车")
                            return True
                        else:
                            logger.warning(f"添加失败，状态码: {response.status}")
                            await asyncio.sleep(0.5)
                
                except Exception as e:
                    logger.warning(f"第 {attempt + 1} 次尝试失败: {str(e)}")
                    await asyncio.sleep(0.5)
            
            logger.error("多次尝试添加到购物车失败")
            return False
        
        except Exception as e:
            logger.error(f"添加到购物车异常: {str(e)}")
            return False
    
    async def _auto_checkout(self, session):
        """
        自动结账
        
        Args:
            session: aiohttp 会话对象
        
        Returns:
            bool: 是否成功
        """
        try:
            logger.info("开始自动结账...")
            
            # 获取购物车信息
            cart_url = "https://www.ticketmaster.com/api/cart"
            
            async with session.get(cart_url) as response:
                if response.status != 200:
                    logger.error("无法获取购物车信息")
                    return False
                
                cart_data = await response.json()
            
            # 提交订单
            checkout_url = "https://www.ticketmaster.com/api/checkout"
            
            payload = {
                'cart_id': cart_data.get('id'),
                'payment_method': 'credit_card',
                'auto_select': True
            }
            
            async with session.post(checkout_url, json=payload) as response:
                if response.status == 200:
                    logger.info("✅ 结账成功")
                    return True
                else:
                    logger.error(f"结账失败，状态码: {response.status}")
                    return False
        
        except Exception as e:
            logger.error(f"自动结账异常: {str(e)}")
            return False
    
    def get_stats(self):
        """
        获取抢票统计
        
        Returns:
            dict: 统计信息
        """
        return {
            'quantity': self.quantity,
            'auto_pay': self.auto_pay,
            'max_attempts': self.max_attempts,
            'attempt_count': self.attempt_count
        }