import mouse_hwnd
import time
import win32gui
import highlighting
import ui.hwnd

highlighter = highlighting.HighlightOverlay(color="green", thickness=2)
ui = ui.hwnd.GlimpseUI()

previous_hwnd = None
while True:
    time.sleep(0.1)

    # 1. 获取当前鼠标位置的窗口句柄 (UID)
    hwnd = mouse_hwnd.get_hwnd()
    if not hwnd:
        continue  # 没有获取到窗口，继续循环等待

    # 4. 更新红框位置
    rect = win32gui.GetWindowRect(hwnd)
    highlighter.draw_rect(rect[0], rect[1], rect[2], rect[3])

    # 2. 逻辑应用：唯一标识去重判断
    if hwnd and hwnd != previous_hwnd:
        # 3. 只有 ID 变了才执行以下属性获取和打印

        ui.update(hwnd)  # 更新UI显示

        previous_hwnd = hwnd  # 更新缓存
    elif not hwnd:
        # 如果没拿到句柄，重置状态
        previous_hwnd = None
