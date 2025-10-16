# ui_main.py
import tkinter as tk
from tkinter import ttk, filedialog, messagebox


class TextVar:
    """用于从 Text 控件取值"""
    def __init__(self, widget: tk.Text):
        self.widget = widget
    def get(self):
        return self.widget.get("1.0", "end-1c")


def build_main_ui(root, on_generate_command):
    """
    构建完整 GUI 主界面（左右分布布局）
    """
    ui = {}

    root.option_add("*Font", ("Microsoft YaHei UI", 10))

    # ======= 整体框架：左右分布 =======
    main_frame = ttk.Frame(root)
    main_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # 左侧：参数设置区
    left_frame = ttk.Frame(main_frame)
    left_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))

    # 右侧：命令输出和操作区
    right_frame = ttk.Frame(main_frame)
    right_frame.pack(side="right", fill="both", expand=False)

    style = ttk.Style()
    style.configure("Header.TLabelframe.Label", font=("Microsoft YaHei UI", 10, "bold"))

    # ============ 下载链接输入 ============
    frm_url = ttk.Labelframe(left_frame, text="下载链接输入", style="Header.TLabelframe")
    frm_url.pack(fill="x", pady=5)
    ttk.Label(frm_url, text="支持多条链接（每行一条）：").pack(anchor="w", padx=5, pady=3)
    txt_urls = tk.Text(frm_url, height=5, width=60)
    txt_urls.pack(fill="x", padx=5, pady=5)
    ui["urls_var"] = TextVar(txt_urls)

    # ============ 自定义目录 ============
    frm_dir = ttk.Labelframe(left_frame, text="自定义目录 (-d，可选)", style="Header.TLabelframe")
    frm_dir.pack(fill="x", pady=5)
    ui["dir_var"] = tk.StringVar()
    ttk.Entry(frm_dir, textvariable=ui["dir_var"], width=40).pack(side="left", padx=5, pady=5)
    ttk.Button(frm_dir, text="浏览...", command=lambda: select_dir(ui)).pack(side="left", padx=5)

    # ============ 线程与并发 ============
    frm_threads = ttk.Labelframe(left_frame, text="线程与并发", style="Header.TLabelframe")
    frm_threads.pack(fill="x", pady=5)
    ui["threads_var"], ui["parallel_var"] = tk.StringVar(), tk.StringVar()
    ttk.Label(frm_threads, text="线程数 (-t)：").pack(side="left", padx=5)
    ttk.Entry(frm_threads, textvariable=ui["threads_var"], width=6).pack(side="left")
    ttk.Label(frm_threads, text="并发数 (-l)：").pack(side="left", padx=10)
    ttk.Entry(frm_threads, textvariable=ui["parallel_var"], width=6).pack(side="left")

    # ============ 功能选项 ============
    frm_opts = ttk.Labelframe(left_frame, text="功能选项", style="Header.TLabelframe")
    frm_opts.pack(fill="x", pady=5)
    for key in ["desc_var", "rewrite_var", "group_var", "skip_var", "takeout_var"]:
        ui[key] = tk.BooleanVar()
    ttk.Checkbutton(frm_opts, text="反序下载 (--desc)", variable=ui["desc_var"]).pack(anchor="w", padx=5)
    ttk.Checkbutton(frm_opts, text="MIME 探测 (--rewrite-ext)", variable=ui["rewrite_var"]).pack(anchor="w", padx=5)
    ttk.Checkbutton(frm_opts, text="相册/组合消息 (--group)", variable=ui["group_var"]).pack(anchor="w", padx=5)
    ttk.Checkbutton(frm_opts, text="自动跳过相同文件 (--skip-same)", variable=ui["skip_var"]).pack(anchor="w", padx=5)
    ttk.Checkbutton(frm_opts, text="Takeout 会话 (--takeout)", variable=ui["takeout_var"]).pack(anchor="w", padx=5)

    # ============ 命名模板 ============
    frm_template = ttk.Labelframe(left_frame, text="命名模板设置 (--template)", style="Header.TLabelframe")
    frm_template.pack(fill="x", pady=5)
    ui["use_custom_template"] = tk.BooleanVar()
    ttk.Checkbutton(frm_template, text="启用自定义命名模板 (--template)", variable=ui["use_custom_template"]).pack(anchor="w", padx=5, pady=3)

    template_frame = ttk.Frame(frm_template)
    template_frame.pack(fill="x", padx=10, pady=5)

    fields = [
        ("标题 (FileCaption)", "{{ .FileCaption }}"),
        ("时间 (DownloadDate)", "{{ .DownloadDate }}"),
        ("文件名 (FileName)", "{{ .FileName }}"),
        ("频道名称 (ChatTitle)", "{{ .ChatTitle }}"),
        ("发送者ID (SenderID)", "{{ .SenderID }}"),
        ("文件大小 (FileSize)", "{{ .FileSize }}"),
    ]
    ui["template_checks"] = []
    for i, (label, code) in enumerate(fields):
        var = tk.BooleanVar(value=(i < 3))
        cb = ttk.Checkbutton(template_frame, text=label, variable=var)
        cb.grid(row=i // 2, column=i % 2, sticky="w", padx=5, pady=3)
        ui["template_checks"].append((var, code))

    ttk.Label(frm_template, text="当前模板预览：").pack(anchor="w", padx=5, pady=3)
    ui["template_var"] = tk.StringVar()
    ttk.Entry(frm_template, textvariable=ui["template_var"], width=55, state="readonly").pack(anchor="w", padx=10)
    ttk.Button(frm_template, text="生成模板", command=lambda: update_template(ui)).pack(anchor="w", padx=10, pady=5)

    # ============ 右侧输出与按钮 ============
    frm_output = ttk.Labelframe(right_frame, text="生成命令输出", style="Header.TLabelframe")
    frm_output.pack(fill="both", expand=True, pady=(0, 10))
    txt_output = tk.Text(frm_output, height=20, width=55, wrap="word")
    txt_output.pack(fill="both", padx=5, pady=5)
    ui["output_var"] = type("Var", (), {"set": lambda self, val: (txt_output.delete("1.0", "end"), txt_output.insert("1.0", val))})()

    # 操作按钮
    frm_btn = ttk.Frame(right_frame)
    frm_btn.pack(fill="x", pady=10)
    ttk.Button(frm_btn, text="生成命令", width=18, command=lambda: on_generate_command(ui)).pack(pady=3)
    ttk.Button(frm_btn, text="复制命令", width=18, command=lambda: copy_to_clipboard(root, txt_output)).pack(pady=3)
    ttk.Button(frm_btn, text="清空所有输入", width=18, command=lambda: clear_all_inputs(ui, txt_urls, txt_output)).pack(pady=3)

    return ui


# ===== 辅助函数 =====
def select_dir(ui):
    path = filedialog.askdirectory(title="选择下载目录")
    if path:
        ui["dir_var"].set(path)

def copy_to_clipboard(root, text_widget):
    data = text_widget.get("1.0", "end-1c").strip()
    if not data:
        messagebox.showinfo("提示", "没有可复制的命令。")
        return
    root.clipboard_clear()
    root.clipboard_append(data)
    messagebox.showinfo("已复制", "命令已复制到剪贴板。")

def clear_all_inputs(ui, txt_urls, txt_output):
    txt_urls.delete("1.0", "end")
    txt_output.delete("1.0", "end")
    for k, v in ui.items():
        if isinstance(v, tk.StringVar): v.set("")
        elif isinstance(v, tk.BooleanVar): v.set(False)
    messagebox.showinfo("已清空", "所有输入已重置。")

def update_template(ui):
    if not ui["use_custom_template"].get():
        ui["template_var"].set("")
        return
    selected = [code for var, code in ui["template_checks"] if var.get()]
    if not selected:
        messagebox.showwarning("提示", "请至少选择一个字段！")
        return
    template = "_".join(selected)
    ui["template_var"].set(template)