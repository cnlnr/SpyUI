import tkinter as tk
import ctypes

# 1. 强制声明 DPI 感知，确保 4K 或缩放屏下坐标 100% 精准
ctypes.windll.shcore.SetProcessDpiAwareness(1)

class UIHighlighter:
    def __init__(self, color="red", thickness=1):
        # 保留初始化配置：颜色和粗细
        self.color, self.thickness, self.root = color, thickness, None

    def start(self, rect):
        """开启高亮标记"""
        if self.root: self.stop()
        
        l, t, r, b = rect
        w, h, trans = r - l, b - t, '#abcdef' # 使用特定色键实现透明

        self.root = tk.Tk()
        # 置顶、无边框、设置透明色
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True, "-transparentcolor", trans)
        self.root.geometry(f"{w}x{h}+{l}+{t}")

        # 【核心优化】：利用 Canvas 边框实现颜色和厚度
        # 这种方式在 thickness=1 时绝对闭合，且代码量极少
        tk.Canvas(self.root, bg=trans, 
                  highlightbackground=self.color, # 这里应用你的自定义颜色
                  highlightthickness=self.thickness).pack(fill=tk.BOTH, expand=True)

        # 开启鼠标穿透 (WS_EX_LAYERED | WS_EX_TRANSPARENT)
        hwnd = ctypes.windll.user32.GetParent(self.root.winfo_id())
        style = ctypes.windll.user32.GetWindowLongW(hwnd, -20)
        ctypes.windll.user32.SetWindowLongW(hwnd, -20, style | 0x80000 | 0x20)
        self.root.update()

    def stop(self):
        """停止并销毁高亮标记"""
        if self.root:
            self.root.destroy()
            self.root = None

if __name__ == "__main__":
    import time
    # 测试：绿色、1像素
    h = UIHighlighter(color="green", thickness=3)
    h.start((300, 300, 700, 600))
    
    print("高亮已开启，5秒后自动关闭...")
    time.sleep(5)
    h.stop()
