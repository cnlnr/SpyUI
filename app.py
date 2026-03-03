import mouse_hwnd
import time
import win32gui
import highlighting

highlighter = highlighting.HighlightOverlay(color="green", thickness=2)

previous_hwnd = None
while True:
    time.sleep(0.5)
    # 获取当前鼠标位置的窗口句柄
    hwnd = mouse_hwnd.get_hwnd_at_cursor()
    # 获取窗口标题
    window_title = win32gui.GetWindowText(hwnd)
    # 获取窗口位置
    rect = win32gui.GetWindowRect(hwnd)
    print(f"句柄：{hwnd}, 标题：{window_title}")

    highlighter.draw_rect(rect[0], rect[1], rect[2], rect[3])