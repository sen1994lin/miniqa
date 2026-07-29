"""miniqa 测试骨架生成器：解析目标 .py，用 AST 生成 miniqa 风格的测试骨架。

零依赖、无需 API key。用法：
    python -m miniqa.gen sample/app/calculator.py
    python -m miniqa.gen sample/app/calculator.py -o sample/tests/test_calculator_gen.py
"""
import argparse
import ast
import sys


def generate(path):
    with open(path, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read(), filename=path)

    out = ["from miniqa import TestCase, test, assert_equal, assert_raises", "", ""]
    found = 0

    # 顶层函数 -> @test 函数
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            found += 1
            args = [a.arg for a in node.args.args]
            argstr = ", ".join(args)
            out.append("@test")
            out.append(f"def test_{node.name}():")
            out.append(f"    # result = {node.name}({argstr})")
            out.append(f"    # assert_equal(result, <期望结果>)")
            out.append("")

    # 类 -> TestCase 子类（每个公开方法一个用例）
    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            found += 1
            out.append(f"class Test{node.name}(TestCase):")
            out.append("    def setup(self):")
            out.append("        self.obj = <被测对象的实例化>")
            out.append("")
            for item in node.body:
                if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)) and not item.name.startswith("_"):
                    args = [a.arg for a in item.args.args if a.arg != "self"]
                    argstr = ", ".join(args)
                    out.append(f"    def test_{item.name}(self):")
                    out.append(f"        # result = self.obj.{item.name}({argstr})")
                    out.append(f"        # assert_equal(result, <期望结果>)")
                    out.append("")
            out.append("")

    if found == 0:
        out.append("# 未在该文件中发现可生成的函数或类。")
        out.append("")
    return "\n".join(out)


def main(argv=None):
    p = argparse.ArgumentParser(prog="miniqa-gen", description="从源码生成 miniqa 测试骨架")
    p.add_argument("file", help="目标源码文件路径")
    p.add_argument("-o", "--output", default=None, help="输出文件（默认打印到控制台）")
    args = p.parse_args(argv)

    code = generate(args.file)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(code)
        print(f"已生成测试骨架: {args.output}")
    else:
        print(code)
    return 0


if __name__ == "__main__":
    sys.exit(main())
