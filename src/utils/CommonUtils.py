from queue import Queue
from typing import List

from flet_core import MainAxisAlignment, Control, Text, Page, SnackBar, TextButton, AlertDialog, BottomSheet, Container, \
    Column


class CommonUtils():
    page: Page = None

    @classmethod
    def init(cls, page: Page):
        CommonUtils.page = page

    @classmethod
    def showSnack(cls, text: str, actionText='提示'):
        if cls.page.snack_bar is None:
            cls.page.snack_bar = SnackBar(
                content=Text("Hello, world!"),
                action=actionText,
            )
        cls.page.snack_bar.content = Text(text)
        cls.page.snack_bar.open = True
        cls.page.update()

    @classmethod
    def showAlertDialog(cls, contentStr: str = '内容', actions: List[Control] = None, content: Control = None,
                        title=None, titleStr='提示', ):
        if content is None:
            content = Text(contentStr)
        if title is None:
            title = Text(titleStr)

        if actions is None:
            actions = [
                TextButton("确定", on_click=lambda p: CommonUtils.closeAlertDialog(cls.page.dialog)),
            ]

        cls.page.dialog = AlertDialog(
            modal=True,
            title=title,
            content=content,
            actions=actions,
            actions_alignment=MainAxisAlignment.END,
            on_dismiss=lambda e: print("dialog dismissed!"),
        )
        cls.page.dialog.open = True
        cls.page.update()

    @classmethod
    def closeAlertDialog(cls, dialog: AlertDialog):
        dialog.open = False
        cls.page.update()

    @classmethod
    def showBottomSheet(cls, widgetList: List[Control], title='提示', ):
        bs = BottomSheet(
            Container(
                Column(
                    controls=widgetList,
                    tight=True,
                    alignment=MainAxisAlignment.CENTER
                ),
                padding=10,
                width=cls.page.width,
            ),
            open=True,
        )
        cls.page.overlay.append(bs)
        bs.open = True
        cls.page.update()
        return bs

    @classmethod
    def closeBottomSheet(cls, bs: BottomSheet):
        bs.open = False
        cls.page.update()

    @staticmethod
    def clearQueue(queue: Queue):
        while not queue.empty():
            queue.get()

    @staticmethod
    def clearQueueOneLeft(queue: Queue):
        while not (queue.qsize() <= 1):
            queue.get()
