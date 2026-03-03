"""
自动登录模块 - 处理账户登录
"""
import asyncio
import aiohttp
from loguru import logger
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TicketAuthenticator:
    """票务系统认证类"""
    
    def __init__(self, account_config):
        """
        初始化认证器
        
        Args:
            account_config: 账户配置字典
        """
        self.username = account_config.get('username')
        self.password = account_config.get('password')
        self.platform = account_config.get('platform', 'ticketmaster')
        self.session = None
        self.driver = None
    
    async def login(self):
        """
        异步登录方法
        
        Returns:
            aiohttp.ClientSession: 登录后的会话对象，失败返回None
        """
        try:
            logger.info(f"正在登录到 {self.platform}...")
            
            # 根据平台选择登录方式
            if self.platform == 'ticketmaster':
                return await self._login_ticketmaster()
            elif self.platform == 'livenation':
                return await self._login_livenation()
            else:
                logger.warning(f"未知的平台: {self.platform}")
                return None
        
        except Exception as e:
            logger.error(f"登录失败: {str(e)}")
            return None
    
    async def _login_ticketmaster(self):
        """
        Ticketmaster 平台登录
        
        Returns:
            aiohttp.ClientSession: 登录后的会话
        """
        try:
            # 使用 Selenium 进行 Web 自动化登录
            self.driver = webdriver.Chrome()
            
            logger.info("打开 Ticketmaster 登录页面...")
            self.driver.get("https://www.ticketmaster.com/login")
            
            # 等待登录表单加载
            wait = WebDriverWait(self.driver, 10)
            
            # 输入用户名
            username_field = wait.until(
                EC.presence_of_element_located((By.ID, "username"))
            )
            username_field.send_keys(self.username)
            
            # 输入密码
            password_field = self.driver.find_element(By.ID, "password")
            password_field.send_keys(self.password)
            
            # 点击登录按钮
            login_button = self.driver.find_element(By.ID, "login-submit")
            login_button.click()
            
            # 等待登录完成
            await asyncio.sleep(3)
            
            # 获取 Cookie 和 Session
            cookies = self.driver.get_cookies()
            
            # 创建 aiohttp 会话并设置 Cookie
            self.session = aiohttp.ClientSession()
            
            for cookie in cookies:
                self.session.cookie_jar.update_cookies(
                    {cookie['name']: cookie['value']}
                )
            
            logger.info("✅ Ticketmaster 登录成功")
            return self.session
        
        except Exception as e:
            logger.error(f"Ticketmaster 登录失败: {str(e)}")
            if self.driver:
                self.driver.quit()
            return None
    
    async def _login_livenation(self):
        """
        LiveNation 平台登录
        
        Returns:
            aiohttp.ClientSession: 登录后的会话
        """
        try:
            # 类似的登录逻辑
            self.session = aiohttp.ClientSession()
            
            login_url = "https://www.livenation.com/login"
            
            async with self.session.post(
                login_url,
                data={
                    'username': self.username,
                    'password': self.password
                }
            ) as response:
                if response.status == 200:
                    logger.info("✅ LiveNation 登录成功")
                    return self.session
                else:
                    logger.error(f"LiveNation 登录失败，状态码: {response.status}")
                    return None
        
        except Exception as e:
            logger.error(f"LiveNation 登录失败: {str(e)}")
            return None
    
    async def logout(self):
        """退出登录"""
        try:
            if self.driver:
                self.driver.quit()
            
            if self.session:
                await self.session.close()
            
            logger.info("已退出登录")
        
        except Exception as e:
            logger.error(f"退出登录失败: {str(e)}")