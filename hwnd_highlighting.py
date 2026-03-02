import ctypes
from ctypes import wintypes

user32 = ctypes.windll.user32
dwmapi = ctypes.windll.dwmapi

DWMWA_BORDER_COLOR = 34
GA_ROOT = 2

def RGB(r,g,b):
    return r | (g<<8) | (b<<16)

hwnd = user32.FindWindowW(None, "任务管理器")

if not hwnd:
    print("窗口没找到")
    exit()

# 获取顶级窗口
hwnd = user32.GetAncestor(hwnd, GA_ROOT)

print("HWND:", hwnd)

color = ctypes.c_uint(RGB(255,0,0))

result = dwmapi.DwmSetWindowAttribute(
    hwnd,
    DWMWA_BORDER_COLOR,
    ctypes.byref(color),
    ctypes.sizeof(color)
)

print("result:", hex(result))