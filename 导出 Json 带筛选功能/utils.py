import tkinter.messagebox as messagebox

def quote_for_cmd(expr: str) -> str:
    """在 Windows CMD 下正确包裹字符串（兼容双引号）"""
    expr = expr.replace('"', '""')
    return f'"{expr}"'

def show_info(title, msg):
    messagebox.showinfo(title, msg)

def show_error(title, msg):
    messagebox.showerror(title, msg)

def ask_yes_no(title, msg) -> bool:
    return messagebox.askyesno(title, msg)