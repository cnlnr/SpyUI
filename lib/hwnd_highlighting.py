import tkinter as tk
import ctypes
import win32gui
import win32con

ctypes.windll.shcore.SetProcessDpiAwareness(1)

class UIHighlighter:
    def __init__(self, color="red", thickness=2):
        self.color, self.thickness, self.root = color, thickness, None

    def start(self, target_hwnd):
        if self.root: self.stop()

        _, _, w, h = win32gui.GetClientRect(target_hwnd)
        
        self.root = tk.Tk()
        self.root.overrideredirect(True)
        
        # 直接使用白色作为透明穿透基准色，不再定义变量
        self.root.config(bg='white')
        self.root.attributes("-transparentcolor", 'white')

        self.root.update_idletasks()
        self.root.update()
        self.root.geometry(f"{w}x{h}+0+0")

        # 绘制画布，背景设为白色以触发透明效果
        tk.Canvas(self.root, bg='white', highlightbackground=self.color,
                  highlightthickness=self.thickness, bd=0).pack(fill=tk.BOTH, expand=True)

        tk_hwnd = ctypes.windll.user32.GetParent(self.root.winfo_id()) or self.root.winfo_id()

        # 物理挂载
        ctypes.windll.user32.SetParent(tk_hwnd, target_hwnd)

        # 样式与鼠标穿透
        style = ctypes.windll.user32.GetWindowLongW(tk_hwnd, win32con.GWL_STYLE)
        ctypes.windll.user32.SetWindowLongW(tk_hwnd, win32con.GWL_STYLE, (style & ~win32con.WS_POPUP) | win32con.WS_CHILD)
        
        ex_style = ctypes.windll.user32.GetWindowLongW(tk_hwnd, win32con.GWL_EXSTYLE)
        ctypes.windll.user32.SetWindowLongW(tk_hwnd, win32con.GWL_EXSTYLE,
                                            ex_style | win32con.WS_EX_LAYERED | win32con.WS_EX_TRANSPARENT)

        win32gui.SetWindowPos(tk_hwnd, win32con.HWND_TOP, 0, 0, w, h, win32con.SWP_SHOWWINDOW | win32con.SWP_NOACTIVATE)
        self.root.update()

    def stop(self):
        if self.root:
            self.root.destroy()
            self.root = None



if __name__ == "__main__":

    # 1. 目标句柄
    target_hwnd = 1840054

    # 2. 检查句柄是否还在
    if win32gui.IsWindow(target_hwnd):
        print(f">>> 发现目标窗口 [HWND: {target_hwnd}]")

        # 3. 初始化高亮器 (紫色，3像素粗)
        highlighter = UIHighlighter(color="purple", thickness=3)

        print(">>> 正在执行『物理焊接』挂载...")
        # 4. 执行挂载
        # 此时 Tkinter 窗口会直接变成 target_hwnd 的子窗口
        highlighter.start(target_hwnd)

        print(">>> 挂载成功！")
        print(">>> 现在的行为：")
        print("    1. 你拖动原窗口，方框会静止不动地跟着走（因为坐标系已锁定）。")
        print("    2. 你缩放原窗口，方框会保持在左上角（除非你手动更新长宽）。")
        print("    3. 你的鼠标可以穿过方框点击目标窗口。")

        # 保持运行，直到手动按回车停止
        input("\n[按下回车键停止挂载并销毁方框]\n")
        highlighter.stop()
        print(">>> 挂载已解除。")
    else:
        print(f"错误：句柄 {target_hwnd} 当前无效。")
        print("请确保目标窗口已打开，并使用你的探测器获取最新的句柄。")
