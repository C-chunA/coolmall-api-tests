"""用户信息接口测试"""
import pytest
from tests.base_test import BaseAPITest, pytest_generate_tests_base


def pytest_generate_tests(metafunc):
    """动态生成测试函数"""
    pytest_generate_tests_base(metafunc, "user_info.yaml", "test_user_info_")


@pytest.mark.user
class TestUserInfo(BaseAPITest):
    """用户信息测试类"""
    
    @pytest.mark.smoke
    def test_user_info_person(self, case):
        """测试获取用户个人信息接口"""
        self._run_test(case)
