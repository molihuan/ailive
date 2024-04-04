from flet_core import UserControl, PopupMenuButton, PopupMenuItem, Page

# 主页弹出菜单
from src.pages.route.RouteUrl import RouteUrl


class HomePopupMenu(UserControl):
    def __init__(self, parent: Page):
        super().__init__()
        self.parent = parent

    def build(self):
        return PopupMenuButton(
            items=[
                PopupMenuItem(text="设置", on_click=lambda _: self.goSettingsPage()),
                # PopupMenuItem(),  # divider
            ]
        )

    def goSettingsPage(self):
        self.parent.go(RouteUrl.PAGE_SETTINGS)

    def did_mount(self):
        pass
