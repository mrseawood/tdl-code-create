import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from template_config import build_template_ui


def build_main_ui(root, on_generate_command):
    """
    构建主界面。返回一个字典 ui，包含所有 tk 变量与关键控件句柄。
    """
    ui = {}

    # ===== 顶层容器：左右两列 =====
    main = tk.Frame(root, bg="#f8f9fb")
    main.pack(fill="both", expand=True, padx=10, pady=8)

    left = tk.Frame(main, bg="#f8f9fb")
    right = tk.Frame(main, bg="#f8f9fb")
    left.pack(side="left", fill="both", expand=True, padx=(0, 6))
    right.pack(side="right", fill="both", expand=True, padx=(6, 0))

    # ===== 左列：导入 JSON、输出目录、并发、功能选项 =====
    # 导入 JSON
    frm_json = ttk.Labelframe(left, text="导入 JSON 下载（替代链接下载）")
    frm_json.pack(fill="x", padx=2, pady=4)

    ui["json_path_var"] = tk.StringVar()
    tk.Label(frm_json, text="导出 JSON 文件路径 (-f)：").grid(row=0, column=0, sticky="w", padx=6, pady=6)
    tk.Entry(frm_json, textvariable=ui["json_path_var"], width=70).grid(row=0, column=1, padx=6, pady=6, sticky="w")

    def pick_json():
        path = filedialog.askopenfilename(
            title="选择 tdl 导出的 JSON 文件",
            filetypes=[("JSON 文件", "*.json"), ("所有文件", "*.*")]
        )
        if path:
            ui["json_path_var"].set(path)

    tk.Button(frm_json, text="浏览...", command=pick_json, width=8).grid(row=0, column=2, padx=6, pady=6)

    # 自定义目录
    frm_dir = ttk.Labelframe(left, text="自定义目录 (-d，可选)")
    frm_dir.pack(fill="x", padx=2, pady=4)
    ui["dir_var"] = tk.StringVar()
    tk.Entry(frm_dir, textvariable=ui["dir_var"], width=70).grid(row=0, column=0, padx=6, pady=6, sticky="w")

    def pick_dir():
        d = filedialog.askdirectory(title="选择下载保存目录")
        if d:
            ui["dir_var"].set(d)

    tk.Button(frm_dir, text="浏览...", command=pick_dir, width=8).grid(row=0, column=1, padx=6, pady=6)

    # 线程与并发（可选）
    frm_thr = ttk.Labelframe(left, text="线程与并发（勾选才启用）")
    frm_thr.pack(fill="x", padx=2, pady=4)

    ui["enable_threads_var"] = tk.BooleanVar(value=False)
    ui["threads_var"] = tk.StringVar()
    ui["enable_parallel_var"] = tk.BooleanVar(value=False)
    ui["parallel_var"] = tk.StringVar()

    def toggle_threads():
        ent_threads.configure(state="normal" if ui["enable_threads_var"].get() else "disabled")

    def toggle_parallel():
        ent_parallel.configure(state="normal" if ui["enable_parallel_var"].get() else "disabled")

    tk.Checkbutton(frm_thr, text="启用线程参数 (-t)", variable=ui["enable_threads_var"], command=toggle_threads)\
        .grid(row=0, column=0, sticky="w", padx=6, pady=(6, 3))
    ent_threads = tk.Entry(frm_thr, textvariable=ui["threads_var"], width=8, state="disabled")
    ent_threads.grid(row=0, column=1, sticky="w", padx=4, pady=(6, 3))

    tk.Checkbutton(frm_thr, text="启用并发参数 (-l)", variable=ui["enable_parallel_var"], command=toggle_parallel)\
        .grid(row=0, column=2, sticky="w", padx=(16, 6), pady=(6, 3))
    ent_parallel = tk.Entry(frm_thr, textvariable=ui["parallel_var"], width=8, state="disabled")
    ent_parallel.grid(row=0, column=3, sticky="w", padx=4, pady=(6, 3))

    tk.Label(frm_thr, text="说明：仅勾选后才会把数值写入命令。").grid(row=1, column=0, columnspan=4, sticky="w", padx=6, pady=(0, 6))

    # 功能选项
    frm_opts = ttk.Labelframe(left, text="功能选项（可多选）")
    frm_opts.pack(fill="x", padx=2, pady=4)

    ui["desc_var"] = tk.BooleanVar()
    ui["rewrite_var"] = tk.BooleanVar()
    ui["group_var"] = tk.BooleanVar()
    ui["skip_var"] = tk.BooleanVar()
    ui["takeout_var"] = tk.BooleanVar()

    tk.Checkbutton(frm_opts, text="反序下载 (--desc)", variable=ui["desc_var"]).grid(row=0, column=0, sticky="w", padx=6, pady=4)
    tk.Checkbutton(frm_opts, text="MIME 探测修正扩展名 (--rewrite-ext)", variable=ui["rewrite_var"])\
        .grid(row=0, column=1, sticky="w", padx=20, pady=4)
    tk.Checkbutton(frm_opts, text="相册/组合消息识别 (--group)", variable=ui["group_var"])\
        .grid(row=1, column=0, sticky="w", padx=6, pady=4)
    tk.Checkbutton(frm_opts, text="自动跳过相同文件 (--skip-same)", variable=ui["skip_var"])\
        .grid(row=1, column=1, sticky="w", padx=20, pady=4)
    tk.Checkbutton(frm_opts, text="Takeout 会话 (--takeout)", variable=ui["takeout_var"])\
        .grid(row=2, column=0, sticky="w", padx=6, pady=4)

    # ===== 右列：模板区 + 输出区 =====
    ui["use_template_var"] = tk.BooleanVar(value=False)
    ui["template_var"] = tk.StringVar()
    build_template_ui(right, template_var=ui["template_var"], enable_template_var=ui["use_template_var"])

    # 输出
    frm_out = ttk.Labelframe(right, text="生成的命令")
    frm_out.pack(fill="both", expand=True, padx=2, pady=(4, 2))
    txt = tk.Text(frm_out, height=12, wrap="word", bg="#101114", fg="#cce7ff", insertbackground="#ffffff")
    txt.pack(fill="both", expand=True, padx=6, pady=6)
    ui["output_text"] = txt

    # 底部按钮（居中放置）
    bottom = tk.Frame(root, bg="#f8f9fb")
    bottom.pack(side="bottom", fill="x", pady=(10, 12))

    # 内层按钮容器，用于居中对齐
    btn_frame = tk.Frame(bottom, bg="#f8f9fb")
    btn_frame.pack(anchor="center")

    btn_gen = tk.Button(btn_frame, text="生成命令", width=12, bg="#0d6efd", fg="white",
                        activebackground="#0b5ed7", activeforeground="white",
                        command=lambda: on_generate_command(ui))
    btn_gen.pack(side="left", padx=12)

    ui["btn_copy"] = tk.Button(btn_frame, text="复制命令", width=12, bg="#198754", fg="white",
                               activebackground="#157347", activeforeground="white")
    ui["btn_copy"].pack(side="left", padx=12)

    ui["btn_clear"] = tk.Button(btn_frame, text="清空输入", width=12, bg="#dc3545", fg="white",
                                activebackground="#bb2d3b", activeforeground="white")
    ui["btn_clear"].pack(side="left", padx=12)

    return ui