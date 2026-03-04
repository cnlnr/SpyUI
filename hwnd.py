import keyboard
import mouse_hwnd
import time
import win32gui
import ui.highlighting as highlighting
import ui.hwnd

highlighter = highlighting.HighlightOverlay(color="green", thickness=2)
gui = ui.hwnd.GlimpseUI()

previous_hwnd = None

# 设置退出标志
exit_flag = False

# 当 Ctrl 被按下时，将 exit_flag 设置为 True


def on_ctrl(e):
    global exit_flag
    exit_flag = True


keyboard.on_press_key("ctrl", on_ctrl)

print("SpyUI(HWND) 窗口句柄侦察器")


while not exit_flag:
    time.sleep(0.05)

    hwnd = mouse_hwnd.get_hwnd()
    if not hwnd:
        previous_hwnd = None
        continue

    rect = win32gui.GetWindowRect(hwnd)
    highlighter.draw_rect(rect[0], rect[1], rect[2], rect[3])

    if hwnd != previous_hwnd:
        gui.update(hwnd)
        previous_hwnd = hwnd
gui.stop()
ui.hwnd.cls()
ui.hwnd.info(hwnd)
input()