#!/usr/bin/env python3
"""
测试运行脚本 - 简化版
"""
import pytest

pytest.main(["tests/", "-v", "--alluredir=reports/allure-results"])
