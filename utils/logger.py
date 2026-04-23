"""日志配置"""
import logging
import sys
from pathlib import Path
from datetime import datetime


class DailyFileHandler(logging.FileHandler):
    """按日期生成日志文件"""
    
    def __init__(self, log_dir, encoding='utf-8'):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.encoding = encoding
        self.current_date = datetime.now().strftime('%Y-%m-%d')
        filename = self.log_dir / f"{self.current_date}.log"
        super().__init__(filename, encoding=encoding)
    
    def emit(self, record):
        """检查日期变化，需要时切换文件"""
        current_date = datetime.now().strftime('%Y-%m-%d')
        if current_date != self.current_date:
            self.current_date = current_date
            self.baseFilename = str(self.log_dir / f"{current_date}.log")
            if self.stream:
                self.stream.close()
            self.stream = self._open()
        super().emit(record)


def setup_logger(name='api_test'):
    """配置日志"""
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    # 清除已有处理器
    logger.handlers.clear()
    
    # 日志格式：时间(毫秒) | 级别 | 消息
    formatter = logging.Formatter(
        '[%(asctime)s.%(msecs)03d] [%(levelname)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # 文件处理器（按日期）
    log_dir = Path(__file__).parent.parent / "logs"
    file_handler = DailyFileHandler(log_dir)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    # 控制台处理器
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    return logger


# 全局 logger
logger = setup_logger()


def log_test_start(test_file, test_name, description=None):
    """记录测试开始"""
    logger.info("")
    logger.info("=" * 80)
    logger.info(f"[测试开始] {test_file} - {test_name}")
    if description:
        logger.info(f"[测试内容] {description}")
    logger.info("-" * 80)


def log_test_end(test_file, test_name, status, duration=None):
    """记录测试结束"""
    duration_str = f" ({duration:.3f}s)" if duration else ""
    if status == "PASSED":
        logger.info(f"[测试通过] {test_name}{duration_str}")
    else:
        logger.info(f"[测试失败] {test_name}{duration_str}")
    logger.info("=" * 80)
    logger.info("")


def log_request(method, url, headers, payload):
    """记录请求"""
    logger.info(f"[请求] {method} {url}")
    # 移除敏感信息
    safe_headers = dict(headers)
    if 'Authorization' in safe_headers:
        safe_headers['Authorization'] = '***'
    logger.debug(f"  [请求头] {safe_headers}")
    if payload:
        logger.debug(f"  [请求体] {payload}")


def log_response(status_code, response_body):
    """记录响应"""
    logger.info(f"[响应] 状态码: {status_code}")
    logger.debug(f"  [响应体] {response_body}")


def log_assertion(assert_name, expected, actual, result):
    """记录断言"""
    status = "通过" if result else "失败"
    logger.info(f"[断言] {assert_name}")
    logger.info(f"  预期: {expected}")
    logger.info(f"  实际: {actual}")
    logger.info(f"  结果: {status}")


def log_file_start(file_name):
    """记录测试文件开始"""
    logger.info("")
    logger.info("#" * 80)
    logger.info(f"# [测试文件] {file_name}")
    logger.info("#" * 80)


def log_file_end(file_name):
    """记录测试文件结束"""
    logger.info("#" * 80)
    logger.info(f"# [测试文件结束] {file_name}")
    logger.info("#" * 80)
    logger.info("")
