from utils import quote_for_cmd, show_error

def build_command(chat, topic, reply, output, t_type, t_range,
                  filters_dict, with_content, raw, allmsg):
    """
    构造 tdl chat export 命令（不执行）
    - chat 允许留空（表示收藏夹），留空时不加 -c
    - output 为空时使用默认 tdl-export.json
    - 过滤表达式按 AND 连接
    """
    cmd = "tdl chat export"

    # CHAT：留空 = 收藏夹（不加 -c）
    if chat.strip():
        cmd += f" -c {chat.strip()}"

    # topic / reply
    if topic.strip():
        cmd += f" --topic {topic.strip()}"
    if reply.strip():
        cmd += f" --reply {reply.strip()}"

    # 输出文件
    if output.strip():
        cmd += f' -o "{output.strip()}"'
    else:
        cmd += ' -o "tdl-export.json"'

    # 范围
    if t_type.strip():
        cmd += f" -T {t_type.strip()}"
    if t_range.strip():
        cmd += f" -i {t_range.strip()}"

    # 过滤器
    filters = []
    cst = filters_dict.get("custom", "").strip()
    if cst:
        filters.append(cst)

    msg_contains = filters_dict.get("message", "").strip()
    if msg_contains:
        filters.append(f"Message contains '{msg_contains}'")

    name_contains = filters_dict.get("name", "").strip()
    if name_contains:
        filters.append(f"Media.Name contains '{name_contains}'")

    views = filters_dict.get("views", "").strip()
    if views:
        filters.append(f"Views > {views}")

    forwards = filters_dict.get("forwards", "").strip()
    if forwards:
        filters.append(f"Forwards > {forwards}")

    size_mb = filters_dict.get("size", "").strip()
    if size_mb:
        try:
            float(size_mb)
            filters.append(f"Media.Size > {size_mb}*1024*1024")
        except ValueError:
            show_error("错误", "文件大小必须是数字（单位 MB）")
            return None

    from_id = filters_dict.get("fromid", "").strip()
    if from_id:
        filters.append(f"FromID == {from_id}")

    if filters_dict.get("pinned", False):
        filters.append("Pinned == true")
    if filters_dict.get("silent", False):
        filters.append("Silent == true")
    if filters_dict.get("mentioned", False):
        filters.append("Mentioned == true")

    if filters:
        f_expr = " && ".join(filters)
        cmd += f" -f {quote_for_cmd(f_expr)}"

    # 附加开关
    if with_content:
        cmd += " --with-content"
    if raw:
        cmd += " --raw"
    if allmsg:
        cmd += " --all"

    return cmd