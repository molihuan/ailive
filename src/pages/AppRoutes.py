import socket

from flet import View, Page

from flet_core import AppBar, Text, colors, ElevatedButton, ScrollMode, IconButton, icons

from src.pages.home.HomePage import HomePage
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
                                      on_click=lambda _: CommonUtils.showAlertDialog( "你干嘛~~哎呦~~")),
                        # HomePopupMenu(self.page),
                    ],
                )
            )
        )
        if self.page.route == "/setting":
            self.page.views.append(
                View(
                    "/setting",
                    [
                        AppBar(title=Text("设置"), bgcolor=colors.SURFACE_VARIANT),
                        ElevatedButton("返回首页", on_click=lambda _: self.page.go("/")),
                    ],
                    scroll=ScrollMode.AUTO,
                )
            )
        elif self.page.route == "/quick_facebook_account":
            self.page.views.append(
                View(
                    "/quick_facebook_account",
                    [
                        AppBar(title=Text("速拿二解号"), bgcolor=colors.SURFACE_VARIANT),
                        # QuickFacebookAccountPage(self.page)
                    ],
                    scroll=ScrollMode.AUTO,
                )
            )
        self.page.update()
