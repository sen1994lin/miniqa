"""miniqa 报告：控制台报告 + 自包含 HTML 报告。"""
from .runner import TestResult


class ConsoleReporter:
    MARK = {"passed": "✓", "failed": "✗", "error": "!"}

    def __init__(self, results):
        self.results = results

    def render(self):
        lines = []
        for r in self.results:
            mark = self.MARK.get(r.status, "?")
            lines.append(f"  {mark} {r.name}  ({r.duration * 1000:.1f}ms)")
            if r.status != "passed":
                lines.append(f"      {r.message}")
        passed = sum(1 for r in self.results if r.status == "passed")
        failed = sum(1 for r in self.results if r.status == "failed")
        errored = sum(1 for r in self.results if r.status == "error")
        lines.append("")
        lines.append(
            f"共 {len(self.results)} 个用例 ｜ 通过 {passed} ｜ 失败 {failed} ｜ 错误 {errored}"
        )
        if failed or errored:
            lines.append("")
            lines.append("失败 / 错误详情:")
            for r in self.results:
                if r.status != "passed":
                    lines.append(f"  [{r.status}] {r.name}: {r.message}")
        return "\n".join(lines)


class HtmlReporter:
    def __init__(self, results, title="miniqa 测试报告"):
        self.results = results
        self.title = title

    @staticmethod
    def _esc(s):
        return (s or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    def render(self):
        passed = sum(1 for r in self.results if r.status == "passed")
        failed = sum(1 for r in self.results if r.status == "failed")
        errored = sum(1 for r in self.results if r.status == "error")
        rows = []
        for r in self.results:
            cls = {"passed": "pass", "failed": "fail", "error": "err"}[r.status]
            msg = self._esc(r.message) if r.message else ""
            rows.append(
                f'<tr class="{cls}"><td>{self._esc(r.name)}</td>'
                f'<td>{r.status}</td><td>{r.duration * 1000:.1f}</td>'
                f'<td class="msg">{msg}</td></tr>'
            )
        return f"""<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8">
<title>{self._esc(self.title)}</title>
<style>
 body{{font-family:-apple-system,Segoe UI,Roboto,'PingFang SC',sans-serif;margin:24px;color:#222;}}
 h1{{font-size:20px;}}
 .summary{{margin:12px 0;font-size:14px;}}
 table{{border-collapse:collapse;width:100%;font-size:13px;}}
 th,td{{border:1px solid #e2e2e2;padding:6px 10px;text-align:left;vertical-align:top;}}
 th{{background:#f5f5f5;}}
 tr.pass td:first-child{{color:#1a7f37;}}
 tr.fail td:first-child,tr.err td:first-child{{font-weight:600;}}
 tr.fail td:first-child{{color:#cf222e;}} tr.err td:first-child{{color:#9a6700;}}
 .pass .msg{{color:#666;}} .fail .msg,.err .msg{{color:#cf222e;white-space:pre-wrap;}}
</style></head><body>
<h1>{self._esc(self.title)}</h1>
<div class="summary">共 <b>{len(self.results)}</b> 个用例 ｜ 通过 <b style="color:#1a7f37">{passed}</b> ｜ 失败 <b style="color:#cf222e">{failed}</b> ｜ 错误 <b style="color:#9a6700">{errored}</b></div>
<table><thead><tr><th>用例</th><th>结果</th><th>耗时(ms)</th><th>信息</th></tr></thead>
<tbody>{"".join(rows)}</tbody></table>
</body></html>"""

    def write(self, path):
        with open(path, "w", encoding="utf-8") as f:
            f.write(self.render())
