"""miniqa 用例示例：同时演示「类式」与「函数式」两种写法。"""
from miniqa import TestCase, test, assert_equal, assert_raises, assert_almost_equal
from sample.app.calculator import Calculator


class TestCalculator(TestCase):
    def setup(self):
        self.calc = Calculator()

    def test_add(self):
        assert_equal(self.calc.add(2, 3), 5)

    def test_subtract(self):
        assert_equal(self.calc.subtract(10, 4), 6)

    def test_divide_by_zero(self):
        # 异常断言：期望 divide(1, 0) 抛出 ValueError
        assert_raises(ValueError, self.calc.divide, 1, 0)

    def test_sqrt_negative(self):
        with assert_raises(ValueError):
            self.calc.sqrt(-1)


@test
def test_multiply():
    c = Calculator()
    assert_equal(c.multiply(4, 5), 20)


@test
def test_float_precision():
    c = Calculator()
    # 浮点比较用 assert_almost_equal，避免精度误差导致误判
    assert_almost_equal(c.divide(1, 3), 0.3333333, places=5)
