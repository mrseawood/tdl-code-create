# main.py
import tkinter as tk
from tkinter import messagebox
from command_builder import build_tdl_command
from ui_main import build_main_ui


def on_generate_command(ui):
    """生成命令回调"""
    try:
        urls_raw = ui["urls_var"].get()
        urls = [u.strip() for u in urls_raw.splitlines() if u.strip()]

        dir_path = ui["dir_var"].get().strip()
        threads = ui["threads_var"].get().strip()
        parallel = ui["parallel_var"].get().strip()

        desc = ui["desc_var"].get()
        rewrite = ui["rewrite_var"].get()
        group = ui["group_var"].get()
        skip = ui["skip_var"].get()
        takeout = ui["takeout_var"].get()

        # ✅ 删除 include/exclude 调用
        # include_exts = ui["include_var"].get()
        # exclude_exts = ui["exclude_var"].get()

        # 模板命名
        template = ui["template_var"].get().strip() if ui["use_custom_template"].get() else ""

        # 构建命令（不再传入 include/exclude）
        command = build_tdl_command(
            urls=urls,
            dir_path=dir_path,
            threads=threads,
            parallel=parallel,
            desc=desc,
            rewrite=rewrite,
            group=group,
            skip=skip,
            takeout=takeout,
            template=template
        )

        ui["output_var"].set(command)

    except Exception as e:
        messagebox.showerror("命令生成错误", str(e))


def run_app():
    root = tk.Tk()
    root.title("TDL 命令生成器")
    root.geometry("950x700")

    ui = build_main_ui(root, on_generate_command)
    root.mainloop()


if __name__ == "__main__":
    run_app()