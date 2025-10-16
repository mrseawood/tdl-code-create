# template_config.py
import tkinter as tk
from tkinter import ttk, messagebox

def build_template_ui(parent_frame, template_var, enable_template_var):
    """命名模板设置 (安全版，含 filenamify 过滤)"""
    frame = tk.LabelFrame(parent_frame, text="命名模板设置 (--template)",
                          font=("微软雅黑", 10, "bold"),
                          bg="#f5f6fa", padx=10, pady=10, labelanchor="nw")
    frame.pack(fill="x", padx=15, pady=10, anchor="w")

    # 启用模板复选框
    tk.Checkbutton(
        frame,
        text="启用自定义命名 (--template)",
        variable=enable_template_var,
        font=("微软雅黑", 10, "bold"),
        bg="#f5f6fa"
    ).pack(anchor="w", pady=(0, 10))

    # -----------------------------
    # 一、下拉模板
    # -----------------------------
    tk.Label(frame, text="选择命名模板（预设组合）:",
             font=("微软雅黑", 10), bg="#f5f6fa").pack(anchor="w")

    template_options = {
        "标题 + 时间 + 文件名 (推荐)": "{{ filenamify .FileCaption 64 }}_{{ formatDate .DownloadDate `2006-01-02-15-04-05` }}_{{ filenamify .FileName }}",
        "仅文件名": "{{ filenamify .FileName }}",
        "频道名 + 文件名": "{{ filenamify .ChatTitle 32 }}_{{ filenamify .FileName }}",
        "日期 + 文件名": "{{ formatDate .DownloadDate `2006-01-02` }}_{{ filenamify .FileName }}",
        "发送者ID + 文件名": "{{ .SenderID }}_{{ filenamify .FileName }}",
        "文件大小 + 文件名": "{{ .FileSize }}B_{{ filenamify .FileName }}",
        "🧩 自定义组合": "CUSTOM"
    }

    combo = ttk.Combobox(frame, state="readonly", font=("Consolas", 10), width=100)
    combo["values"] = list(template_options.keys())
    combo.current(0)
    combo.pack(padx=10, pady=5)

    # -----------------------------
    # 二、自定义组合区
    # -----------------------------
    custom_frame = tk.Frame(frame, bg="#f5f6fa")
    custom_frame.pack(fill="x", padx=20, pady=(5, 5))

    tk.Label(custom_frame, text="自定义命名字段选择：",
             font=("微软雅黑", 10), bg="#f5f6fa").grid(row=0, column=0, sticky="w", pady=(0, 5))

    field_defs = [
        ("标题（FileCaption）", "{{ filenamify .FileCaption 64 }}"),
        ("时间（DownloadDate）", "{{ formatDate .DownloadDate `2006-01-02-15-04-05` }}"),
        ("文件名（FileName）", "{{ filenamify .FileName }}"),
        ("频道名（ChatTitle）", "{{ filenamify .ChatTitle 32 }}"),
        ("发送者ID（SenderID）", "{{ .SenderID }}"),
        ("文件大小（FileSize）", "{{ .FileSize }}B")
    ]
    custom_vars = []
    for i, (label, expr) in enumerate(field_defs):
        var = tk.BooleanVar(value=False)
        cb = tk.Checkbutton(custom_frame, text=label, variable=var,
                            bg="#f5f6fa", font=("微软雅黑", 10))
        cb.grid(row=i + 1, column=0, sticky="w", padx=30)
        custom_vars.append((var, expr))

    # -----------------------------
    # 三、当前模板显示框
    # -----------------------------
    tk.Label(frame, text="当前模板内容：", font=("微软雅黑", 10), bg="#f5f6fa")\
        .pack(anchor="w", pady=(8, 0), padx=10)
    preview_box = tk.Entry(frame, textvariable=template_var, width=95,
                           font=("Consolas", 10), state="readonly")
    preview_box.pack(padx=10, pady=(2, 5))

    # -----------------------------
    # 四、生成模板按钮
    # -----------------------------
    def generate_template():
        if not enable_template_var.get():
            messagebox.showinfo("提示", "请先启用自定义命名 (--template)")
            return

        selected = combo.get()
        if selected == "🧩 自定义组合":
            selected_parts = [expr for var, expr in custom_vars if var.get()]
            if not selected_parts:
                messagebox.showwarning("提示", "请至少勾选一个自定义字段！")
                return
            final_template = "_".join(selected_parts)
        else:
            final_template = template_options[selected]

        template_var.set(final_template)
        preview_box.config(state="normal")
        preview_box.delete(0, "end")
        preview_box.insert(0, final_template)
        preview_box.config(state="readonly")

    tk.Button(frame, text="生成当前模板", bg="#4CAF50", fg="white",
              font=("微软雅黑", 10, "bold"), width=15,
              command=generate_template).pack(anchor="w", padx=30, pady=(8, 3))

    # -----------------------------
    # 五、状态控制
    # -----------------------------
    def toggle_enable(*_):
        if enable_template_var.get():
            combo.config(state="readonly")
            generate_template()
        else:
            combo.config(state="disabled")
            template_var.set("")
            preview_box.config(state="normal")
            preview_box.delete(0, "end")
            preview_box.insert(0, "（未启用自定义命名）")
            preview_box.config(state="readonly")

    enable_template_var.trace_add("write", toggle_enable)

    # 提示文字
    tk.Label(frame, text="说明：\n1️⃣ 所有命名字段都自动过滤非法字符，确保符合 Windows 命名规范；\n"
                         "2️⃣ 你可自由组合命名字段（如 标题+时间+文件名）；\n"
                         "3️⃣ filenamify 会限制字符串长度并替换特殊符号。",
             font=("微软雅黑", 9), fg="#555", bg="#f5f6fa",
             wraplength=700, justify="left").pack(anchor="w", pady=(5, 0))

    toggle_enable()
    return frame