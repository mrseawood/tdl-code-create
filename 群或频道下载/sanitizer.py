import re

# 目前模板交给 tdl 的内置函数 filenamify 处理。
# 这里保留一个备用“客户端侧”清理函数（未直接使用）。
INVALID_WIN = re.compile(r'[\\/:*?"<>|\r\n]+')

def sanitize_filename(name: str, replacement: str = "_", max_len: int = 180) -> str:
    name = INVALID_WIN.sub(replacement, name)
    name = name.strip(" .")
    if not name:
        name = "file"
    if len(name) > max_len:
        name = name[:max_len].rstrip()
    return name