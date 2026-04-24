"""用户信息接口测试 - 动态生成测试函数版本"""
import pytest
import yaml
from pathlib import Path
from utils.request import APIRequest
from utils.assertions import assert_response_code, assert_response_message, assert_response_field_exists


def load_test_cases():
    """加载所有测试用例"""
    data_path = Path(__file__).parent.parent / "data" / "user_info.yaml"
    with open(data_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data["test_cases"]


def pytest_generate_tests(metafunc):
    """动态生成测试函数"""
    if "case" in metafunc.fixturenames:
        cases = load_test_cases()
        
        # 按接口最后一个单词分组
        grouped_cases = {}
        for case in cases:
            endpoint = case["endpoint"]
            # 提取接口最后一个单词作为分组名
            group_name = endpoint.split("/")[-1]
            if group_name not in grouped_cases:
                grouped_cases[group_name] = []
            grouped_cases[group_name].append(case)
        
        # 根据当前测试函数名决定加载哪组用例
        func_name = metafunc.function.__name__
        
        if func_name.startswith("test_user_info_"):
            group_name = func_name.replace("test_user_info_", "")
            if group_name in grouped_cases:
                cases_for_func = grouped_cases[group_name]
                # 生成用例ID，显示为用例名称
                ids = [c["name"] for c in cases_for_func]
                metafunc.parametrize("case", cases_for_func, ids=ids)


@pytest.mark.user
class TestUserInfo:
    """用户信息测试类"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """测试前置：初始化 API 客户端"""
        self.api = APIRequest()
    
    def _send_request(self, case):
        """发送请求并返回响应"""
        method = case.get("method", "GET")
        endpoint = case["endpoint"]
        headers = case.get("headers", {})
        
        # 判断是否使用 Token
        # 如果 headers 里有 Authorization，说明是 Token 测试场景，禁用自动 Token
        use_token = not bool(headers)
        
        if method == "GET":
            return self.api.get(endpoint, headers=headers if headers else None, use_token=use_token)
        else:
            return self.api.post(
                endpoint,
                payload=case.get("payload", {}),
                headers=headers if headers else None,
                use_token=use_token
            )
    
    def _run_test(self, case):
        """执行测试"""
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
    
    @pytest.mark.smoke
    def test_user_info_person(self, case):
        """测试获取用户个人信息接口"""
        self._run_test(case)
