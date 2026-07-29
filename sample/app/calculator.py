"""被测对象（SUT）：一个极简计算器，仅用于演示 miniqa 的测试能力。"""


class Calculator:
    def add(self, a, b):
        return a + b

    def subtract(self, a, b):
        return a - b

    def multiply(self, a, b):
        return a * b

    def divide(self, a, b):
        if b == 0:
            raise ValueError("除数不能为 0")
        return a / b

    def sqrt(self, x):
        if x < 0:
            raise ValueError("不能对负数开平方")
        return x ** 0.5
