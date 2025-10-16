import os


def validate_json_path(path: str):
    if not path:
        return False, "请先选择 tdl 导出的 JSON 文件路径。"
    if not os.path.exists(path):
        return False, "指定的 JSON 文件不存在。"
    if not path.lower().endswith(".json"):
        return False, "请选择 *.json 文件。"
    return True, ""


def validate_threads_and_parallel(enable_t: bool, t_val: str, enable_l: bool, l_val: str):
    if enable_t:
        if not t_val.isdigit() or int(t_val) <= 0:
            return False, "线程数 (-t) 必须是正整数。"
    if enable_l:
        if not l_val.isdigit() or int(l_val) <= 0:
            return False, "并发数 (-l) 必须是正整数。"
    return True, ""