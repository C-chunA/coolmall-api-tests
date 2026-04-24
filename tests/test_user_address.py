"""收货地址接口测试"""
import pytest
from tests.base_test import BaseAPITest, pytest_generate_tests_base
from utils.assertions import assert_response_code, assert_response_message, assert_response_field_exists


def pytest_generate_tests(metafunc):
    """动态生成测试函数"""
    pytest_generate_tests_base(metafunc, "user_address.yaml", "test_address_")


@pytest.mark.address
class TestUserAddress(BaseAPITest):
    """收货地址测试类"""
    
    def _cleanup_address(self, response):
        """如果响应包含id，则删除该地址"""
        try:
            data = response.json()
            address_id = data.get("data", {}).get("id")
            if address_id:
                self.api.post("/app/user/address/delete", payload={"ids": [address_id]})
        except:
            pass
    
    def _run_test_with_cleanup(self, case):
        """执行测试并清理"""
        response = self._send_request(case)
        
        try:
            assert_response_code(response, case["expected"]["code"])
            if "message" in case["expected"]:
                assert_response_message(response, case["expected"]["message"])
            if "data_fields" in case["expected"]:
                for field in case["expected"]["data_fields"]:
                    assert_response_field_exists(response, f"data.{field}")
        finally:
            self._cleanup_address(response)
        
        return response
    
    @pytest.mark.smoke
    def test_address_add(self, case):
        """测试添加收货地址接口"""
        self._run_test_with_cleanup(case)
    
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
            if address_id:
                self.api.post("/app/user/address/delete", payload={"ids": [address_id]})
    
    def test_address_delete(self, case):
        """测试删除收货地址接口"""
        self._run_test(case)
    
    def test_address_info(self, case):
        """测试查询地址信息接口 - 先创建地址再查询"""
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
        
        case_copy = case.copy()
        case_copy["payload"] = {"id": address_id}
        
        try:
            self._run_test(case_copy)
        finally:
            if address_id:
                self.api.post("/app/user/address/delete", payload={"ids": [address_id]})
    
    def test_address_list(self, case):
        """测试查询地址列表接口"""
        self._run_test(case)
    
    def test_address_default(self, case):
        """测试查询默认地址接口"""
        self._run_test(case)
