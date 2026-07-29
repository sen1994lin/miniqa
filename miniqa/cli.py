"""miniqa 命令行入口：python -m miniqa.cli -d <目录> [--html report.html]"""
import argparse
import sys

from .runner import TestRunner
from .reporter import ConsoleReporter, HtmlReporter


def main(argv=None):
    p = argparse.ArgumentParser(prog="miniqa", description="轻量 Python 自动化测试框架")
    p.add_argument("-d", "--dir", default=".", help="测试目录（默认当前目录）")
    p.add_argument("-p", "--pattern", default="test_*.py", help="用例文件匹配模式")
    p.add_argument("--html", default=None, help="输出 HTML 报告的文件路径")
    p.add_argument("-v", "--verbose", action="store_true", help="显示每个用例耗时")
    args = p.parse_args(argv)

    runner = TestRunner(pattern=args.pattern)
    results = runner.run(args.dir)
    print(ConsoleReporter(results).render())

    if args.html:
        HtmlReporter(results).write(args.html)
        print(f"\nHTML 报告已生成: {args.html}")

    failed = [r for r in results if r.status != "passed"]
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
