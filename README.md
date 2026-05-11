# CoolMall API 自动化测试框架

> 🙏 **特别感谢** [Joker-x-dev](https://github.com/Joker-x-dev) 提供的 [CoolMallKotlin](https://github.com/Joker-x-dev/CoolMallKotlin.git) 安卓项目及完整的接口文档，没有该项目的支持，本接口自动化测试框架将无法实现。

## 项目介绍

基于 Python + pytest + requests 的接口自动化测试框架，用于测试 CoolMall 电商 App 的 API 接口。

**最新进展 (2026-05-11)**：
- ✅ 已完成 7 个核心模块测试（100个测试用例）
- ✅ 测试通过率 69%，发现 6 个接口缺陷
- ✅ 生成完整测试报告（HTML + PDF）
- ✅ 集成 Allure 可视化报告

## 技术栈

- Python 3.8+
- pytest（测试框架）
- requests（HTTP请求）
- PyYAML（测试数据管理）
- allure-pytest（测试报告）
- pytest-xdist（并行执行）

## 项目结构

```
coolmall-api-tests/
├── config/                      # 配置
│   ├── settings.yaml            # 环境配置
│   └── constants.py             # 常量定义
├── api/                         # 接口封装
│   └── base_api.py              # API基础类
├── tests/                       # 测试用例
│   ├── test_user_login.py       # 用户登录测试（10用例）
│   ├── test_user_info.py        # 用户信息测试（4用例）
│   ├── test_user_address.py     # 收货地址测试（19用例）
│   ├── test_user_order.py       # 订单管理测试（15用例）
│   ├── test_user_order_flow.py  # 订单流程测试（8用例）
│   ├── test_order_status_flow.py # 订单状态流转测试（10用例）
│   └── test_goods_comment.py    # 商品评价测试（34用例）
├── utils/                       # 工具模块
│   ├── request.py               # HTTP请求封装
│   ├── token_manager.py         # Token管理
│   ├── assertions.py            # 断言封装
│   └── logger.py                # 日志工具
├── data/                        # 测试数据（YAML）
│   ├── user_login.yaml
│   ├── user_info.yaml
│   ├── user_address.yaml
│   ├── user_order.yaml
│   ├── order_status_flow.yaml
│   └── goods_comment.yaml
├── reports/                     # 测试报告
│   ├── allure-results/          # Allure原始数据
│   ├── allure-report/           # Allure可视化报告
│   ├── 测试报告_20260511.html    # HTML测试报告
│   └── 测试报告_20260511.pdf     # PDF测试报告
├── conftest.py                  # pytest配置
├── pytest.ini                   # pytest配置
├── requirements.txt             # 依赖清单
└── README.md                    # 说明文档
```

## 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/C-chunA/coolmall-api-tests.git
cd coolmall-api-tests
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置测试环境

编辑 `config/settings.yaml`：

```yaml
base_url: "https://mall.dusksnow.top"
test_account:
  phone: "13205562371"
  password: "123456"
```

### 4. 运行测试

```bash
# 运行所有测试
pytest

# 运行指定模块
pytest tests/test_user_login.py

# 运行指定标记的测试
pytest -m smoke          # 冒烟测试
pytest -m login          # 登录相关
pytest -m order          # 订单相关

# 生成 Allure 报告
pytest --alluredir=reports/allure-results
allure generate reports/allure-results -o reports/allure-report --clean
allure open reports/allure-report
```

### 📊 查看完整报告

- **[PDF 测试报告](https://github.com/C-chunA/coolmall-api-tests/blob/master/reports/测试报告_20260511.pdf)** - 包含详细缺陷分析
- **[HTML 测试报告](https://github.com/C-chunA/coolmall-api-tests/blob/master/reports/测试报告_20260511.html)** - 可在线浏览

## 核心特性

1. **🔄 Token 自动管理** - 登录一次，自动刷新，无需手动处理
2. **📄 数据驱动** - 测试数据存储在 YAML 文件，易于维护和扩展
3. **🧹 自动清理** - 测试产生的数据自动删除，保持环境干净
4. **📝 详细日志** - 请求/响应详情自动打印，便于调试和问题定位
5. **📊 Allure 报告** - 美观的测试报告，支持图表、趋势分析和失败截图
6. **🏷️ 标记分类** - 支持 smoke、login、order 等标记，灵活筛选测试
7. **🔧 参数化测试** - 使用 pytest_generate_tests 动态生成测试用例
8. **📦 模块化设计** - 易于扩展新模块和接口

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

### pytest.ini

```ini
[pytest]
testpaths = tests
python_files = test_*.py
addopts = -v --tb=short --strict-markers --alluredir=reports/allure-results
markers =
    smoke: 冒烟测试（登录、核心流程）
    login: 登录相关
    user: 用户信息相关
    address: 收货地址相关
    order: 订单相关
```

## 扩展指南

### 添加新测试模块

1. 在 `data/` 下创建 YAML 测试数据文件
2. 在 `tests/` 下创建测试类，继承 `BaseTest`
3. 使用 `@pytest.mark` 添加标记
4. 运行测试验证

### 示例

```python
# tests/test_new_module.py
import pytest
from tests.base_test import BaseTest

class TestNewModule(BaseTest):
    @pytest.mark.smoke
    def test_new_feature(self):
        # 测试代码
        pass
```

## 相关链接

- 📱 **安卓项目**: [CoolMallKotlin](https://github.com/Joker-x-dev/CoolMallKotlin.git) by [Joker-x-dev](https://github.com/Joker-x-dev)
- 📋 **接口文档**: https://coolmall.apifox.cn/
- 🧪 **测试仓库**: https://github.com/C-chunA/coolmall-api-tests

## 许可证

MIT License
