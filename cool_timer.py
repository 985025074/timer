from datetime import datetime
import time
from rich.layout import Layout
from rich.panel import Panel
from rich.live import Live
from rich.align import Align
from rich.padding import Padding
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from rich.text import Text
from pydub import AudioSegment
from pydub.playback import play
# settings:
achive_times = 0
focus_per_time = 1  # in minutes
focus_per_rest = 1   # in minutes

# 布局创建
def make_layout() -> Layout:
    layout = Layout(name="root", size=120)
    layout.split(
        Layout(name="clock", size=3),
        Layout(name="info"),
    )
    layout["info"].split_row(
        Layout(name="achievements", ratio=1),
        Layout(name="progress", ratio=5),
    )
    return layout

# 时钟组件
class Clock:
    def __rich__(self) -> Panel:
        time_text = Text.from_markup(datetime.now().ctime().replace(":", "[blink]:[/]"), justify="center")
        layout = Layout()
        layout.split_row(
            Layout(Align.center(time_text, vertical="middle"), ratio=4),
            Layout(Align.right("[b]Kokona Made[/b]", vertical="middle"), ratio=1)
        )
        return Panel(layout, style="white on blue")

# 成就组件
class Achievements:
    def __rich__(self):
        grid = Table(expand=True, title="Achievements")
        grid.add_column("Focus Times", justify="center", ratio=1)
        grid.add_row(str(achive_times), style="green")
        return Panel(grid)

# 进度组件
class FocusProgress:
    def __init__(self):
        self.progress = Progress(
            "{task.description}",
            SpinnerColumn(),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.00f}%"),
      
        )
        self.working_task = self.progress.add_task("[green]Working", total=focus_per_time * 60)
        self.resting_task = self.progress.add_task("[red]Resting", total=focus_per_rest * 60)

    def __rich__(self):
        return Panel(self.progress)

# 初始化 layout 和组件
layout = make_layout()
achive_component = Achievements()
progress_component = FocusProgress()
layout["clock"].update(Clock())
layout["achievements"].update(achive_component)
layout["progress"].update(progress_component)
layout = Layout(Padding(layout, (5, 10, 5, 10)))  # 添加外边距

# 主循环
rest = False
with Live(layout, refresh_per_second=1, screen=False):
    while True:
        # layout["clock"].update(Clock())
        # layout["achievements"].update(Achievements())  # 每次刷新都更新

        if rest:
            progress_component.progress.advance(progress_component.resting_task, 1)
            if progress_component.progress.tasks[progress_component.resting_task].finished:
                rest = False
                progress_component.progress.reset(progress_component.resting_task)
        else:
            progress_component.progress.advance(progress_component.working_task, 1)
            if progress_component.progress.tasks[progress_component.working_task].finished:
                rest = True
                achive_times += 1
                progress_component.progress.reset(progress_component.working_task)
                obj = AudioSegment.from_mp3("./alert.mp3")
                play(obj)

        time.sleep(1)
