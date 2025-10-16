# utils.py
import tkinter as tk
from tkinter import filedialog, messagebox

def browse_directory(var):
    """选择文件夹"""
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        var.set(folder_selected)

def copy_to_clipboard(root, text_widget):
    """复制输出框文本到剪贴板"""
    command = text_widget.get("1.0", tk.END).strip()
    if not command:
        messagebox.showinfo("提示", "没有内容可复制。")
        return
    root.clipboard_clear()
    root.clipboard_append(command)
    messagebox.showinfo("提示", "命令已复制到剪贴板！")