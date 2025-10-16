# command_builder.py
import re
from tkinter import messagebox

def _ensure_safe_template(template: str | None) -> str:
    """
    兜底增强模板：
      1) .FileCaption/.FileName/.ChatTitle/.SenderID -> {{ filenamify .Field }}
      2) {{ .DownloadDate }} -> {{ formatDate .DownloadDate `2006-01-02-15-04-05` }}
      3) 若 template 为空，给出安全默认
    不修改用户已写好的函数（如已存在 filenamify/formatDate/replace 等则不动）。
    """
    if not template or not template.strip():
        return "{{ .DialogID }}_{{ .MessageID }}_{{ filenamify .FileName }}"

    tpl = template.strip()

    # 1) 字符串类字段自动 filenamify（仅在没包过的情况下）
    string_fields = [".FileCaption", ".FileName", ".ChatTitle", ".SenderID"]
    for field in string_fields:
        # {{  .Field  }}
        pat_plain = re.compile(r"{{\s*" + re.escape(field) + r"\s*}}")
        # 已被 filenamify 的不处理
        if pat_plain.search(tpl):
            # 但要避免把 {{ filenamify .Field }} 又替换；先检查是否已在 filenamify 中
            pat_wrapped = re.compile(r"{{\s*filenamify\s+" + re.escape(field) + r"(?:\s+\d+)?\s*}}")
            if not pat_wrapped.search(tpl):
                tpl = pat_plain.sub(lambda m: "{{ filenamify " + field + " }}", tpl)

    # 2) 时间字段：把 {{ .DownloadDate }} 升级为 formatDate（如已手写 formatDate 则不动）
    pat_date_plain = re.compile(r"{{\s*\.DownloadDate\s*}}")
    pat_date_has_format = re.compile(r"{{\s*formatDate\s+\.DownloadDate\b")
    if pat_date_plain.search(tpl) and not pat_date_has_format.search(tpl):
        tpl = pat_date_plain.sub("{{ formatDate .DownloadDate `2006-01-02-15-04-05` }}", tpl)

    return tpl


def build_tdl_command(
    urls,
    dir_path=None,
    threads=None,
    parallel=None,
    desc=False,
    rewrite=False,
    group=False,
    skip=False,
    takeout=False,
    template=None
):
    """
    构建完整 tdl 命令（已移除 -i/-e；自动兜底模板安全化）
    """
    # 1) 验证链接
    if not urls or not any(u.strip() for u in urls):
        messagebox.showerror("错误", "请至少输入一条 Telegram 链接！")
        return ""

    # 2) 链接参数
    url_args = " ".join(f"-u {u.strip()}" for u in urls if u.strip())

    # 3) 目录、线程、并发
    dir_arg = f"-d \"{dir_path.strip()}\"" if dir_path else ""
    thread_arg = f"-t {threads.strip()}" if threads else ""
    parallel_arg = f"-l {parallel.strip()}" if parallel else ""

    # 4) 功能开关
    switches = []
    if desc: switches.append("--desc")
    if rewrite: switches.append("--rewrite-ext")
    if group: switches.append("--group")
    if skip: switches.append("--skip-same")
    if takeout: switches.append("--takeout")

    # 5) 模板参数（自动做安全兜底）
    template_arg = ""
    safe_tpl = _ensure_safe_template(template)
    if safe_tpl:
        # 统一加单引号包裹，防止空格/特殊字符
        template_arg = f"--template '{safe_tpl}'"

    # 6) 组装命令
    parts = ["tdl", "dl", url_args]
    if dir_arg: parts.append(dir_arg)
    if thread_arg: parts.append(thread_arg)
    if parallel_arg: parts.append(parallel_arg)
    parts.extend(switches)
    if template_arg: parts.append(template_arg)

    command = " ".join(p for p in parts if p).strip()

    # 7) 简单校验
    if not command.startswith("tdl dl"):
        messagebox.showerror("错误", "命令生成失败，请检查输入内容。")
        return ""

    return command


# 可选：本地测试
if __name__ == "__main__":
    cmd = build_tdl_command(
        urls=[
            "https://t.me/c/1697050800/10879",
            "https://t.me/c/1398577452/10886",
            "https://t.me/c/1697050800/17616",
        ],
        dir_path="D:/Download",
        threads="8",
        parallel="3",
        desc=True,
        rewrite=True,
        group=False,
        skip=True,
        takeout=False,
        # 故意给原始模板，看看是否被兜底成安全模板
        template="{{ .FileCaption }}_{{ .DownloadDate }}_{{ .FileName }}"
    )
    print(cmd)