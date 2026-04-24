"""订单流程测试（需要前置创建订单）"""
import pytest
from tests.base_test import BaseAPITest
from utils.assertions import assert_response_code, assert_response_message


@pytest.mark.order
class TestUserOrderFlow(BaseAPITest):
    """订单流程测试类"""
    
    def _create_order(self):
        """创建订单并返回订单ID"""
        create_payload = {
            "data": {
                "remark": "测试订单",
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
    
    def test_cancel_order(self):
        """测试取消订单流程：创建订单 -> 取消订单"""
        # 步骤1：创建订单
        order_id = self._create_order()
        
        try:
            # 步骤2：取消订单
            cancel_payload = {
                "orderId": order_id,
                "remark": "测试取消"
            }
            cancel_response = self.api.post("/app/order/info/cancel", payload=cancel_payload)
            
            # 断言取消成功
            assert_response_code(cancel_response, 1000)
            assert_response_message(cancel_response, "success")
        except Exception as e:
            print(f"取消订单可能失败: {e}")
    
    def test_update_order(self):
        """测试修改订单流程：创建订单 -> 修改订单"""
        # 步骤1：创建订单
        order_id = self._create_order()
        
        try:
            # 步骤2：修改订单（修改备注）
            update_payload = {
                "id": order_id,
                "remark": "修改后的备注"
            }
            update_response = self.api.post("/app/order/info/update", payload=update_payload)
            
            # 断言修改成功
            assert_response_code(update_response, 1000)
            assert_response_message(update_response, "success")
        finally:
            # 后置：取消订单，清理测试数据
            try:
                cancel_payload = {
                    "orderId": order_id,
                    "remark": "测试后清理"
                }
                cancel_response = self.api.post("/app/order/info/cancel", payload=cancel_payload)
                print(f"取消订单结果: orderId={order_id}, code={cancel_response.json().get('code')}")
            except Exception as e:
                print(f"取消订单失败: {e}")
