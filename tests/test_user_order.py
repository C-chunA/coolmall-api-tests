"""订单接口测试"""
import pytest
from tests.base_test import BaseAPITest, pytest_generate_tests_base
from utils.assertions import assert_response_code, assert_response_message


def pytest_generate_tests(metafunc):
    """动态生成测试函数"""
    pytest_generate_tests_base(metafunc, "user_order.yaml", "test_order_")


@pytest.mark.order
class TestUserOrder(BaseAPITest):
    """订单测试类"""
    
    def test_order_create(self, case):
        """测试创建订单接口"""
        response = self._send_request(case)
        
        # 先获取响应数据用于后置清理
        try:
            response_data = response.json()
        except:
            response_data = {}
        
        try:
            # 断言 code
            assert_response_code(response, case["expected"]["code"])
            
            # 断言 message（如果有）
            if "message" in case["expected"]:
                assert_response_message(response, case["expected"]["message"])
        finally:
            # 后置操作：如果实际创建订单成功（返回code=1000且有id），立即取消订单
            try:
                if response_data.get("code") == 1000:
                    order_id = response_data.get("data", {}).get("id")
                    if order_id:
                        cancel_payload = {
                            "orderId": order_id,
                            "remark": "测试后清理"
                        }
                        cancel_response = self.api.post("/app/order/info/cancel", payload=cancel_payload)
                        print(f"取消订单结果: orderId={order_id}, code={cancel_response.json().get('code')}")
            except Exception as e:
                print(f"取消订单失败: {e}")
    
    def test_order_page(self, case):
        """测试订单列表分页接口"""
        self._run_test(case)
    
    def test_order_info(self, case):
        """测试订单详情查询接口"""
        self._run_test(case)
    
    def test_order_userCount(self, case):
        """测试用户订单统计接口"""
        self._run_test(case)
    
    def test_order_logistics(self, case):
        """测试物流信息查询接口"""
        self._run_test(case)
    
    def test_order_confirm(self, case):
        """测试确认收货接口"""
        self._run_test(case)
