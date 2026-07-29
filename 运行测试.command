#!/bin/bash
# 双击本文件即可运行 miniqa 全部示例用例并打开 HTML 报告。
# 首次运行若被 macOS 拦截，请到「系统设置 → 隐私与安全性」点击「仍要打开」。
cd "$(dirname "$0")"
/Users/houxiaobin/.workbuddy/binaries/python/versions/3.13.12/bin/python3 run.py -d sample/tests --html report.html
echo "测试完成，正在打开报告…"
open report.html
