from rich.live import Live
from rich.console import Console
import win32gui
import win32process
import psutil

console = Console()


class GlimpseUI:

    def __init__(self):
        # 初始化时显示占位文本
        self.live = Live("等待更新窗口信息...", console=console, refresh_per_second=10)
        self.live.start()

    def render(self, hwnd):
        pid = win32process.GetWindowThreadProcessId(hwnd)[1]

        return f"""
[green]标题[/green]: [yellow]{win32gui.GetWindowText(hwnd)}[/yellow]
[green]句柄[/green]: {hwnd}
[green]类名[/green]：[yellow]{win32gui.GetClassName(hwnd)}[/yellow]
[green]PID[/green]: {pid}
[green]应用[/green]：[yellow]{psutil.Process(pid).name()}[/yellow]
"""

    def update(self, hwnd):
        self.live.update(self.render(hwnd))

    def stop(self):
        self.live.stop()


if __name__ == "__main__":
    ui = GlimpseUI()

    ui.update(123456)

    ui.stop()
