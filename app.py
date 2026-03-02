import mouse_hwnd
import time
import win32gui
import highlighting

highlighter = highlighting.UIHighlighter(color="purple", thickness=3)

previous_hwnd = None
while True:
    time.sleep(0.5)  # 减少 CPU 占用
    # 获取当前鼠标位置的窗口句柄
    current_hwnd = mouse_hwnd.get_hwnd_at_cursor()
    # 获取窗口标题
    window_title = win32gui.GetWindowText(current_hwnd)
    print(f"句柄：{current_hwnd}, 标题：{window_title}")

    rect = win32gui.GetWindowRect(current_hwnd)
    print(f"窗口坐标: {rect}")
    highlighter.start(rect)