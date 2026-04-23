"""收货地址接口测试 - 动态生成测试函数版本"""
import pytest
import yaml
from pathlib import Path
from utils.request import APIRequest
from utils.assertions import assert_response_code, assert_response_message, assert_response_field_exists


def load_test_cases():
    """加载所有测试用例"""
    data_path = Path(__file__).parent.parent / "data" / "user_address.yaml"
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
        
        if func_name.startswith("test_address_"):
            group_name = func_name.replace("test_address_", "")
            if group_name in grouped_cases:
                cases_for_func = grouped_cases[group_name]
                # 生成用例ID，显示为用例名称
                ids = [c["name"] for c in cases_for_func]
                metafunc.parametrize("case", cases_for_func, ids=ids)


class TestUserAddress:
    """收货地址测试类"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """测试前置"""
        self.api = APIRequest()
    
    def teardown_method(self):
        """测试后置：清理创建的地址"""
        # 这里不需要额外清理，每个用例内部已处理
        pass
    
    def _send_request(self, case):
        """发送请求并返回响应"""
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
    
    def _cleanup_address(self, response):
        """如果响应包含id，则删除该地址"""
        try:
            data = response.json()
            # 无论code是什么，只要有id就删除
            address_id = data.get("data", {}).get("id")
            if address_id:
                self.api.post("/app/user/address/delete", payload={"ids": [address_id]})
        except:
            pass
    
    def _run_test(self, case):
        """执行测试并清理"""
        response = self._send_request(case)
        
        try:
            # 断言 code
            assert_response_code(response, case["expected"]["code"])
            
            # 断言 message（如果有）
            if "message" in case["expected"]:
                assert_response_message(response, case["expected"]["message"])
            
            # 验证返回字段（如果有）
            if "data_fields" in case["expected"]:
                for field in case["expected"]["data_fields"]:
                    assert_response_field_exists(response, f"data.{field}")
        finally:
            # 清理：无论测试成功与否，如果创建了地址，删除它
            self._cleanup_address(response)
    
    def test_address_add(self, case):
        """测试添加收货地址接口"""
        self._run_test(case)
    
    def test_address_page(self, case):
        """测试分页查询收货地址接口"""
        self._run_test(case)
    
    def test_address_update(self, case):
        """测试更新收货地址接口 - 先创建地址再更新"""
        # 先创建一条地址数据
        add_response = self.api.post("/app/user/address/add", payload={
            "contact": "测试联系人",
            "phone": "13800138000",
            "province": "江苏省",
            "city": "南京市",
            "district": "鼓楼区",
            "address": "测试街道123号",
            "isDefault": False
        })
        add_data = add_response.json()
        address_id = add_data.get("data", {}).get("id")
        
        # 更新用例的payload，添加实际id
        case_copy = case.copy()
        case_copy["payload"] = case["payload"].copy()
        case_copy["payload"]["id"] = address_id
        
        try:
            self._run_test(case_copy)
        finally:
            # 清理：删除创建的地址
            if address_id:
                self.api.post("/app/user/address/delete", payload={"ids": [address_id]})
    
    def test_address_delete(self, case):
        """测试删除收货地址接口"""
        self._run_test(case)
    
    def test_address_info(self, case):
        """测试查询地址信息接口 - 先创建地址再查询"""
        # 先创建一条地址数据
        add_response = self.api.post("/app/user/address/add", payload={
            "contact": "测试联系人",
            "phone": "13800138000",
            "province": "江苏省",
            "city": "南京市",
            "district": "鼓楼区",
            "address": "测试街道123号",
            "isDefault": False
        })
        add_data = add_response.json()
        address_id = add_data.get("data", {}).get("id")
        
        # 更新用例的payload为实际id
        case_copy = case.copy()
        case_copy["payload"] = {"id": address_id}
        
        try:
            self._run_test(case_copy)
        finally:
            # 清理：删除创建的地址
            if address_id:
                self.api.post("/app/user/address/delete", payload={"ids": [address_id]})
    
    def test_address_list(self, case):
        """测试查询地址列表接口"""
        self._run_test(case)
    
    def test_address_default(self, case):
        """测试查询默认地址接口"""
        self._run_test(case)
