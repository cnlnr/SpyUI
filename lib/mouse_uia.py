import ctypes
from ctypes import wintypes
from comtypes import client

# --- 保持你原有的初始化逻辑 ---
uia_module = client.GetModule("UIAutomationCore.dll")
from comtypes.gen.UIAutomationClient import CUIAutomation, IUIAutomationElement
uia = client.CreateObject(CUIAutomation, interface=uia_module.IUIAutomation)

def get_uia_id():
    """获取鼠标当前位置元素的 RuntimeId (唯一标识)"""
    # 1. 获取鼠标坐标
    point = wintypes.POINT()
    ctypes.windll.user32.GetCursorPos(ctypes.byref(point))
    
    try:
        # 2. 从坐标获取元素
        element = uia.ElementFromPoint(point)
        
        # 3. 获取 RuntimeId (返回的是一个包含整数的元组)
        # 这是 UIA 规范中定义的跨进程唯一标识
        runtime_id = element.GetRuntimeId()
        
        return runtime_id
    except Exception as e:
        # 无法获取元素（例如指向了系统保护窗口或任务栏某些区域）
        return None

if __name__ == "__main__":
    import time
    last_id = None
    while True:
        try:
            # 1. 获取鼠标指向的元素
            pt = ctypes.wintypes.POINT()
            ctypes.windll.user32.GetCursorPos(ctypes.byref(pt))
            el = uia.ElementFromPoint(pt)
            
            # 2. 唯一标识去重并打印属性
            uid = el.GetRuntimeId()
            if uid != last_id:
                print(f"ID: {uid} | 名称: {el.CurrentName} | 类名: {el.CurrentClassName}")
                last_id = uid
        except:
            pass
        time.sleep(0.1)

