#!/usr/bin/env python3
"""
测试运行脚本
运行测试并自动启动 Allure 报告服务
"""
import subprocess
import sys
import time
import webbrowser
import os
import signal
from pathlib import Path


def kill_allure_server(port=8889):
    """杀掉占用指定端口的 Allure 进程"""
    try:
        # 查找占用端口的进程
        result = subprocess.run(
            ["lsof", "-t", "-i", f":{port}"],
            capture_output=True,
            text=True
        )
        if result.stdout:
            pids = result.stdout.strip().split('\n')
            for pid in pids:
                if pid:
                    print(f"发现占用端口 {port} 的进程: {pid}，正在终止...")
                    os.kill(int(pid), signal.SIGTERM)
                    time.sleep(1)
    except Exception as e:
        print(f"终止进程时出错: {e}")


def run_tests():
    """运行测试并生成 Allure 报告"""
    print("=" * 60)
    print("开始运行接口自动化测试")
    print("=" * 60)
    
    # 运行 pytest 测试
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "tests/", "-v", "--alluredir=reports/allure-results"],
        cwd=Path(__file__).parent
    )
    
    print("\n" + "=" * 60)
    print("测试执行完成")
    print("=" * 60)
    
    # 生成静态报告
    print("\n正在生成 Allure 报告...")
    subprocess.run(
        ["allure", "generate", "reports/allure-results", "-o", "allure-report", "--clean"],
        cwd=Path(__file__).parent,
        check=False
    )
    
    # 启动 Allure 服务
    print("\n正在启动 Allure 报告服务...")
    
    # 先杀掉可能占用端口的旧进程
    kill_allure_server(8889)
    
    print("报告地址: http://111.229.39.148:8889")
    print("按 Ctrl+C 停止服务\n")
    
    try:
        # 启动 allure open（使用静态报告，端口8889）
        subprocess.run(
            ["allure", "open", "allure-report", "-h", "0.0.0.0", "-p", "8889"],
            cwd=Path(__file__).parent
        )
    except KeyboardInterrupt:
        print("\n服务已停止")
    except FileNotFoundError:
        print("\n错误: 未找到 allure 命令")
        print("请先安装 Allure: https://docs.qameta.io/allure/")
        print("或使用以下命令查看报告:")
        print("  allure serve reports/allure-results")


if __name__ == "__main__":
    run_tests()
