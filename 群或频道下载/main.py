import tkinter as tk
from tkinter import messagebox
from ui_main import build_main_ui
from command_builder import build_command
from validators import (
    validate_json_path,
    validate_threads_and_parallel,
)
from utils import copy_to_clipboard, clear_all_inputs


def on_generate_command(ui):
    """
    收集 UI 的所有字段，生成命令并显示在输出框
    """
    # 1) 基础字段
    json_path = ui["json_path_var"].get().strip()
    out_dir = ui["dir_var"].get().strip()

    # 2) 并发参数（只有勾选时才读取数值）
    threads = ui["enable_threads_var"].get() and ui["threads_var"].get().strip() or ""
    parallel = ui["enable_parallel_var"].get() and ui["parallel_var"].get().strip() or ""

    # 3) 功能开关
    opts = {
        "desc": ui["desc_var"].get(),
        "rewrite": ui["rewrite_var"].get(),
        "group": ui["group_var"].get(),
        "skip_same": ui["skip_var"].get(),
        "takeout": ui["takeout_var"].get(),
    }

    # 4) 模板
    use_template = ui["use_template_var"].get()
    template_str = ui["template_var"].get().strip() if use_template else ""

    # ---------- 校验 ----------
    ok, err = validate_json_path(json_path)
    if not ok:
        messagebox.showerror("错误", err)
        return

    ok, err = validate_threads_and_parallel(
        ui["enable_threads_var"].get(), threads,
        ui["enable_parallel_var"].get(), parallel
    )
    if not ok:
        messagebox.showerror("错误", err)
        return

    # 若启用了模板但没点“生成当前模板”，自动给一个默认模板，避免“空模板”报警
    if use_template and not template_str:
        template_str = "{{ filenamify .FileCaption 64 }}_{{ formatDate .DownloadDate `2006-01-02-15-04-05` }}_{{ filenamify .FileName }}"

    cmd = build_command(
        json_path=json_path,
        out_dir=out_dir,
        threads=threads,
        parallel=parallel,
        opts=opts,
        template=template_str
    )

    ui["output_text"].delete("1.0", "end")
    ui["output_text"].insert("1.0", cmd)


def run_app():
    root = tk.Tk()
    root.title("TDL 命令生成器（导入 JSON 下载）")
    root.geometry("1760x730")
    root.minsize(980, 650)

    # Windows 上更稳的缺省字体
    root.option_add("*Font", ("Microsoft YaHei UI", 10))

    ui = build_main_ui(root, on_generate_command)

    # 顶部按钮回调接入
    ui["btn_copy"].configure(command=lambda: copy_to_clipboard(root, ui["output_text"]))
    ui["btn_clear"].configure(command=lambda: clear_all_inputs(ui))

    root.mainloop()


if __name__ == "__main__":
    try:
        run_app()
    except Exception as e:
        import traceback
        print("程序发生异常：", e)
        print(traceback.format_exc())
        input("\n按 Enter 退出...")