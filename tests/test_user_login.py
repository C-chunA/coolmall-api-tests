"""用户登录接口测试"""
import pytest
from tests.base_test import BaseAPITest, pytest_generate_tests_base


def pytest_generate_tests(metafunc):
    """动态生成测试函数"""
    pytest_generate_tests_base(metafunc, "user_login.yaml", "test_login_")


@pytest.mark.login
@pytest.mark.smoke
class TestUserLogin(BaseAPITest):
    """用户登录测试类"""
    
    @pytest.mark.smoke
    def test_login_password(self, case):
        """测试密码登录接口"""
        self._run_test(case)
