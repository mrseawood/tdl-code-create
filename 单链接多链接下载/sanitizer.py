# sanitizer.py
import re
import unicodedata

def sanitize_filename(name: str) -> str:
    """
    清理 Windows 文件名非法字符和 emoji。
    仅用于目录或非模板路径，不处理模板（模板由 filenamify 控制）。
    """
    if not name:
        return "output"

    # 去掉控制字符和 emoji
    name = ''.join(ch for ch in name if unicodedata.category(ch)[0] != 'C' and not unicodedata.category(ch).startswith('So'))

    # 替换非法符号
    name = re.sub(r'[<>:"/\\|?*]', '_', name)

    # 去掉末尾空格和点
    name = name.strip().rstrip('.')

    # 限制最大长度
    if len(name) > 240:
        name = name[:240]

    return name