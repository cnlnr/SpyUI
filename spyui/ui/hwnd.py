from rich.live import Live
from rich.console import Console
import win32gui
import win32process
import psutil

console = Console()


class GlimpseUI:

    def __init__(self):
        # 初始化时显示占位文本
        self.live = Live("信息加载中...", console=console, refresh_per_second=10)
        self.live.start()

    def render(self, hwnd):
        pid = win32process.GetWindowThreadProcessId(hwnd)[1]

        return f"""
[green]标题[/green]: [yellow]{win32gui.GetWindowText(hwnd)}[/yellow]
[green]句柄[/green]: {hwnd} ({hex(hwnd)})
[green]类名[/green]：{win32gui.GetClassName(hwnd)}

[green]应用[/green]：[yellow]{psutil.Process(pid).name()}[/yellow]
[green]进程[/green]: {pid}
[green]线程[/green]: {win32process.GetWindowThreadProcessId(hwnd)[0]}
[green]路径[/green]: {psutil.Process(pid).exe()}

按住 Ctrl 停止，回车后退出
"""

    def update(self, hwnd):
        self.live.update(self.render(hwnd))

    def stop(self):
        self.live.stop()


def info(hwnd):
    pid = win32process.GetWindowThreadProcessId(hwnd)[1]
    console.clear()
    console.print(f"""
ⓘ 详细信息

[green]标题[/green]: [yellow]{win32gui.GetWindowText(hwnd)}[/yellow]
[green]句柄[/green]: {hwnd} ({hex(hwnd)})
[green]类名[/green]：{win32gui.GetClassName(hwnd)}

[green]应用[/green]：[yellow]{psutil.Process(pid).name()}[/yellow]
[green]进程[/green]: {pid}
[green]线程[/green]: {win32process.GetWindowThreadProcessId(hwnd)[0]}
[green]路径[/green]: {psutil.Process(pid).exe()}
""")

import os

def cls():
    # Windows 下这个命令会重置缓冲区，滚动条会消失
    os.system('cls') 


if __name__ == "__main__":
    ui = GlimpseUI()

    ui.update(123456)

    ui.stop()
