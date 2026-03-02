import time
import ctypes
from comtypes import client

# 1. 初始化 UIA 核心接口
# UIAutomationCore.dll 是 Windows 自带的
try:
    # 尝试加载 UIA 库并创建 CUIAutomation 对象
    uia_module = client.GetModule("UIAutomationCore.dll")
    from comtypes.gen.UIAutomationClient import CUIAutomation, IUIAutomationElement
    uia = client.CreateObject(CUIAutomation, interface=uia_module.IUIAutomation)
except Exception as e:
    print(f"初始化 UIA 失败: {e}")
    exit()

def start_native_uia_spy():
    print("SpyUI (原生 UIA 模式) 启动... 移动鼠标进行侦察。")
    
    last_element_ptr = None
    
    try:
        while True:
            # 获取鼠标当前坐标
            point = ctypes.wintypes.POINT()
            ctypes.windll.user32.GetCursorPos(ctypes.byref(point))
            
            # 2. 调用原生 API: ElementFromPoint
            try:
                element = uia.ElementFromPoint(point)
                
                # 获取元素唯一标识（简单对比，防止重复打印）
                current_ptr = ctypes.cast(element, ctypes.c_void_p).value
                
                if current_ptr != last_element_ptr:
                    # 3. 提取属性 (这些都是原生 COM 属性)
                    name = element.CurrentName
                    type_id = element.CurrentControlType
                    class_name = element.CurrentClassName
                    pid = element.CurrentProcessId
                    
                    print(f"\n[ 侦察到控件 ]")
                    print(f"名称: {name}")
                    print(f"类名: {class_name}")
                    print(f"PID: {pid}")
                    
                    last_element_ptr = current_ptr
            except:
                pass # 忽略某些无法获取元素的区域（如系统受限区域）
                
            time.sleep(0.2)
    except KeyboardInterrupt:
        print("\n侦察已停止。")

if __name__ == "__main__":
    start_native_uia_spy()
