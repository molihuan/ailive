from flet import View, Page

from flet_core import AppBar, Text, colors, ElevatedButton, ScrollMode, IconButton, icons

from src.pages.home.HomePage import HomePage
from src.pages.home.HomePopupMenu import HomePopupMenu
from src.pages.idle.IdlePage import IdlePage
from src.pages.llm.LLMPage import LLMPage
from src.pages.route.RouteUrl import RouteUrl
from src.pages.settings.SettingsPage import SettingsPage
from src.pages.tts.TTSPage import TTSPage
from src.utils.CommonUtils import CommonUtils


class AppRoutes():

    def __init__(self, page: Page):
        self.page = page

    def view_pop(self, view):
        # 移除最上层的视图
        self.page.views.pop()
        top_view = self.page.views[-1]
        # 显示最上层视图
        self.page.go(top_view.route)

    def route_change(self, route):
        self.page.views.clear()

        # 默认页面
        self.page.views.append(
            View(
                "/",
                [
                    HomePage(self.page),
                ],
                scroll=ScrollMode.AUTO,
                appbar=AppBar(
                    # leading=ft.Image(src=f"/imgs/ml.png"),
                    # leading_width=40,
                    title=Text(f"无人直播工具"),
                    center_title=False,
                    bgcolor=colors.SURFACE_VARIANT,
                    actions=[
                        IconButton(icons.WB_SUNNY_OUTLINED,
                                   on_click=lambda _: CommonUtils.showAlertDialog("你干嘛~~哎呦~~")),
                        HomePopupMenu(self.page),
                    ],
                )
            )
        )

        if self.page.route == RouteUrl.PAGE_SETTINGS:
            self.page.views.append(
                View(
                    RouteUrl.PAGE_SETTINGS,
                    [
                        AppBar(title=Text("设置"), bgcolor=colors.SURFACE_VARIANT),
                        SettingsPage(self.page),
                    ],
                    scroll=ScrollMode.AUTO,
                )
            )
        elif self.page.route == RouteUrl.PAGE_LLM:
            self.page.views.append(
                View(
                    RouteUrl.PAGE_LLM,
                    [
                        AppBar(title=Text("大语言模型"), bgcolor=colors.SURFACE_VARIANT),
                        LLMPage(self.page)
                    ],
                    scroll=ScrollMode.AUTO,
                )
            )
        elif self.page.route == RouteUrl.PAGE_TTS:
            self.page.views.append(
                View(
                    RouteUrl.PAGE_TTS,
                    [
                        AppBar(title=Text("文字转语音"), bgcolor=colors.SURFACE_VARIANT),
                        TTSPage(self.page)
                    ],
                    scroll=ScrollMode.AUTO,
                )
            )
        elif self.page.route == RouteUrl.PAGE_IDLE:
            self.page.views.append(
                View(
                    RouteUrl.PAGE_IDLE,
                    [
                        AppBar(title=Text("闲时任务"), bgcolor=colors.SURFACE_VARIANT),
                        IdlePage(self.page)
                    ],
                    scroll=ScrollMode.AUTO,
                )
            )

        self.page.update()
