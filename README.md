# CoolMall API 自动化测试框架

## 项目介绍

基于 Python + pytest + requests 的接口自动化测试框架，用于测试 CoolMall 电商 App 的 API 接口。

## 技术栈

- Python 3.8+
- pytest
- requests
- PyYAML
- allure-pytest

## 项目结构

```
coolmall-api-tests/
├── config/                 # 配置
│   ├── settings.yaml       # 环境配置
│   └── constants.py        # 常量
├── api/                    # 接口封装（待扩展）
├── tests/                  # 测试用例
│   ├── test_user_login.py  # 用户登录测试
│   ├── test_user_info.py   # 用户信息测试
│   └── test_user_address.py # 收货地址测试
├── utils/                  # 工具
│   ├── request.py          # 请求封装
│   ├── token_manager.py    # Token 管理
│   └── assertions.py       # 断言封装
├── data/                   # 测试数据
│   ├── user_login.yaml
│   ├── user_info.yaml
│   └── user_address.yaml
├── conftest.py             # pytest 配置
├── pytest.ini              # pytest 配置
├── requirements.txt        # 依赖
└── README.md               # 说明文档
```

## 快速开始

### 1. 安装依赖

```bash
cd coolmall-api-tests
pip install -r requirements.txt
```

### 2. 配置测试账号

编辑 `config/settings.yaml`：

```yaml
test_account:
  phone: "13205562371"
  password: "123456"
```

### 3. 运行测试

```bash
# 运行所有测试
pytest

# 运行指定模块
pytest tests/test_user_login.py

# 运行冒烟测试
pytest -m smoke

# 生成 allure 报告
pytest --alluredir=reports/allure-results
allure serve reports/allure-results
```

## 测试模块

### 用户登录 (test_user_login.py)

- 手机号密码登录成功
- 手机号不存在
- 密码错误
- 手机号为空
- 密码为空

### 用户信息 (test_user_info.py)

- 获取用户信息成功

### 收货地址 (test_user_address.py)

- 添加收货地址成功
- 添加地址-缺少联系人
- 查询收货地址列表
- 更新收货地址
- 删除收货地址

## 核心特性

1. **Token 自动管理**：登录一次，自动刷新，无需手动处理
2. **数据驱动**：测试数据存储在 YAML 文件，易于维护
3. **自动清理**：测试产生的数据自动删除，保持环境干净
4. **详细日志**：请求/响应详情自动打印，便于调试
5. **Allure 报告**：美观的测试报告，支持图表和趋势分析

## 配置说明

### settings.yaml

```yaml
base_url: "https://mall.dusksnow.top"  # API 基础地址
test_account:                          # 测试账号
  phone: "13205562371"
  password: "123456"
log:
  level: "DEBUG"                       # 日志级别
  print_request: true                  # 打印请求
  print_response: true                 # 打印响应
token:
  refresh_before_expire: 300           # Token 提前刷新时间（秒）
```

## 扩展指南

### 添加新测试模块

1. 在 `data/` 下创建 YAML 测试数据文件
2. 在 `tests/` 下创建测试类
3. 参考现有测试编写用例

### 添加新接口

1. 在 `utils/request.py` 中添加请求方法（如需要）
2. 在测试类中调用 `api_client.request()` 发送请求
3. 使用 `assertions.py` 中的方法进行断言

## 注意事项

- 测试账号需要提前在系统中注册
- 测试数据会自动清理，但建议不要在生产环境运行
- Token 有效期为 30 天，refresh_token 有效期为 90 天

## 重要规则

### 接口测试代码必须严格对齐接口文档

**核心原则**：所有测试代码必须根据接口文档编写，不能凭经验猜测。

**必须对齐的项：**

| 对齐项 | 说明 | 示例 |
|--------|------|------|
| 请求路径 | 必须和文档完全一致 | `/app/user/info/person` 不是 `/app/user/info` |
| 请求方法 | GET/POST/PUT/DELETE 必须一致 | 文档是 POST 就不能用 GET |
| 字段名称 | 必须和文档字段名一致 | 文档是 `phone` 就不能用 `account` |
| 字段类型 | string/number/boolean/array 必须匹配 | |
| 必填字段 | required 列表里的字段必须传 | |
| 响应结构 | 断言字段路径必须匹配实际返回 | `data.pagination.total` 不是 `data.total` |

**工作流程：**
1. 先读接口文档，提取关键信息（路径、方法、字段、响应）
2. 写测试代码时逐条核对文档
3. 不确定的字段名、路径，查文档确认
4. 跑不通时优先怀疑代码，不是接口

**常见错误：**
- ❌ 凭经验用 `account` 代替 `phone`
- ❌ 凭经验用 `id` 代替 `ids`
- ❌ 凭经验猜测接口路径
- ❌ 不验证响应字段路径

## 更新日志

- 2026-04-20: 初始化项目，完成用户登录、用户信息、收货地址三个模块
- 2026-04-20: 添加接口文档对齐规则，修复字段名不一致问题
