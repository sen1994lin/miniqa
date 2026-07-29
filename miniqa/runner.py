"""miniqa 运行器：发现 test_*.py、收集用例、执行并收集结果。"""
import importlib.util
import inspect
import time
import traceback
from pathlib import Path


class TestResult:
    def __init__(self, name, status, duration=0.0, message="", trace=""):
        self.name = name
        self.status = status      # "passed" | "failed" | "error"
        self.duration = duration  # 秒
        self.message = message
        self.trace = trace

    def __repr__(self):
        return f"<TestResult {self.name} {self.status}>"


class TestRunner:
    def __init__(self, pattern="test_*.py"):
        self.pattern = pattern
        self.results = []

    # ---------- 发现 ----------
    def discover(self, root):
        return sorted(Path(root).rglob(self.pattern), key=lambda p: str(p))

    def _load_module(self, path):
        module_name = f"_miniqa_{path.stem}"
        spec = importlib.util.spec_from_file_location(module_name, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    # ---------- 执行 ----------
    def run(self, root):
        self.results = []
        for path in self.discover(root):
            try:
                module = self._load_module(path)
            except Exception as e:  # 模块导入失败也算一个错误用例
                self.results.append(
                    TestResult(str(path), "error", 0.0,
                               f"模块导入失败: {type(e).__name__}: {e}",
                               traceback.format_exc())
                )
                continue
            self._run_module(module, path)
        return self.results

    def _run_module(self, module, path):
        setup_module = getattr(module, "setup_module", None)
        teardown_module = getattr(module, "teardown_module", None)
        try:
            if setup_module:
                setup_module()
            # 类式用例
            for _name, obj in inspect.getmembers(module, inspect.isclass):
                if issubclass(obj, TestCase) and obj is not TestCase:
                    self._run_testcase(obj, path)
            # 函数式用例
            for _name, obj in inspect.getmembers(module, inspect.isfunction):
                if getattr(obj, "__is_test__", False):
                    self._run_function_test(obj, path)
        finally:
            if teardown_module:
                try:
                    teardown_module()
                except Exception:
                    pass

    def _run_testcase(self, cls, path):
        for name in dir(cls):
            if name.startswith("test"):
                case = cls()
                method = getattr(case, name, None)  # 绑定到实例，避免缺 self
                if callable(method):
                    self._execute(
                        f"{path.stem}.{cls.__name__}.{name}",
                        case.setup, method, case.teardown,
                    )

    def _run_function_test(self, func, path):
        self._execute(f"{path.stem}.{func.__name__}", None, func, None)

    def _execute(self, name, setup, target, teardown):
        start = time.perf_counter()
        status, message, tb = "passed", "", ""
        try:
            if setup:
                setup()
            target()
        except AssertionError as e:        # 断言失败 = 用例失败
            status, message, tb = "failed", str(e), traceback.format_exc()
        except Exception as e:             # 其它异常 = 用例错误
            status, message, tb = "error", f"{type(e).__name__}: {e}", traceback.format_exc()
        finally:
            duration = time.perf_counter() - start
            if teardown:
                try:
                    teardown()
                except Exception:
                    pass
            self.results.append(TestResult(name, status, duration, message, tb))


# 供 core 反向引用，避免循环导入问题
from .core import TestCase  # noqa: E402
