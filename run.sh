#!/bin/bash
# 运行测试并生成报告

PORT=8889

echo "========================================"
echo "开始运行接口自动化测试"
echo "========================================"

# 运行测试
python3 -m pytest tests/ -v --alluredir=reports/allure-results

echo ""
echo "========================================"
echo "测试执行完成"
echo "========================================"

# 生成报告
echo ""
echo "正在生成 Allure 报告..."
allure generate reports/allure-results -o reports/allure-report --clean

# 检查端口是否被占用
echo ""
echo "检查端口 ${PORT} 是否被占用..."
PID=$(lsof -t -i:${PORT} 2>/dev/null)

if [ -n "$PID" ]; then
    echo "端口 ${PORT} 被进程 ${PID} 占用，正在终止..."
    kill -9 ${PID} 2>/dev/null
    sleep 1
    echo "进程已终止"
fi

# 启动报告服务
echo ""
echo "正在启动 Allure 报告服务..."
echo "报告地址: http://111.229.39.148:${PORT}"
echo "按 Ctrl+C 停止服务"
echo ""

allure open reports/allure-report -h 0.0.0.0 -p ${PORT}
