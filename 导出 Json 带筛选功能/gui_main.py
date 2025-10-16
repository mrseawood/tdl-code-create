import tkinter as tk
from tkinter import ttk, filedialog
from utils import show_info, ask_yes_no
from tdl_logic import build_command


def main():
    root = tk.Tk()
    root.title("TDL 导出命令生成器（带示例与帮助 + 输出文件夹选择）")
    root.geometry("1320x820")
    root.configure(bg="#f8f9fa")

    style = ttk.Style()
    style.configure("Header.TLabelframe.Label", font=("Microsoft YaHei UI", 11, "bold"))

    # ====== 外框：左右两列 ======
    main_frame = tk.Frame(root, bg="#f8f9fa")
    main_frame.pack(fill="both", expand=True, padx=10, pady=10)

    left_frame = tk.Frame(main_frame, bg="#f8f9fa")
    right_frame = tk.Frame(main_frame, bg="#f8f9fa")
    left_frame.pack(side="left", fill="both", expand=True, padx=(0, 6))
    right_frame.pack(side="right", fill="both", expand=True, padx=(6, 0))

    # 变量
    chat_var   = tk.StringVar()
    topic_var  = tk.StringVar()
    reply_var  = tk.StringVar()
    output_var = tk.StringVar()

    t_type_var  = tk.StringVar(value="time")
    t_range_var = tk.StringVar()

    with_content_var = tk.BooleanVar()
    raw_var          = tk.BooleanVar()
    allmsg_var       = tk.BooleanVar()

    filters_vars = {
        "custom":    tk.StringVar(),
        "message":   tk.StringVar(),
        "name":      tk.StringVar(),
        "views":     tk.StringVar(),
        "forwards":  tk.StringVar(),
        "size":      tk.StringVar(),     # MB
        "fromid":    tk.StringVar(),
        "pinned":    tk.BooleanVar(),
        "silent":    tk.BooleanVar(),
        "mentioned": tk.BooleanVar(),
    }

    # ================= 左列：基础设置 =================
    frm_basic = ttk.Labelframe(left_frame, text="基础设置", style="Header.TLabelframe")
    frm_basic.pack(fill="x", padx=5, pady=5)

    ttk.Label(frm_basic, text="聊天标识 (-c CHAT)：").grid(row=0, column=0, sticky="w", padx=5, pady=4)
    ttk.Entry(frm_basic, textvariable=chat_var, width=35).grid(row=0, column=1, padx=5, pady=4, sticky="w")

    examples = [
        "@iyear（@用户名）",
        "iyear（无@的用户名）",
        "123456789（数值ID）",
        "https://t.me/iyear（公开链接）",
        "+1 123456789（电话号码）",
        "留空=收藏夹"
    ]
    sample_combo = ttk.Combobox(frm_basic, state="readonly", values=examples, width=26)
    sample_combo.set("快速示例…")
    sample_combo.grid(row=0, column=2, padx=5, pady=4, sticky="w")

    def on_pick_example(_evt=None):
        val = sample_combo.get()
        if val.startswith("@iyear"):
            chat_var.set("@iyear")
        elif val.startswith("iyear（"):
            chat_var.set("iyear")
        elif val.startswith("123456789"):
            chat_var.set("123456789")
        elif val.startswith("https://t.me/iyear"):
            chat_var.set("https://t.me/iyear")
        elif val.startswith("+1 123456789"):
            chat_var.set("+1 123456789")
        elif val.startswith("留空"):
            chat_var.set("")
    sample_combo.bind("<<ComboboxSelected>>", on_pick_example)

    def show_chat_help():
        msg = (
            "以 JSON 格式导出聊天/频道/群组中的媒体消息。\n\n"
            "CHAT 可用值（任选其一）：\n"
            "• @iyear          → @用户名\n"
            "• iyear           → 无 @ 的用户名\n"
            "• 123456789       → 数值 ID\n"
            "• https://t.me/iyear → 公开链接\n"
            "• +1 123456789    → 电话号码\n"
            "• 留空            → 收藏夹（Saved Messages）\n\n"
            "如何在 Telegram 桌面端获取聊天 ID：\n"
            "设置 → 高级 → 实验性设置 → 在资料中显示对话 ID"
        )
        show_info("CHAT 可用值说明", msg)

    tk.Button(frm_basic, text="说明", width=6, command=show_chat_help)\
        .grid(row=0, column=3, padx=5, pady=4, sticky="w")

    # 输出文件（带选择文件夹按钮）
    ttk.Label(frm_basic, text="输出文件 (-o)：").grid(row=1, column=0, sticky="w", padx=5, pady=4)
    ttk.Entry(frm_basic, textvariable=output_var, width=35).grid(row=1, column=1, padx=5, pady=4, sticky="w")

    def choose_output_dir():
        folder = filedialog.askdirectory(title="选择输出文件夹")
        if folder:
            output_var.set(f"{folder}/tdl-export.json")
    ttk.Button(frm_basic, text="选择文件夹", command=choose_output_dir)\
        .grid(row=1, column=2, padx=5, pady=4, sticky="w")

    # 主题 / 回复（可选）
    ttk.Label(frm_basic, text="主题 ID (--topic，可选)：").grid(row=2, column=0, sticky="w", padx=5, pady=4)
    ttk.Entry(frm_basic, textvariable=topic_var, width=35).grid(row=2, column=1, padx=5, pady=4, sticky="w")

    ttk.Label(frm_basic, text="回复 ID (--reply，可选)：").grid(row=3, column=0, sticky="w", padx=5, pady=4)
    ttk.Entry(frm_basic, textvariable=reply_var, width=35).grid(row=3, column=1, padx=5, pady=4, sticky="w")

    # ================= 左列：导出范围 =================
    frm_range = ttk.Labelframe(left_frame, text="导出范围 (-T / -i)", style="Header.TLabelframe")
    frm_range.pack(fill="x", padx=5, pady=5)

    ttk.Label(frm_range, text="类型 (-T)：").grid(row=0, column=0, padx=5, pady=3, sticky="w")
    ttk.Combobox(frm_range, textvariable=t_type_var, state="readonly",
                 values=["time", "id", "last"], width=10)\
        .grid(row=0, column=1, padx=5, pady=3)

    ttk.Label(frm_range, text="范围或数量 (-i)：").grid(row=0, column=2, padx=5, pady=3, sticky="w")
    ttk.Entry(frm_range, textvariable=t_range_var, width=25)\
        .grid(row=0, column=3, padx=5, pady=3)

    def show_range_help():
        msg = (
            "【如何填写导出范围 (-T 与 -i)】\n\n"
            "🕒 1) time（按时间范围导出）\n"
            "   - 写法：-i 起始时间戳,结束时间戳（包含两端）。\n"
            "   - 例：把 2024-10-01 ~ 2024-10-03 转成时间戳后填入\n"
            "         -i 1727712000,1727894399\n"
            "   - 时间戳转换：https://www.epochconverter.com\n\n"
            "🧩 2) id（按消息 ID 范围导出）\n"
            "   - 写法：-i 起始ID,结束ID（包含两端）。\n"
            "   - 例：-i 100,500 表示导出 ID 在 100~500 的消息。\n\n"
            "📦 3) last（导出最近 N 条消息）\n"
            "   - 写法：-i N\n"
            "   - 例：-i 100 表示导出最近 100 条。"
        )
        show_info("导出范围使用说明", msg)

    ttk.Button(frm_range, text="📘 使用说明", command=show_range_help)\
        .grid(row=0, column=4, padx=5, pady=3)

    # ================= 左列：附加选项 =================
    frm_opts = ttk.Labelframe(left_frame,
                              text="附加选项 (--with-content / --raw / --all)",
                              style="Header.TLabelframe")
    frm_opts.pack(fill="x", padx=5, pady=5)

    def tip_with_content():
        show_info("附带消息内容 (--with-content)",
                  "导出媒体的同时附带消息文字内容（Message 字段）。")
    def tip_raw():
        show_info("导出原始结构 (--raw)",
                  "用于调试，导出 MTProto 原始结构。一般用户不需要。")
    def tip_all():
        show_info("包含非媒体消息 (--all)",
                  "默认只导出包含媒体的消息；勾选后导出所有消息。")

    ttk.Checkbutton(frm_opts, text="附带消息内容 (--with-content)",
                    variable=with_content_var)\
        .grid(row=0, column=0, sticky="w", padx=5, pady=3)
    tk.Button(frm_opts, text="?", width=2, command=tip_with_content)\
        .grid(row=0, column=1, sticky="w", padx=(0, 8))

    ttk.Checkbutton(frm_opts, text="导出原始结构 (--raw)", variable=raw_var)\
        .grid(row=0, column=2, sticky="w", padx=5, pady=3)
    tk.Button(frm_opts, text="?", width=2, command=tip_raw)\
        .grid(row=0, column=3, sticky="w", padx=(0, 8))

    ttk.Checkbutton(frm_opts, text="包含非媒体消息 (--all)", variable=allmsg_var)\
        .grid(row=0, column=4, sticky="w", padx=5, pady=3)
    tk.Button(frm_opts, text="?", width=2, command=tip_all)\
        .grid(row=0, column=5, sticky="w", padx=(0, 8))

    # ================= 右列：过滤设置 =================
    frm_filter = ttk.Labelframe(right_frame, text="过滤设置 (-f，可选)", style="Header.TLabelframe")
    frm_filter.pack(fill="both", expand=True, padx=5, pady=5)

    ttk.Label(frm_filter, text="自定义表达式：").grid(row=0, column=0, sticky="w", padx=5, pady=3)
    ttk.Entry(frm_filter, textvariable=filters_vars["custom"], width=56)\
        .grid(row=0, column=1, padx=5, pady=3, sticky="w")

    fields = [
        ("消息内容包含 (Message contains)：", "message"),
        ("文件名包含 (Media.Name contains)：", "name"),
        ("浏览数大于 (Views >)：", "views"),
        ("转发数大于 (Forwards >)：", "forwards"),
        ("文件大小大于MB (Media.Size >)：", "size"),
        ("发送者 ID 等于 (FromID ==)：", "fromid"),
    ]
    for i, (label, key) in enumerate(fields, start=1):
        ttk.Label(frm_filter, text=label).grid(row=i, column=0, sticky="w", padx=5, pady=3)
        ttk.Entry(frm_filter, textvariable=filters_vars[key], width=30)\
            .grid(row=i, column=1, padx=5, pady=3, sticky="w")

    ttk.Label(frm_filter, text="布尔筛选：", font=("Microsoft YaHei UI", 9, "bold"))\
        .grid(row=7, column=0, sticky="w", padx=5, pady=(10, 2))
    ttk.Checkbutton(frm_filter, text="仅导出置顶消息 (Pinned)",
                    variable=filters_vars["pinned"])\
        .grid(row=8, column=0, sticky="w", padx=5)
    ttk.Checkbutton(frm_filter, text="仅导出静音消息 (Silent)",
                    variable=filters_vars["silent"])\
        .grid(row=8, column=1, sticky="w", padx=5)
    ttk.Checkbutton(frm_filter, text="仅导出提及我的消息 (Mentioned)",
                    variable=filters_vars["mentioned"])\
        .grid(row=9, column=0, sticky="w", padx=5)

    # ================= 底部：输出 + 按钮 =================
    frm_output = ttk.Labelframe(root, text="命令预览（复制到 CMD/PowerShell 执行）", style="Header.TLabelframe")
    frm_output.pack(fill="both", expand=True, padx=10, pady=(6, 10))
    txt_output = tk.Text(frm_output, height=10, wrap="word",
                         bg="#1e1e1e", fg="#cce7ff", insertbackground="white")
    txt_output.pack(fill="both", expand=True, padx=10, pady=10)

    btn_bar = tk.Frame(root, bg="#f8f9fa")
    btn_bar.pack(pady=(0, 8))

    def on_generate():
        # 若 chat 为空，弹确认（收藏夹）
        if not chat_var.get().strip():
            if not ask_yes_no("提示", "聊天标识为空将导出“收藏夹”。是否继续生成命令？"):
                return
        cmd = build_command(
            chat_var.get(), topic_var.get(), reply_var.get(), output_var.get(),
            t_type_var.get(), t_range_var.get(),
            {k: v.get() if not isinstance(v, tk.BooleanVar) else v.get()
             for k, v in filters_vars.items()},
            with_content_var.get(), raw_var.get(), allmsg_var.get()
        )
        if cmd:
            txt_output.delete("1.0", "end")
            txt_output.insert("1.0", cmd)

    def on_copy():
        data = txt_output.get("1.0", "end-1c").strip()
        if not data:
            show_info("提示", "请先生成命令。")
            return
        root.clipboard_clear()
        root.clipboard_append(data)
        show_info("已复制", "命令已复制到剪贴板。")

    def on_clear():
        chat_var.set("")
        topic_var.set("")
        reply_var.set("")
        output_var.set("")
        t_type_var.set("time")
        t_range_var.set("")
        for v in filters_vars.values():
            if isinstance(v, tk.BooleanVar):
                v.set(False)
            else:
                v.set("")
        with_content_var.set(False)
        raw_var.set(False)
        allmsg_var.set(False)
        txt_output.delete("1.0", "end")

    tk.Button(btn_bar, text="生成命令", bg="#007bff", fg="white", width=14, command=on_generate)\
        .pack(side="left", padx=8)
    tk.Button(btn_bar, text="复制命令", bg="#28a745", fg="white", width=14, command=on_copy)\
        .pack(side="left", padx=8)
    tk.Button(btn_bar, text="清空输入", bg="#dc3545", fg="white", width=14, command=on_clear)\
        .pack(side="left", padx=8)

    root.mainloop()