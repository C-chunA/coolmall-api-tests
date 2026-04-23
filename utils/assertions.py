"""断言封装"""
import json
from .logger import log_assertion


def assert_response_code(response, expected_code=1000):
    """断言响应 code"""
    try:
        data = response.json()
    except:
        raise AssertionError(f"响应不是 JSON 格式: {response.text}")
    
    actual_code = data.get("code")
    # 支持数字和字符串的自动转换比较
    result = str(actual_code) == str(expected_code)
    log_assertion("响应状态码 / Response Code", expected_code, actual_code, result)
    
    assert result, f"期望 code={expected_code}, 实际 code={actual_code}, message={data.get('message')}"


def assert_response_message(response, expected_message):
    """断言响应 message"""
    data = response.json()
    actual_message = data.get("message")
    result = actual_message == expected_message
    log_assertion("响应消息 / Response Message", expected_message, actual_message, result)
    
    assert result, f"期望 message='{expected_message}', 实际 message='{actual_message}'"


def assert_response_field(response, field_path, expected_value):
    """
    断言响应字段值
    
    Args:
        response: Response 对象
        field_path: 字段路径，如 "data.token" 或 "data.user.name"
        expected_value: 期望值
    """
    data = response.json()
    
    # 按路径获取字段值
    keys = field_path.split(".")
    actual_value = data
    for key in keys:
        if isinstance(actual_value, dict):
            actual_value = actual_value.get(key)
        else:
            raise AssertionError(f"无法获取字段 '{field_path}'，中间值不是字典: {actual_value}")
    
    result = actual_value == expected_value
    log_assertion(f"字段值 / Field Value [{field_path}]", expected_value, actual_value, result)
    
    assert result, f"字段 '{field_path}' 期望值={expected_value}, 实际值={actual_value}"


def assert_response_field_exists(response, field_path):
    """断言字段存在"""
    data = response.json()
    keys = field_path.split(".")
    actual_value = data
    
    exists = True
    for key in keys:
        if isinstance(actual_value, dict) and key in actual_value:
            actual_value = actual_value[key]
        else:
            exists = False
            break
    
    log_assertion(f"字段存在 / Field Exists [{field_path}]", "存在", "存在" if exists else "不存在", exists)
    
    if not exists:
        raise AssertionError(f"字段 '{field_path}' 不存在")


def assert_response_field_type(response, field_path, expected_type):
    """断言字段类型"""
    data = response.json()
    keys = field_path.split(".")
    actual_value = data
    
    for key in keys:
        if isinstance(actual_value, dict):
            actual_value = actual_value.get(key)
        else:
            raise AssertionError(f"无法获取字段 '{field_path}'")
    
    result = isinstance(actual_value, expected_type)
    log_assertion(f"字段类型 / Field Type [{field_path}]", expected_type.__name__, type(actual_value).__name__, result)
    
    assert result, f"字段 '{field_path}' 期望类型={expected_type.__name__}, 实际类型={type(actual_value).__name__}"


def get_response_data(response):
    """获取响应 data 字段"""
    data = response.json()
    return data.get("data")
