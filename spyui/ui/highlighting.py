import tkinter as tk
import ctypes


class HighlightOverlay:
    def __init__(self, color="red", thickness=5):
        self.color = color
        self.thickness = thickness

        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.attributes("-transparentcolor", "white")

        # 屏幕适配
        self.root.geometry(
            f"{self.root.winfo_screenwidth()}x{self.root.winfo_screenheight()}+0+0")

        self.canvas = tk.Canvas(self.root, bg="white",
                                highlightthickness=0, bd=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.current_rect = None

        # 必须保留这一个 update，否则 winfo_id() 拿不到有效的句柄
        self.root.update()

        # 优雅获取 HWND
        hwnd = ctypes.windll.user32.GetAncestor(self.root.winfo_id(), 2)

        # 注入穿透样式 (WS_EX_TRANSPARENT | WS_EX_LAYERED)
        GWL_EXSTYLE = -20
        current_style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
        ctypes.windll.user32.SetWindowLongW(
            hwnd, GWL_EXSTYLE, current_style | 0x20 | 0x80000)

    def draw_rect(self, x1, y1, x2, y2):
        if self.current_rect:
            self.canvas.delete(self.current_rect)
        self.current_rect = self.canvas.create_rectangle(
            x1, y1, x2, y2,
            outline=self.color,
            width=self.thickness
        )
        self.root.update()

    def close(self):
        if self.current_rect:
            self.canvas.delete(self.current_rect)
            self.current_rect = None

    def destroy(self):
        self.root.destroy()


if __name__ == "__main__":

    overlay = HighlightOverlay(color="red", thickness=8)
    overlay.draw_rect(100, 100, 800, 600)
    input("Press Enter to close...")
    overlay.close()
    overlay.destroy()
