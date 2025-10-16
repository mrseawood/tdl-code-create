import tkinter as tk
from tkinter import messagebox


def copy_to_clipboard(root, text_widget: tk.Text):
    data = text_widget.get("1.0", "end-1c").strip()
    if not data:
        messagebox.showinfo("提示", "没有可复制的命令。")
        return
    root.clipboard_clear()
    root.clipboard_append(data)
    messagebox.showinfo("已复制", "命令已复制到剪贴板。")


def clear_all_inputs(ui: dict):
    # 基础
    for key in ["json_path_var", "dir_var", "threads_var", "parallel_var"]:
        ui[key].set("")

    # 开关
    for key in ["enable_threads_var", "enable_parallel_var", "desc_var", "rewrite_var",
                "group_var", "skip_var", "takeout_var", "use_template_var"]:
        ui[key].set(False)

    # 模板
    ui["template_var"].set("")

    # 输出
    ui["output_text"].delete("1.0", "end")