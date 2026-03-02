import hwnd
import time
import win32gui
import hwnd_highlighting

highlighter = hwnd_highlighting.UIHighlighter(color="purple", thickness=3)

while True:
    hwnd = hwnd.get_hwnd_at_cursor()
    print(f"句柄：{hwnd}, 标题：{win32gui.GetWindowText(hwnd)}")
    highlighter.start(hwnd)
    time.sleep(1)

