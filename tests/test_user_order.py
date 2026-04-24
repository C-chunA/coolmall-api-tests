"""订单接口测试"""
import pytest
import yaml
from pathlib import Path
from utils.request import APIRequest
from utils.assertions import assert_response_code, assert_response_message


def load_test_cases():
    """加载所有测试用例"""
    data_path = Path(__file__).parent.parent / "data" / "user_order.yaml"
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
        
        if func_name.startswith("test_order_"):
            group_name = func_name.replace("test_order_", "")
            if group_name in grouped_cases:
                cases_for_func = grouped_cases[group_name]
                # 生成用例ID，显示为用例名称
                ids = [c["name"] for c in cases_for_func]
                metafunc.parametrize("case", cases_for_func, ids=ids)


@pytest.mark.order
class TestUserOrder:
    """订单测试类"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """测试前置"""
        self.api = APIRequest()
    
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
    
    def _run_test(self, case):
        """执行测试"""
        response = self._send_request(case)
        
        # 断言 code
        assert_response_code(response, case["expected"]["code"])
        
        # 断言 message（如果有）
        if "message" in case["expected"]:
            assert_response_message(response, case["expected"]["message"])
    
    @pytest.mark.smoke
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
                # 检查是否实际创建成功（code=1000 且有订单id）
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
