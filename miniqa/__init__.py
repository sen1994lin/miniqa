"""miniqa —— 零依赖的轻量 Python 自动化测试框架。

特性：
- 类式（TestCase）与函数式（@test）两种用例写法
- 内置常用断言 + 异常断言
- 自动发现 test_*.py，支持 setup / teardown
- 控制台报告 + 自包含 HTML 报告
- 内置测试骨架生成器（基于 AST，无需任何第三方库）
"""
from .core import (
    TestCase,
    test,
    assert_equal,
    assert_true,
    assert_false,
    assert_in,
    assert_almost_equal,
    assert_raises,
)
from .runner import TestRunner, TestResult
from .reporter import ConsoleReporter, HtmlReporter

__version__ = "0.1.0"
__all__ = [
    "TestCase", "test",
    "assert_equal", "assert_true", "assert_false", "assert_in",
    "assert_almost_equal", "assert_raises",
    "TestRunner", "TestResult", "ConsoleReporter", "HtmlReporter",
]
