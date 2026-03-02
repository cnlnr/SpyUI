import win32gui
import ctypes
import win32api


# 强制声明进程支持 DPI 感知（仅限 Win8.1 及以上系统）
# 1 代表 PROCESS_PER_MONITOR_DPI_AWARE，确保在不同缩放倍数的显示器间也准确
ctypes.windll.shcore.SetProcessDpiAwareness(1)


import time

def persistent_frame(hwnd, duration=5):
    """持续绘制方框，duration 为持续秒数"""
    start_time = time.time()
    brush = win32gui.CreateSolidBrush(win32api.RGB(255, 0, 0))
    
    try:
        while time.time() - start_time < duration:
            rect = win32gui.GetWindowRect(hwnd)
            hdc = win32gui.GetWindowDC(0)
            win32gui.FrameRect(hdc, rect, brush)
            win32gui.ReleaseDC(0, hdc)
            time.sleep(0.01) # 10ms 刷新一次，减少闪烁
    finally:
        win32gui.DeleteObject(brush)
        # 强制系统重绘该区域以清除残余红框
        win32gui.InvalidateRect(0, None, True)



# 测试：给句柄 1380888 画个“色块”标记
persistent_frame(1380888, 3)
input("按回车继续...")
