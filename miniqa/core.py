"""miniqa 核心：断言函数、TestCase 基类、@test 装饰器、异常断言上下文。

所有断言失败统一抛出内置 AssertionError，便于 runner 区分「失败」与「错误」。
"""
import traceback


# ---------- 断言函数 ----------
def assert_equal(actual, expected, msg=None):
    if actual != expected:
        raise AssertionError(msg or f"assert_equal 失败: 实际 {actual!r} != 期望 {expected!r}")


def assert_true(expr, msg=None):
    if not expr:
        raise AssertionError(msg or f"assert_true 失败: {expr!r} 不为真")


def assert_false(expr, msg=None):
    if expr:
        raise AssertionError(msg or f"assert_false 失败: {expr!r} 不为假")


def assert_in(member, container, msg=None):
    if member not in container:
        raise AssertionError(msg or f"assert_in 失败: {member!r} 不在 {container!r} 中")


def assert_almost_equal(actual, expected, places=7, msg=None):
    if round(abs(actual - expected), places) != 0:
        raise AssertionError(
            msg or f"assert_almost_equal 失败: {actual!r} 与 {expected!r} 相差超过 {places} 位小数"
        )


class _RaisesContext:
    """with assert_raises(Exc): ... 的上下文管理器。"""

    def __init__(self, expected):
        self.expected = expected
        self.exc = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, tb):
        if exc_type is None:
            raise AssertionError(f"assert_raises 失败: 期望抛出 {self.expected.__name__}，但未抛出任何异常")
        if not issubclass(exc_type, self.expected):
            raise AssertionError(
                f"assert_raises 失败: 期望抛出 {self.expected.__name__}，实际抛出 {exc_type.__name__}"
            )
        self.exc = exc_val
        return True  # 吞掉被期望的异常


def assert_raises(expected, callable_obj=None, *args, **kwargs):
    """两种用法：
        assert_raises(ValueError, func, arg)          # 直接校验可调用对象
        with assert_raises(ValueError): func(arg)      # 上下文管理器
    """
    if callable_obj is not None:
        try:
            callable_obj(*args, **kwargs)
        except expected:
            return
        except Exception as e:
            raise AssertionError(
                f"assert_raises 失败: 期望 {expected.__name__}，实际 {type(e).__name__}: {e}"
            )
        raise AssertionError(f"assert_raises 失败: 期望 {expected.__name__}，但未抛出任何异常")
    return _RaisesContext(expected)


# ---------- 用例基类 ----------
class TestCase:
    """类式用例：子类里以 test 开头的方法会被自动收集。
    可选重写 setup / teardown 做每个用例的前置与清理。"""

    def setup(self):
        pass

    def teardown(self):
        pass


# ---------- 函数式装饰器 ----------
def test(func):
    """标记一个函数为测试用例：@test def test_xxx(): ..."""
    func.__is_test__ = True
    return func


__all__ = [
    "assert_equal", "assert_true", "assert_false", "assert_in",
    "assert_almost_equal", "assert_raises", "TestCase", "test",
]
