from flet_core import UserControl, Page, Container, Column, ElevatedButton, ScrollMode, MainAxisAlignment, TextField, \
    Ref

from src.service.ServiceManager import ServiceManager
from src.service.danmaku.DouyinDanmaku import DouyinDanmaku
from src.service.llm.BaseLLM import AskQueueItem
from src.utils.CommonUtils import CommonUtils
from src.utils.LogUtils import LogUtils


class HomePage(UserControl):
    def __init__(self, parent: Page):
        super().__init__()
        self.parent = parent
        self.askTF = Ref[TextField]()

    def initData(self):
        pass

    def did_mount(self):
        self.initData()


    def build(self):
        return Container(
            content=Column(
                [
                    ElevatedButton(text="开启监听",
                                   on_click=lambda _: ServiceManager.generalManager.startThread()),
                    ElevatedButton(text="获取弹幕",
                                   on_click=lambda _: DouyinDanmaku().startGetDanmaku()),
                    TextField(
                        ref=self.askTF,
                        hint_text="",
                        width=self.parent.width / 2
                    ),
                    ElevatedButton(text="提问",
                                      on_click=lambda _: self.tv(self.askTF.current.value)),
                ],
                auto_scroll=True,
                scroll=ScrollMode.ALWAYS,
                alignment=MainAxisAlignment.CENTER
            ),
        )

    def tv(self,qtext:str):
        ask_queue = ServiceManager.generalManager.askQueue
        item = AskQueueItem(text=qtext)
        ask_queue.put(item)
        LogUtils.d(qtext)
        pass
