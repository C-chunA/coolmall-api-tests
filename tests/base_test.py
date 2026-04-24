"""API 测试基础类"""
import pytest
import yaml
from pathlib import Path
from utils.request import APIRequest
from utils.assertions import assert_response_code, assert_response_message, assert_response_field_exists


def load_test_cases(data_file):
    """加载测试数据"""
    data_path = Path(__file__).parent.parent / "data" / data_file
    with open(data_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data["test_cases"]


def pytest_generate_tests_base(metafunc, data_file, method_prefix):
    """通用测试生成函数"""
    if "case" in metafunc.fixturenames:
        cases = load_test_cases(data_file)
        
        # 按接口最后一个单词分组
        grouped_cases = {}
        for case in cases:
            endpoint = case["endpoint"]
            group_name = endpoint.split("/")[-1]
            if group_name not in grouped_cases:
                grouped_cases[group_name] = []
            grouped_cases[group_name].append(case)
        
        # 根据函数名决定加载哪组用例
        func_name = metafunc.function.__name__
        
        if func_name.startswith(method_prefix):
            group_name = func_name.replace(method_prefix, "")
            if group_name in grouped_cases:
                cases_for_func = grouped_cases[group_name]
                ids = [c["name"] for c in cases_for_func]
                metafunc.parametrize("case", cases_for_func, ids=ids)


class BaseAPITest:
    """API 测试基础类"""
    
    # 子类必须定义
    data_file = None
    test_method_prefix = "test_"
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """测试前置：初始化 API 客户端"""
        self.api = APIRequest()
    
    def _send_request(self, case):
        """发送请求"""
        method = case.get("method", "POST")
        endpoint = case["endpoint"]
        payload = case.get("payload", {})
        
        if method == "GET":
            if "?" in endpoint or not payload:
                return self.api.get(endpoint)
            else:
                params = "&".join([f"{k}={v}" for k, v in payload.items()])
                return self.api.get(f"{endpoint}?{params}")
        else:
            return self.api.post(endpoint, payload=payload)
    
    def _run_test(self, case):
        """执行测试并断言"""
        response = self._send_request(case)
        
        # 断言 code
        assert_response_code(response, case["expected"]["code"])
        
        # 断言 message（如果有）
        if "message" in case["expected"]:
            assert_response_message(response, case["expected"]["message"])
        
        # 验证返回字段（如果有）
        if "data_fields" in case["expected"]:
            for field in case["expected"]["data_fields"]:
                assert_response_field_exists(response, f"data.{field}")
        
        return response
