import tkinter as tk
import ctypes
import win32gui
import win32con

ctypes.windll.shcore.SetProcessDpiAwareness(1)


class UIHighlighter:
    def __init__(self, color="red", thickness=2):
        self.color, self.thickness, self.root = color, thickness, None

    def start(self, target_hwnd):
        """
        极致优雅：修正『无效窗口句柄』错误的挂载版本
        """
        if self.root:
            self.stop()

        # 1. 获取目标尺寸
        _, _, w, h = win32gui.GetClientRect(target_hwnd)
        trans = '#abcdef'

        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.config(bg=trans)
        self.root.attributes("-transparentcolor", trans)

        # 【关键修正 1】：强制 Tkinter 立即创建底层原生窗口
        # 这一步如果不做，下面的 GetParent 就会抓到无效句柄
        self.root.update_idletasks()
        self.root.update()

        self.root.geometry(f"{w}x{h}+0+0")

        # 3. 绘制方框
        tk.Canvas(self.root, bg=trans, highlightbackground=self.color,
                  highlightthickness=self.thickness).pack(fill=tk.BOTH, expand=True)

        # 4. 获取 Tkinter 窗口的真正原生句柄
        # 使用 winfo_id() 拿到内部句柄，再转为整数
        tk_internal_id = self.root.winfo_id()
        tk_hwnd = ctypes.windll.user32.GetParent(tk_internal_id)

        # 验证抓到的句柄是否有效
        if not win32gui.IsWindow(tk_hwnd):
            # 如果 GetParent 失败，尝试直接使用内部 ID
            tk_hwnd = tk_internal_id

        # 【核心：物理挂载】
        ctypes.windll.user32.SetParent(tk_hwnd, target_hwnd)

        # 样式调整
        style = ctypes.windll.user32.GetWindowLongW(
            tk_hwnd, win32con.GWL_STYLE)
        new_style = (style & ~win32con.WS_POPUP) | win32con.WS_CHILD
        ctypes.windll.user32.SetWindowLongW(
            tk_hwnd, win32con.GWL_STYLE, new_style)

        # 5. 开启鼠标穿透
        ex_style = ctypes.windll.user32.GetWindowLongW(
            tk_hwnd, win32con.GWL_EXSTYLE)
        ctypes.windll.user32.SetWindowLongW(tk_hwnd, win32con.GWL_EXSTYLE,
                                            ex_style | win32con.WS_EX_LAYERED | win32con.WS_EX_TRANSPARENT)

        # 6. 【关键修正 2】：使用 try 保护 SetWindowPos
        try:
            win32gui.SetWindowPos(tk_hwnd, win32con.HWND_TOP, 0, 0, w, h,
                                  win32con.SWP_SHOWWINDOW | win32con.SWP_NOACTIVATE)
        except Exception as e:
            print(f"SetWindowPos 警告 (可忽略): {e}")

        self.root.update()

    def stop(self):
        if self.root:
            self.root.destroy()
            self.root = None


if __name__ == "__main__":
    import time

    # 1. 目标句柄
    target_hwnd = 9112144

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
