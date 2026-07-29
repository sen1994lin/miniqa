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

    out = [
        "from miniqa import test, assert_equal, assert_raises",
        "",
        "",
    ]
    found = 0
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
    if found == 0:
        out.append("# 未在该文件中发现顶层函数，可手动为类方法补充 TestCase。")
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
