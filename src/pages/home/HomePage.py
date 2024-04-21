from flet_core import UserControl, Page, Container, Column, ElevatedButton, ScrollMode, MainAxisAlignment, TextField, \
    Ref, Row

from src.pages.BasePage import BasePage
from src.pages.route.RouteUrl import RouteUrl
from src.service.ServiceManager import ServiceManager
from src.service.danmaku.BaseDanmaku import BaseDanmaku
from src.service.danmaku.DouyinBarrageGrabDK import DouyinBarrageGrabDK
from src.service.danmaku.DouyinLiveWebFetcherDK import DouyinLiveWebFetcherDK
from src.service.llm.BaseLLM import AskQueueItem
from src.utils.LogUtils import LogUtils


class HomePage(BasePage):
    def __init__(self, parent: Page):
        super().__init__()
        self.douyinDanmaku = None
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
                    Row([
                        ElevatedButton(text="直播间设置",
                                       on_click=lambda _: self.parent.go(RouteUrl.PAGE_LIVE_ROOM)),
                        ElevatedButton(text="大语言模型",
                                       on_click=lambda _: self.parent.go(RouteUrl.PAGE_LLM)),
                        ElevatedButton(text="文字转语音",
                                       on_click=lambda _: self.parent.go(RouteUrl.PAGE_TTS)),
                        ElevatedButton(text="闲时任务",
                                       on_click=lambda _: self.parent.go(RouteUrl.PAGE_IDLE)),
                    ]),
                    Row([
                        # ElevatedButton(text="开启所有线程",
                        #                on_click=lambda _: ServiceManager.generalManager.startAllThread()),
                        ElevatedButton(text="获取弹幕",
                                       on_click=lambda _: self.startGetDanmaku()),
                        ElevatedButton(text="停止弹幕",
                                       on_click=lambda _: self.douyinDanmaku.stopGetDanmakuThread()),
                    ]),

                    Row([
                        TextField(
                            ref=self.askTF,
                            hint_text="",
                            width=self.parent.width / 2
                        ),
                        ElevatedButton(text="提问",
                                       on_click=lambda _: self.tv(self.askTF.current.value)),
                    ]),

                ],
                auto_scroll=True,
                scroll=ScrollMode.ALWAYS,
                alignment=MainAxisAlignment.CENTER
            ),
        )

    def startGetDanmaku(self):
        # 梦幻西游表弟：655127452297
        # 花花皮匠：507700023202
        # 可乐男鞋3：950658833853
        # 公牛氏邸男鞋旗舰店：91425433198
        LogUtils.d(f"抖音直播间号:{self.configs.douyinLiveRoomNumber}")
        self.douyinDanmaku: BaseDanmaku = DouyinLiveWebFetcherDK(self.configs.douyinLiveRoomNumber)
        self.douyinDanmaku.startGetDanmakuThread()
        pass

    def tv(self, qtext: str):
        ask_queue = ServiceManager.generalManager.askQueue
        item = AskQueueItem(text=qtext)
        ask_queue.put(item)
        pass
