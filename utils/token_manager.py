"""Token 管理器"""
import time
import requests
import yaml
from pathlib import Path


class TokenManager:
    """管理 JWT Token 的获取和自动刷新"""
    
    def __init__(self):
        config_path = Path(__file__).parent.parent / "config" / "settings.yaml"
        with open(config_path, "r", encoding="utf-8") as f:
            self.config = yaml.safe_load(f)
        
        self.base_url = self.config["base_url"]
        self.phone = self.config["test_account"]["phone"]
        self.password = self.config["test_account"]["password"]
        self.refresh_before = self.config["token"]["refresh_before_expire"]
        
        self.token = None
        self.refresh_token = None
        self.expire_time = 0
        self.refresh_expire_time = 0
    
    def _login(self):
        """执行登录获取新 Token"""
        url = f"{self.base_url}/app/user/login/password"
        payload = {
            "phone": self.phone,
            "password": self.password
        }
        
        response = requests.post(url, json=payload, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        if data.get("code") != 1000:
            raise Exception(f"登录失败: {data.get('message')}")
        
        token_data = data["data"]
        self.token = token_data["token"]
        self.refresh_token = token_data["refreshToken"]
        
        # 计算过期时间（当前时间 + 有效期）
        current_time = time.time()
        self.expire_time = current_time + token_data["expire"]
        self.refresh_expire_time = current_time + token_data["refreshExpire"]
        
        return self.token
    
    def _refresh(self):
        """使用 refresh_token 刷新 Token"""
        url = f"{self.base_url}/app/user/login/refreshToken"
        payload = {
            "refreshToken": self.refresh_token
        }
        
        response = requests.post(url, json=payload, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        if data.get("code") != 1000:
            # 刷新失败，重新登录
            return self._login()
        
        token_data = data["data"]
        self.token = token_data["token"]
        self.refresh_token = token_data["refreshToken"]
        
        current_time = time.time()
        self.expire_time = current_time + token_data["expire"]
        self.refresh_expire_time = current_time + token_data["refreshExpire"]
        
        return self.token
    
    def get_token(self):
        """获取有效 Token（自动处理刷新）"""
        current_time = time.time()
        
        # 如果没有 Token，先登录
        if not self.token:
            return self._login()
        
        # 如果 Token 即将过期，尝试刷新
        if current_time >= (self.expire_time - self.refresh_before):
            # 检查 refresh_token 是否也过期了
            if current_time >= (self.refresh_expire_time - self.refresh_before):
                # refresh_token 也过期了，重新登录
                return self._login()
            else:
                # 刷新 Token
                return self._refresh()
        
        return self.token
    
    def get_auth_header(self):
        """获取带 Authorization 的请求头"""
        token = self.get_token()
        return {
            "Authorization": token,
            "Content-Type": "application/json",
            "Accept": "application/json"
        }


# 全局 TokenManager 实例（单例）
_token_manager = None


def get_token_manager():
    """获取 TokenManager 单例"""
    global _token_manager
    if _token_manager is None:
        _token_manager = TokenManager()
    return _token_manager
