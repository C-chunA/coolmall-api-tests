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

### 5. 查看报告

- **Allure 在线报告**：http://111.229.39.148:8889
- **PDF 测试报告**：[点击查看](https://github.com/C-chunA/coolmall-api-tests/blob/master/reports/测试报告_20260511.pdf)
- **HTML 测试报告**：[点击查看](https://github.com/C-chunA/coolmall-api-tests/blob/master/reports/测试报告_20260511.html)

## 测试模块

### 用户登录 (test_user_login.py) - 10用例

| 用例 | 状态 |
|------|------|
| 手机号密码登录成功 | ✅ 通过 |
| 手机号不存在 | ❌ 失败（接口缺陷） |
| 密码错误 | ❌ 失败（接口缺陷） |
| 手机号为空 | ❌ 失败（接口缺陷） |
| 密码为空 | ❌ 失败（接口缺陷） |
| phone为null | ❌ 失败（接口缺陷） |
| password为null | ❌ 失败（接口缺陷） |
| 缺少phone字段 | ❌ 失败（接口缺陷） |
| 缺少password字段 | ❌ 失败（接口缺陷） |

### 用户信息 (test_user_info.py) - 4用例

| 用例 | 状态 |
|------|------|
| 获取用户信息成功 | ✅ 通过 |
| 无Token访问 | ❌ 失败（接口缺陷） |
| Token格式错误 | ❌ 失败（接口缺陷） |
| Token过期 | ❌ 失败（接口缺陷） |

### 收货地址 (test_user_address.py) - 19用例

- ✅ 添加收货地址成功
- ❌ 参数校验缺陷（11个用例）- 必填字段为空/null时仍可创建
- ✅ 查询收货地址列表
- ✅ 更新收货地址
- ✅ 删除收货地址

### 订单管理 (test_user_order.py) - 15用例

- ✅ 创建订单成功
- ❌ 商品数量为负数仍可创建（接口缺陷）
- ✅ 查询订单列表
- ✅ 查询订单详情
- ✅ 取消订单
- ❌ 订单统计接口响应不符
- ❌ 确认收货提示文案不符

### 订单流程 (test_user_order_flow.py) - 8用例

- ✅ 完整订单流程测试（创建→查询→取消）
- ✅ 数据自动清理

### 订单状态流转 (test_order_status_flow.py) - 10用例

- ✅ 正常状态流转（0→1→2→3）
- ✅ 跨状态修改测试
- ✅ 无效状态参数测试
- ❌ 部分状态流转异常

### 商品评价 (test_goods_comment.py) - 34用例

- ✅ 正常评价提交
- ❌ 评分值校验缺失（starCount=0,6,-1均可提交）
- ✅ 评价列表查询
- ✅ 评价详情查询

## 测试结果

### 最新执行统计（2026-05-11）

| 指标 | 数值 |
|------|------|
| **总用例数** | 100 |
| **通过** | 69 ✅ |
| **失败** | 31 ❌ |
| **通过率** | **69%** |
| **执行时间** | 17.65 秒 |

### 各模块通过率

| 模块 | 用例数 | 通过 | 失败 | 通过率 |
|------|--------|------|------|--------|
| 用户登录 | 10 | 2 | 8 | 20% |
| 用户信息 | 4 | 1 | 3 | 25% |
| 收货地址 | 19 | 8 | 11 | 42% |
| 订单管理 | 15 | 12 | 3 | 80% |
| 订单流程 | 8 | 8 | 0 | 100% |
| 订单状态流转 | 10 | 8 | 2 | 80% |
| 商品评价 | 34 | 30 | 4 | 88% |

### 📊 查看完整报告

- **[PDF 测试报告](https://github.com/C-chunA/coolmall-api-tests/blob/master/reports/测试报告_20260511.pdf)** - 包含详细缺陷分析
- **[HTML 测试报告](https://github.com/C-chunA/coolmall-api-tests/blob/master/reports/测试报告_20260511.html)** - 可在线浏览
- **[Allure 可视化报告](http://111.229.39.148:8889)** - 实时查看

## 接口缺陷发现

### 🔴 严重缺陷（需立即修复）

| 缺陷 | 影响 | 详情 |
|------|------|------|
| 登录接口异常处理缺失 | 安全隐患 | 用户不存在/密码错误返回 code=1000 并返回 token |
| 收货地址参数校验缺失 | 数据完整性 | 必填字段为空/null时仍可创建成功 |
| 订单数量校验缺失 | 业务逻辑 | 商品数量为负数时仍能创建订单 |
| 评价评分校验缺失 | 数据有效性 | starCount 为 0/6/-1 时未返回错误 |

### 🟡 一般缺陷

| 缺陷 | 详情 |
|------|------|
| 订单统计接口 | 传入无效 code 参数返回 code=1001，与文档不符 |
| 确认收货提示 | 错误提示为"非法操作"，应为"订单状态不允许确认收货" |

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

- **2026-05-11**: 完成 7 个模块测试（100用例），通过率 69%，生成完整测试报告
- **2026-04-29**: 完成订单状态流转测试用例（10个）
- **2026-04-24**: 完成商品评价模块测试（34用例）
- **2026-04-23**: 完成订单模块测试（15用例），创建 GitHub 仓库
- **2026-04-22**: 添加测试用例设计方法文档
- **2026-04-20**: 初始化项目，完成用户登录、用户信息、收货地址三个模块

## 相关链接

- 📱 **安卓项目**: [CoolMallKotlin](https://github.com/Joker-x-dev/CoolMallKotlin.git) by [Joker-x-dev](https://github.com/Joker-x-dev)
- 📋 **接口文档**: https://coolmall.apifox.cn/
- 🧪 **测试仓库**: https://github.com/C-chunA/coolmall-api-tests
- 📊 **在线报告**: http://111.229.39.148:8889

## 许可证

MIT License
