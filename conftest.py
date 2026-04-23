"""pytest 配置和全局 fixture"""
import pytest
import shutil
import time
from pathlib import Path
from utils.token_manager import get_token_manager
from utils.request import APIRequest
from utils.logger import log_test_start, log_test_end, log_file_start, log_file_end


# Allure 报告目录
ALLURE_RESULTS_DIR = Path(__file__).parent / "reports" / "allure-results"


# 存储测试开始时间
_test_start_times = {}


def pytest_configure(config):
    """pytest 配置：清空 allure 历史记录"""
    config.addinivalue_line("markers", "smoke: 冒烟测试")
    config.addinivalue_line("markers", "user: 用户模块测试")
    config.addinivalue_line("markers", "address: 收货地址模块测试")
    
    # 清空 allure-results 目录
    if ALLURE_RESULTS_DIR.exists():
        shutil.rmtree(ALLURE_RESULTS_DIR)
    ALLURE_RESULTS_DIR.mkdir(parents=True, exist_ok=True)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """在测试执行后设置测试结果属性"""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)


@pytest.fixture(autouse=True)
def log_test_wrapper(request):
    """自动记录测试开始和结束"""
    test_file = request.module.__name__
    test_name = request.node.name
    
    # 获取测试函数的描述（docstring）
    test_doc = request.node.function.__doc__
    
    # 测试开始
    log_test_start(test_file, test_name, test_doc)
    start_time = time.time()
    
    yield
    
    # 测试结束
    duration = time.time() - start_time
    # 从 request.node 获取测试结果
    if hasattr(request.node, 'rep_call'):
        if request.node.rep_call.failed:
            status = "FAILED"
        elif request.node.rep_call.passed:
            status = "PASSED"
        else:
            status = "COMPLETED"
    else:
        status = "COMPLETED"
    log_test_end(test_file, test_name, status, duration)


def pytest_sessionstart(session):
    """测试会话开始"""
    log_file_start("Test Session")


def pytest_sessionfinish(session, exitstatus):
    """测试会话结束"""
    log_file_end("Test Session")


@pytest.fixture(scope="session")
def token():
    """session 级别的 token fixture"""
    token_manager = get_token_manager()
    return token_manager.get_token()


@pytest.fixture(scope="session")
def api_client():
    """API 请求客户端"""
    return APIRequest()


@pytest.fixture(scope="session")
def auth_headers():
    """带认证信息的请求头"""
    token_manager = get_token_manager()
    return token_manager.get_auth_header()


@pytest.fixture(scope="function")
def temp_address(api_client, auth_headers):
    """
    临时收货地址 fixture
    创建测试地址，用例结束后自动删除
    """
    # 创建地址
    address_data = {
        "contact": "测试联系人",
        "phone": "13800138000",
        "province": "江苏省",
        "city": "南京市",
        "district": "鼓楼区",
        "address": "测试街道123号",
        "isDefault": False
    }
    
    response = api_client.post("/app/user/address/add", payload=address_data)
    
    if response.json().get("code") == 1000:
        address_id = response.json().get("data", {}).get("id")
        yield {"id": address_id, **address_data}
        
        # 清理：删除地址
        try:
            api_client.post("/app/user/address/delete", payload={"ids": [address_id]})
        except:
            pass  # 清理失败不影响测试结果
    else:
        yield None
