import mouse_hwnd
import time
import win32gui
import hwnd_highlighting

highlighter = hwnd_highlighting.UIHighlighter(color="purple", thickness=3)

previous_hwnd = None

while True:
    # 获取当前鼠标位置的窗口句柄
    current_hwnd = mouse_hwnd.get_hwnd_at_cursor()
    # 获取窗口标题
    window_title = win32gui.GetWindowText(current_hwnd)
    print(f"句柄：{current_hwnd}, 标题：{window_title}")
    
    # 核心逻辑：只有当前句柄和上一个句柄不同时，才执行高亮操作
    if current_hwnd != previous_hwnd:
        highlighter.start(current_hwnd)
        # 更新上一个句柄为当前句柄
        previous_hwnd = current_hwnd
    
    time.sleep(0.3)