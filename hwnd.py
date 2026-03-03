import mouse_hwnd
import time
import win32gui
import highlighting

highlighter = highlighting.HighlightOverlay(color="green", thickness=2)

previous_hwnd = None
while True:
    time.sleep(0.1)
    try:
        # 1. 获取当前鼠标位置的窗口句柄 (UID)
        hwnd = mouse_hwnd.get_hwnd()
        
        # 2. 逻辑应用：唯一标识去重判断
        if hwnd and hwnd != previous_hwnd:
            # 3. 只有 ID 变了才执行以下属性获取和打印
            window_title = win32gui.GetWindowText(hwnd)
            rect = win32gui.GetWindowRect(hwnd)
            
            print(f"句柄：{hwnd}, 标题：{window_title}")
            
            # 4. 更新红框位置
            highlighter.draw_rect(rect[0], rect[1], rect[2], rect[3])
            
            previous_hwnd = hwnd # 更新缓存
        elif not hwnd:
            # 如果没拿到句柄，重置状态
            previous_hwnd = None
            
    except Exception:
        # 参考 UIA 例子中的逻辑：静默跳过错误
        pass
