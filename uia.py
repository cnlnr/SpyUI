import mouse_uia
import ctypes
import time
import ui.highlighting as highlighting

# 初始化红框
highlighter = highlighting.HighlightOverlay(color="green", thickness=2)

last_id = None

while True:
    try:
        # 1. 获取鼠标坐标并获取 UIA 元素
        pt = ctypes.wintypes.POINT()
        ctypes.windll.user32.GetCursorPos(ctypes.byref(pt))
        el = mouse_uia.ElementFromPoint(pt)
        
        if el:
            # 2. 获取唯一 ID 并进行去重判断
            uid = el.GetRuntimeId()
            
            if uid != last_id:
                # 3. 提取属性 (ID 变了才打印和绘图)
                name = el.CurrentName or "无名称"
                cls = el.CurrentClassName
                # 获取 UIA 矩形对象
                rect = el.CurrentBoundingRectangle 
                
                print(f"ID: {uid} | 名称: {name} | 类名: {cls}")
                
                # 4. 更新红框位置 (使用 UIA 矩形的四个边界值)
                highlighter.draw_rect(rect.left, rect.top, rect.right, rect.bottom)
                
                last_id = uid  # 更新缓存
        else:
            # 如果没拿到元素，重置状态并隐藏框
            if last_id is not None:
                highlighter.close()
                last_id = None
                
    except Exception:
        # 捕获异常（如划过系统受限区域），静默重置
        if last_id is not None:
            highlighter.close()
            last_id = None
        pass
        
    time.sleep(0.1)
