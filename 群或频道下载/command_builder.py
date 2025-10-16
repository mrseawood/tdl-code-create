def _q(s: str) -> str:
    """Windows 命令行用双引号包裹字符串，并转义内部双引号"""
    if s is None:
        return ""
    return '"' + s.replace('"', '""') + '"'


def build_command(
    json_path: str,
    out_dir: str = "",
    threads: str = "",
    parallel: str = "",
    opts: dict = None,
    template: str = "",
) -> str:
    """
    生成 tdl 命令（以 JSON 导入为输入）
    tdl dl -f <json> [ -d dir ] [ -t N ] [ -l N ] [flags...] [ --template '<tpl>' ]
    """
    opts = opts or {}

    parts = ["tdl", "dl", "-f", _q(json_path)]

    if out_dir:
        parts += ["-d", _q(out_dir)]

    if threads:
        parts += ["-t", threads]

    if parallel:
        parts += ["-l", parallel]

    # flags
    if opts.get("desc"):
        parts.append("--desc")
    if opts.get("rewrite"):
        parts.append("--rewrite-ext")
    if opts.get("group"):
        parts.append("--group")
    if opts.get("skip_same"):
        parts.append("--skip-same")
    if opts.get("takeout"):
        parts.append("--takeout")

    # template（使用单引号包裹，内部包含反引号/花括号可直接透传）
    if template:
        # 避免用户误在外层再套引号，这里统一包上单引号
        tpl = template.strip()
        if (tpl.startswith("'") and tpl.endswith("'")) or (tpl.startswith('"') and tpl.endswith('"')):
            tpl = tpl[1:-1]
        parts += ["--template", f"'{tpl}'"]

    return " ".join(parts)