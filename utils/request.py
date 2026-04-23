"""HTTP 请求封装"""
import requests
import json
import time
from .token_manager import get_token_manager
from .logger import log_request, log_response, log_test_start, log_test_end, log_assertion


class APIRequest:
    """API 请求封装类"""
    
    def __init__(self, base_url=None):
        if base_url is None:
            import yaml
            from pathlib import Path
            config_path = Path(__file__).parent.parent / "config" / "settings.yaml"
            with open(config_path, "r", encoding="utf-8") as f:
                config = yaml.safe_load(f)
            base_url = config["base_url"]
        
        self.base_url = base_url
        self.session = requests.Session()
    
    def _log_request(self, method, url, headers, payload):
        """记录请求信息"""
        log_request(method, url, headers, payload)
    
    def _log_response(self, response):
        """记录响应信息"""
        try:
            resp_data = response.json()
            resp_body = json.dumps(resp_data, ensure_ascii=False)
        except:
            resp_body = response.text
        
        log_response(response.status_code, resp_body)
    
    def request(self, method, endpoint, payload=None, headers=None, use_token=True):
        """
        发送 HTTP 请求
        
        Args:
            method: HTTP 方法 (GET/POST/PUT/DELETE)
            endpoint: 接口路径（不含 base_url）
            payload: 请求体
            headers: 自定义请求头
            use_token: 是否自动添加 Token
        
        Returns:
            Response 对象
        """
        import allure
        
        url = f"{self.base_url}{endpoint}"
        
        # 设置请求头
        if headers is None:
            headers = {}
        
        if use_token:
            token_headers = get_token_manager().get_auth_header()
            headers.update(token_headers)
        else:
            headers.update({
                "Content-Type": "application/json",
                "Accept": "application/json"
            })
        
        # Allure 步骤：记录请求
        with allure.step(f"发送请求: {method} {endpoint}"):
            safe_headers = dict(headers)
            if 'Authorization' in safe_headers:
                safe_headers['Authorization'] = '***'
            allure.attach(json.dumps(safe_headers, ensure_ascii=False), 
                         name="请求头", attachment_type=allure.attachment_type.JSON)
            if payload:
                allure.attach(json.dumps(payload, ensure_ascii=False), 
                             name="请求体", attachment_type=allure.attachment_type.JSON)
        
        # 记录请求到日志
        self._log_request(method, url, headers, payload)
        
        # 发送请求
        response = self.session.request(
            method=method,
            url=url,
            json=payload,
            headers=headers,
            timeout=30
        )
        
        # Allure 步骤：记录响应
        with allure.step(f"接收响应: Status {response.status_code}"):
            try:
                resp_body = response.json()
                allure.attach(json.dumps(resp_body, ensure_ascii=False), 
                             name="响应体", attachment_type=allure.attachment_type.JSON)
            except:
                allure.attach(response.text[:1000], 
                             name="响应体", attachment_type=allure.attachment_type.TEXT)
        
        # 记录响应到日志
        self._log_response(response)
        
        return response
    
    def get(self, endpoint, params=None, **kwargs):
        """GET 请求"""
        return self.request("GET", endpoint, payload=params, **kwargs)
    
    def post(self, endpoint, payload=None, **kwargs):
        """POST 请求"""
        return self.request("POST", endpoint, payload=payload, **kwargs)
    
    def put(self, endpoint, payload=None, **kwargs):
        """PUT 请求"""
        return self.request("PUT", endpoint, payload=payload, **kwargs)
    
    def delete(self, endpoint, **kwargs):
        """DELETE 请求"""
        return self.request("DELETE", endpoint, **kwargs)
