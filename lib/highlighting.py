import win32gui
import win32api
import threading
import time
import ctypes

# 开启 DPI 感知
ctypes.windll.shcore.SetProcessDpiAwareness(1)

class UIHighlighter:
    def __init__(self, color=(255, 0, 0)):
        """
        初始化：仅保留颜色设置
        """
        self.color = win32api.RGB(*color)
        self._stop_event = threading.Event()
        self._thread = None

    def _drawing_loop(self, hwnd):
        # 获取资源
        brush = win32gui.CreateSolidBrush(self.color)
        hdc = win32gui.GetWindowDC(0)
        
        try:
            while not self._stop_event.is_set():
                if not win32gui.IsWindow(hwnd):
                    break
                
                # 获取坐标并直接绘制（API 默认就是 1 像素，不加循环）
                rect = win32gui.GetWindowRect(hwnd)
                win32gui.FrameRect(hdc, rect, brush)
                
                # 刷新频率设为 0.1s
                time.sleep(0.1) 
        finally:
            # 清理资源
            win32gui.ReleaseDC(0, hdc)
            win32gui.DeleteObject(brush)
            win32gui.InvalidateRect(0, None, True)

    def start(self, hwnd):
        self.stop() 
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._drawing_loop, args=(hwnd,), daemon=True)
        self._thread.start()

    def stop(self):
        self._stop_event.set()

if __name__ == "__main__":
    # 初始化一个绿色高亮器
    highlighter = UIHighlighter(color=(0, 255, 0))

    # 标记目标
    target_hwnd = 1380888
    highlighter.start(target_hwnd)
    print(f"窗口 {target_hwnd} 已锁定。")

    input("按回车停止...")
    highlighter.stop()
