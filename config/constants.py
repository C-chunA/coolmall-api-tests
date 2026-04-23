"""常量定义"""

# 成功状态码
SUCCESS_CODE = 1000

# 请求头
DEFAULT_HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}

# 超时设置
TIMEOUT = 30

# 重试配置
MAX_RETRIES = 0  # 不重试
