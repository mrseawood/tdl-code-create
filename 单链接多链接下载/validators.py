# validators.py
def validate_links(links):
    """检查链接格式是否合法"""
    invalid_lines = []
    for idx, link in enumerate(links, start=1):
        if not link.startswith("https://t.me/"):
            invalid_lines.append(idx)
    return invalid_lines