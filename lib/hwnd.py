import win32gui
import win32api
import time


def get_hwnd_at_cursor(mode="normal"):
    """
    SpyUI 核心探测引擎：抓取成功返回 HWND (int)，失败返回 None
    """
    # 1. 获取屏幕绝对坐标
    point = win32api.GetCursorPos()

    # 2. 基础探测：获取最顶层的窗口句柄
    return win32gui.WindowFromPoint(point)


if __name__ == "__main__":

    while True:
        hwnd = get_hwnd_at_cursor()
        print(f"句柄：{hwnd}, 标题：{win32gui.GetWindowText(hwnd)}")
        time.sleep(1)
