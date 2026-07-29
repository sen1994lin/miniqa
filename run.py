"""一键运行入口：python run.py -d sample/tests --html report.html"""
import sys

from miniqa.cli import main

if __name__ == "__main__":
    sys.exit(main())
