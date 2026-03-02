import win32gui
import win32api
import time

def start_spy():
    print("开始侦察... (按 Ctrl+C 停止)")
    try:
        while True:
            # 1. 获取当前鼠标的屏幕绝对坐标
            x, y = win32api.GetCursorPos()
            
            # 2. 根据坐标获取该点下方的窗口句柄 (HWND)
            # WindowFromPoint 会返回包含该点的最顶层子窗口
            hwnd = win32gui.WindowFromPoint((x, y))
            
            # 3. 获取窗口详细信息
            title = win32gui.GetWindowText(hwnd)
            class_name = win32gui.GetClassName(hwnd)
            
            # 4. 实时刷新显示
            print(f"坐标: ({x}, {y}) | 句柄: {hwnd} | 类名: {class_name} | 标题: {title}", end='\r')
            
            time.sleep(0.1)  # 降低 CPU 占用
    except KeyboardInterrupt:
        print("\n侦察结束。")

if __name__ == "__main__":
    start_spy()
