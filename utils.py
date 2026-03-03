"""
工具函数 - 公共工具方法
"""
import json
import hashlib
from datetime import datetime
from loguru import logger


class TimeUtils:
    """时间工具类"""
    
    @staticmethod
    def get_current_time():
        """获取当前时间"""
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    @staticmethod
    def timestamp():
        """获取当前时间戳"""
        return int(datetime.now().timestamp() * 1000)


class RequestUtils:
    """请求工具类"""
    
    @staticmethod
    def generate_request_id():
        """生成请求 ID"""
        timestamp = TimeUtils.timestamp()
        request_id = hashlib.md5(str(timestamp).encode()).hexdigest()
        return request_id
    
    @staticmethod
    def generate_signature(data, secret):
        """
        生成签名
        
        Args:
            data: 数据
            secret: 密钥
        
        Returns:
            str: 签名
        """
        content = json.dumps(data) + secret
        signature = hashlib.sha256(content.encode()).hexdigest()
        return signature


class RetryUtils:
    """重试工具类"""
    
    @staticmethod
    async def retry_async(func, max_retries=3, delay=1, backoff=2):
        """
        异步重试装饰器
        
        Args:
            func: 要重试的异步函数
            max_retries: 最大重试次数
            delay: 初始延迟时间
            backoff: 延迟倍数
        
        Returns:
            任意: 函数返回值
        """
        import asyncio
        
        last_exception = None
        current_delay = delay
        
        for attempt in range(max_retries):
            try:
                return await func()
            except Exception as e:
                last_exception = e
                logger.warning(f"重试 {attempt + 1}/{max_retries} 失败: {str(e)}")
                
                if attempt < max_retries - 1:
                    await asyncio.sleep(current_delay)
                    current_delay *= backoff
        
        raise last_exception


class DataUtils:
    """数据工具类"""
    
    @staticmethod
    def safe_get(data, key, default=None):
        """安全获取字典值"""
        
        Args:
            data: 字典数据
            key: 键
            default: 默认值
        
        Returns:
            任意: 值或默认值
        """
        try:
            return data.get(key, default)
        except:
            return default
    
    @staticmethod
    def format_error_message(error):
        """格式化错误信息"""
        
        Args:
            error: 异常对象
        
        Returns:
            str: 格式化的错误信息
        """
        error_type = type(error).__name__
        error_msg = str(error)
        return f"{error_type}: {error_msg}"


class LogUtils:
    """日志工具类"""
    
    @staticmethod
    def log_request(url, method='GET', data=None):
        """记录请求"""
        logger.debug(f"Request: {method} {url}")
        if data:
            logger.debug(f"Data: {data}")
    
    @staticmethod
    def log_response(status_code, response_data=None):
        """记录响应"""
        logger.debug(f"Response Status: {status_code}")
        if response_data:
            logger.debug(f"Response: {response_data}")