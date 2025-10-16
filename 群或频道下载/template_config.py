import tkinter as tk
from tkinter import ttk, messagebox


def build_template_ui(parent_frame, template_var: tk.StringVar, enable_template_var: tk.BooleanVar):
    """
    命名模板设置（支持预设 与 自定义组合，二选一）
    """
    frame = ttk.Labelframe(parent_frame, text="命名模板设置 (--template)")
    frame.pack(fill="x", padx=2, pady=4)

    # 启用模板
    tk.Checkbutton(frame, text="启用自定义命名模板 (--template)", variable=enable_template_var)\
        .grid(row=0, column=0, sticky="w", padx=8, pady=(8, 4))

    # 预设模板
    tk.Label(frame, text="预设模板：").grid(row=1, column=0, sticky="w", padx=8)
    presets = {
        "标题 + 时间 + 文件名（默认）":
            "{{ filenamify .FileCaption 64 }}_{{ formatDate .DownloadDate `2006-01-02-15-04-05` }}_{{ filenamify .FileName }}",
        "仅文件名":
            "{{ filenamify .FileName }}",
        "频道名 + 文件名":
            "{{ filenamify .ChatTitle 32 }}_{{ filenamify .FileName }}",
        "日期 + 文件名":
            "{{ formatDate .DownloadDate `2006-01-02` }}_{{ filenamify .FileName }}",
        "发送者ID + 文件名":
            "{{ .SenderID }}_{{ filenamify .FileName }}",
        "文件大小 + 文件名":
            "{{ .FileSize }}B_{{ filenamify .FileName }}",
        "🧩 自定义组合（勾选下方项）": "CUSTOM"
    }
    combo = ttk.Combobox(frame, state="readonly", width=52, values=list(presets.keys()))
    combo.grid(row=1, column=1, sticky="w", padx=6, pady=4)
    combo.set("标题 + 时间 + 文件名（默认）")

    # 自定义组合
    tk.Label(frame, text="自定义组合（仅在选“自定义组合”时生效）：").grid(row=2, column=0, sticky="w", padx=8, pady=(6, 0))

    custom_area = tk.Frame(frame)
    custom_area.grid(row=2, column=1, sticky="w", padx=6, pady=(6, 4))

    fields = [
        ("标题 (FileCaption)", "{{ filenamify .FileCaption 64 }}"),
        ("时间 (DownloadDate)", "{{ formatDate .DownloadDate `2006-01-02-15-04-05` }}"),
        ("文件名 (FileName)", "{{ filenamify .FileName }}"),
        ("频道名称 (ChatTitle)", "{{ filenamify .ChatTitle 32 }}"),
        ("发送者ID (SenderID)", "{{ .SenderID }}"),
        ("文件大小 (FileSize)", "{{ .FileSize }}B"),
    ]
    vars_checks = []
    for i, (label, expr) in enumerate(fields):
        var = tk.BooleanVar(value=False)
        cb = tk.Checkbutton(custom_area, text=label, variable=var)
        cb.grid(row=i // 3, column=i % 3, sticky="w", padx=6, pady=2)
        vars_checks.append((var, expr))

    # 当前模板 + 生成按钮
    tk.Label(frame, text="当前模板：").grid(row=3, column=0, sticky="w", padx=8, pady=(6, 0))
    ent_preview = tk.Entry(frame, textvariable=template_var, width=70, state="readonly")
    ent_preview.grid(row=3, column=1, sticky="w", padx=6, pady=(6, 0))

    def generate_template():
        if not enable_template_var.get():
            messagebox.showinfo("提示", "请先勾选“启用自定义命名模板”。")
            return
        sel = combo.get()
        if not sel:
            messagebox.showwarning("提示", "请选择一个预设模板或“自定义组合”。")
            return

        if presets.get(sel) == "CUSTOM":
            parts = [expr for v, expr in vars_checks if v.get()]
            if not parts:
                # 自定义未选任何字段时，给默认模板，避免“启用但为空”
                templ = "{{ filenamify .FileCaption 64 }}_{{ formatDate .DownloadDate `2006-01-02-15-04-05` }}_{{ filenamify .FileName }}"
            else:
                templ = "_".join(parts)
        else:
            templ = presets[sel]

        ent_preview.configure(state="normal")
        ent_preview.delete(0, "end")
        ent_preview.insert(0, templ)
        ent_preview.configure(state="readonly")

    tk.Button(frame, text="生成当前模板", width=14, command=generate_template)\
        .grid(row=4, column=1, sticky="w", padx=6, pady=8)

    # 说明
    hint = (
        "说明：\n"
        "1) 预设与自定义组合二选一；\n"
        "2) 勾选“启用自定义命名模板”后，点击“生成当前模板”使之生效；\n"
        "3) 内置 filenamify / formatDate 等可避免 Windows 非法文件名。"
    )
    tk.Label(frame, text=hint, fg="#6c757d", justify="left").grid(row=5, column=0, columnspan=2, sticky="w", padx=8, pady=(0, 8))

    return frame