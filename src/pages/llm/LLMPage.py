from flet_core import UserControl, Page, Container, Column, ElevatedButton, ScrollMode, MainAxisAlignment, alignment, \
    Ref, ControlEvent

from src.dao.DataManager import DataManager
from src.pages.BasePage import BasePage


class LLMPage(BasePage):
    def __init__(self, parent: Page):
        super().__init__()
        self.parent = parent
        self.btn_reset_configs = Ref[ElevatedButton]()

    def initData(self):
        self.page.update()
        pass

    def did_mount(self):
        # 挂载后调用
        self.initData()
        pass

    def btn_click(self, e: ControlEvent):
        view = e.control
        if view == self.btn_reset_configs.current:
            pass

    def build(self):
        return Container(
            content=Column([
                ElevatedButton(ref=self.btn_reset_configs, text='恢复默认', on_click=self.btn_click)
            ],
                scroll=ScrollMode.ALWAYS,
                alignment=MainAxisAlignment.CENTER
            ),
            alignment=alignment.center

        )
