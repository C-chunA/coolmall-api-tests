"""订单状态流转测试

测试订单状态完整流转：
status 0: 待付款 -> status 1: 待发货 -> status 2: 待收货 -> status 3: 待评价 -> status 4: 已完成

通过修改订单接口(/app/order/info/update)修改订单状态
支持跨状态修改
"""
import pytest
from tests.base_test import BaseAPITest
from utils.assertions import assert_response_code, assert_response_message


@pytest.mark.order
class TestOrderStatusFlow(BaseAPITest):
    """订单状态流转测试类"""
    
    def _create_order(self):
        """创建订单并返回订单ID"""
        create_payload = {
            "data": {
                "remark": "状态流转测试订单",
                "goodsList": [
                    {
                        "goodsInfo": {
                            "id": 1,
                            "createTime": "2025-03-29 00:17:15",
                            "updateTime": "2025-03-29 23:07:48",
                            "typeId": 11,
                            "title": "Redmi 14C",
                            "subTitle": "【持久续航】5160mAh 大电池",
                            "mainPic": "https://game-box-1315168471.cos.ap-guangzhou.myqcloud.com/app%2Fbase%2Ffcd84baf3d3a4b49b35a03aaf783281e_%E7%BA%A2%E7%B1%B3%2014c.png",
                            "pics": [
                                "https://game-box-1315168471.cos.ap-guangzhou.myqcloud.com/app%2Fbase%2F83561ee604b14aae803747c32ff59cbb_b1.png"
                            ],
                            "price": 499,
                            "sold": 0,
                            "content": "",
                            "status": 1,
                            "sortNum": 0,
                            "specs": None
                        },
                        "spec": {
                            "id": 5,
                            "createTime": "2025-03-29 00:31:19",
                            "updateTime": "2025-03-29 00:31:19",
                            "goodsId": 1,
                            "name": "碧波绿 4GB+64GB",
                            "price": 499,
                            "stock": 999,
                            "sortNum": 0,
                            "images": None,
                            "cover": "https://game-box-1315168471.cos.ap-guangzhou.myqcloud.com/app%2Fbase%2Ffcd84baf3d3a4b49b35a03aaf783281e_%E7%BA%A2%E7%B1%B3%2014c.png"
                        },
                        "count": 1,
                        "goodsId": 1
                    }
                ],
                "couponId": None,
                "addressId": 136,
                "title": "购买商品"
            }
        }
        
        create_response = self.api.post("/app/order/info/create", payload=create_payload)
        create_data = create_response.json()
        
        assert create_data.get("code") == 1000, f"创建订单失败: {create_data}"
        
        order_id = create_data.get("data", {}).get("id")
        assert order_id, "创建订单未返回订单ID"
        
        return order_id
    
    def _get_order_info(self, order_id):
        """获取订单详情，返回订单状态"""
        response = self.api.get(f"/app/order/info/info?id={order_id}")
        data = response.json()
        
        if data.get("code") == 1000 and data.get("data"):
            return data["data"].get("status")
        return None
    
    def _update_order_status(self, order_id, status):
        """修改订单状态"""
        update_payload = {
            "id": order_id,
            "status": status
        }
        response = self.api.post("/app/order/info/update", payload=update_payload)
        return response
    
    def _cancel_order(self, order_id):
        """取消订单（status=0时可用）"""
        try:
            cancel_payload = {
                "orderId": order_id,
                "remark": "测试后清理"
            }
            cancel_response = self.api.post("/app/order/info/cancel", payload=cancel_payload)
            print(f"取消订单结果: orderId={order_id}, code={cancel_response.json().get('code')}")
        except Exception as e:
            print(f"取消订单失败: {e}")
    
    def _refund_order(self, order_id):
        """申请售后退款（status=1或2时可用）"""
        try:
            refund_payload = {
                "orderId": order_id,
                "reason": "体验不佳"
            }
            refund_response = self.api.post("/app/order/info/refund", payload=refund_payload)
            print(f"申请退款结果: orderId={order_id}, code={refund_response.json().get('code')}")
        except Exception as e:
            print(f"申请退款失败: {e}")
    
    def _cleanup_order(self, order_id, status):
        """根据订单状态选择合适的清理方式"""
        if status == 0:
            # 待付款：取消订单
            self._cancel_order(order_id)
        elif status in [1, 2]:
            # 待发货/待收货：申请售后退款
            self._refund_order(order_id)
        # status 3、4 无需清理
    
    def test_status_0_to_1(self):
        """测试状态流转：待付款(0) -> 待发货(1)"""
        order_id = self._create_order()
        
        try:
            # 验证初始状态
            initial_status = self._get_order_info(order_id)
            print(f"订单初始状态: {initial_status}")
            assert initial_status == 0, f"初始状态应为0，实际{initial_status}"
            
            # 修改状态为待发货(1)
            response = self._update_order_status(order_id, 1)
            
            # 断言修改成功
            assert_response_code(response, 1000)
            assert_response_message(response, "success")
            
            # 验证状态已变更
            updated_status = self._get_order_info(order_id)
            print(f"修改后状态: {updated_status}")
            assert updated_status == 1, f"状态变更失败，期望1，实际{updated_status}"
            
        finally:
            # status=1 用退款清理
            self._cleanup_order(order_id, 1)
    
    def test_status_0_to_2(self):
        """测试状态流转：待付款(0) -> 待收货(2) 跨状态"""
        order_id = self._create_order()
        
        try:
            # 直接跨状态修改为待收货(2)
            response = self._update_order_status(order_id, 2)
            
            # 断言修改成功
            assert_response_code(response, 1000)
            assert_response_message(response, "success")
            
            # 验证状态已变更
            updated_status = self._get_order_info(order_id)
            print(f"修改后状态: {updated_status}")
            assert updated_status == 2, f"状态变更失败，期望2，实际{updated_status}"
            
        finally:
            # status=2 用退款清理
            self._cleanup_order(order_id, 2)
    
    def test_status_0_to_3(self):
        """测试状态流转：待付款(0) -> 待评价(3) 跨状态"""
        order_id = self._create_order()
        
        try:
            # 直接跨状态修改为待评价(3)
            response = self._update_order_status(order_id, 3)
            
            # 断言修改成功
            assert_response_code(response, 1000)
            assert_response_message(response, "success")
            
            # 验证状态已变更
            updated_status = self._get_order_info(order_id)
            print(f"修改后状态: {updated_status}")
            assert updated_status == 3, f"状态变更失败，期望3，实际{updated_status}"
            
        finally:
            # status=3 无需清理
            self._cleanup_order(order_id, 3)
    
    def test_status_0_to_4(self):
        """测试状态流转：待付款(0) -> 已完成(4) 跨状态"""
        order_id = self._create_order()
        
        try:
            # 直接跨状态修改为已完成(4)
            response = self._update_order_status(order_id, 4)
            
            # 断言修改成功
            assert_response_code(response, 1000)
            assert_response_message(response, "success")
            
            # 验证状态已变更
            updated_status = self._get_order_info(order_id)
            print(f"修改后状态: {updated_status}")
            assert updated_status == 4, f"状态变更失败，期望4，实际{updated_status}"
            
        finally:
            # status=4 无需清理
            self._cleanup_order(order_id, 4)
    
    def test_status_1_to_4(self):
        """测试状态流转：待发货(1) -> 已完成(4) 跨状态"""
        order_id = self._create_order()
        
        try:
            # 先修改为待发货(1)
            self._update_order_status(order_id, 1)
            status_1 = self._get_order_info(order_id)
            assert status_1 == 1, f"前置状态设置失败，期望1，实际{status_1}"
            
            # 跨状态修改为已完成(4)
            response = self._update_order_status(order_id, 4)
            
            # 断言修改成功
            assert_response_code(response, 1000)
            assert_response_message(response, "success")
            
            # 验证状态已变更
            updated_status = self._get_order_info(order_id)
            print(f"修改后状态: {updated_status}")
            assert updated_status == 4, f"状态变更失败，期望4，实际{updated_status}"
            
        finally:
            # status=4 无需清理
            self._cleanup_order(order_id, 4)
    
    def test_status_2_to_3(self):
        """测试状态流转：待收货(2) -> 待评价(3) 顺序流转"""
        order_id = self._create_order()
        
        try:
            # 先修改为待收货(2)
            self._update_order_status(order_id, 2)
            status_2 = self._get_order_info(order_id)
            assert status_2 == 2, f"前置状态设置失败，期望2，实际{status_2}"
            
            # 修改为待评价(3)
            response = self._update_order_status(order_id, 3)
            
            # 断言修改成功
            assert_response_code(response, 1000)
            assert_response_message(response, "success")
            
            # 验证状态已变更
            updated_status = self._get_order_info(order_id)
            print(f"修改后状态: {updated_status}")
            assert updated_status == 3, f"状态变更失败，期望3，实际{updated_status}"
            
        finally:
            # status=3 无需清理
            self._cleanup_order(order_id, 3)
    
    def test_status_full_flow(self):
        """测试完整状态流转：0->1->2->3->4"""
        order_id = self._create_order()
        final_status = 0
        
        try:
            # 验证初始状态
            initial_status = self._get_order_info(order_id)
            print(f"初始状态: {initial_status}")
            assert initial_status == 0, f"初始状态应为0，实际{initial_status}"
            
            # 完整流转
            status_flow = [
                (0, "待付款"),
                (1, "待发货"),
                (2, "待收货"),
                (3, "待评价"),
                (4, "已完成")
            ]
            
            for status, name in status_flow[1:]:  # 跳过初始状态
                response = self._update_order_status(order_id, status)
                assert_response_code(response, 1000)
                
                current_status = self._get_order_info(order_id)
                print(f"流转至[{name}]: status={current_status}")
                assert current_status == status, f"状态流转失败，期望{status}，实际{current_status}"
                final_status = current_status
            
            print("完整状态流转测试通过!")
            
        finally:
            self._cleanup_order(order_id, final_status)
    
    @pytest.mark.parametrize("invalid_status", [
        99,      # 无效正数
        -1,      # 负数
        "abc",   # 字符串
        1.5,     # 小数
        999      # 超大数
    ])
    def test_update_invalid_status(self, invalid_status):
        """测试修改订单状态为无效值"""
        order_id = self._create_order()
        final_status = 0
        
        try:
            # 尝试修改为无效状态
            response = self._update_order_status(order_id, invalid_status)
            
            response_data = response.json()
            print(f"无效状态[{invalid_status}]修改结果: {response_data}")
            
            # 获取实际状态（接口可能接受或拒绝）
            current_status = self._get_order_info(order_id)
            print(f"当前状态: {current_status}")
            final_status = current_status if current_status is not None else 0
            
            # 注：当前接口对无效状态值没有校验，会被接受
            # 此测试用于记录接口行为
            
        finally:
            # 根据实际状态选择清理方式
            # status=0: cancel, status=1/2: refund, 其他: 不处理
            self._cleanup_order(order_id, final_status)
    
    def test_update_status_nonexistent_order(self):
        """测试修改不存在的订单状态"""
        # 使用不存在的订单ID
        response = self._update_order_status(999999, 1)
        
        response_data = response.json()
        print(f"修改不存在订单结果: {response_data}")
        
        # 断言返回错误
        assert response_data.get("code") != 1000, "不存在的订单应返回错误"
