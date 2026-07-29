# miniqa · 轻量 Python 自动化测试框架

> 一个**零依赖**、可独立运行的测试框架，作为个人作品集，
> 用于展示「会用 AI 提效的测试工程师 / 测开」的工程能力。

---

## 为什么写它

2026 年的测试岗位正在"去初级化"：纯手工功能测试被 AI 与自动化平台快速吞掉，
而市场疯抢的是**懂编程、能搭自动化框架、会用 AI 提效**的质量工程人才。
本项目用一个完全自研、不依赖 pytest 的小框架，证明我具备「造工具」而不是「只会用工具」的能力。

## 特性

- ✅ 类式 `TestCase` 与函数式 `@test` 两种用例写法
- ✅ 内置断言：`assert_equal / assert_true / assert_false / assert_in / assert_almost_equal / assert_raises`
- ✅ 自动发现 `test_*.py`，支持 `setup / teardown` 与模块级 `setup_module / teardown_module`
- ✅ 控制台报告 + **自包含 HTML 报告**（无任何第三方依赖）
- ✅ 内置**测试骨架生成器**（`miniqa.gen`，基于 AST，免 API key）
- ✅ 自带 GitHub Actions CI 模板（多版本 Python 矩阵）

## 快速开始

```bash
# 运行示例用例并生成 HTML 报告
python run.py -d sample/tests --html report.html

# 等价命令
python -m miniqa.cli -d sample/tests --html report.html

# 从源码生成测试骨架（零依赖）
python -m miniqa.gen sample/app/calculator.py
```

## 写用例

**类式（适合需要前置/清理的用例）：**

```python
from miniqa import TestCase, assert_equal, assert_raises
from sample.app.calculator import Calculator

class TestCalculator(TestCase):
    def setup(self):
        self.calc = Calculator()

    def test_divide_by_zero(self):
        assert_raises(ValueError, self.calc.divide, 1, 0)
```

**函数式（轻量、直观）：**

```python
from miniqa import test, assert_equal
from sample.app.calculator import Calculator

@test
def test_multiply():
    assert_equal(Calculator().multiply(4, 5), 20)
```

## 项目结构

```
miniqa/
├── miniqa/                 # 框架本体（纯标准库）
│   ├── core.py             # 断言 / TestCase / @test
│   ├── runner.py           # 用例发现与执行
│   ├── reporter.py         # 控制台 + HTML 报告
│   ├── cli.py              # 命令行入口
│   └── gen.py              # AST 测试骨架生成器
├── sample/                 # 示例：被测对象 + 用例
│   ├── app/calculator.py
│   └── tests/test_calculator.py
├── examples/ai_assisted.md # AI 辅助测试工作流
├── run.py                  # 一键运行
├── requirements.txt        # 零依赖
└── .github/workflows/ci.yml
```

## AI 辅助测试

详见 [`examples/ai_assisted.md`](examples/ai_assisted.md)。
核心观点：**AI 生成骨架与穷举用例点，人把关测试策略、业务边界与质量风险**——
这正是传统测试员升级为质量架构师的关键。

## 关于作者

候晓宾（晓宾）· 软件测试工程师。曾于 AI 大模型公司**面壁智能（ModelBest）**从事外包测试。
本项目是其「从功能测试走向质量工程 / 测开」转型的作品集。

## License

MIT
