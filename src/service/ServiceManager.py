import sys

from flet_core import Page, AlertDialog, Text, ElevatedButton, OutlinedButton, MainAxisAlignment

from src.service.managers.GeneralManager import GeneralManager

# 业务管理者
from src.utils.CommonUtils import CommonUtils


class ServiceManager():
    generalManager: GeneralManager
    page: Page

    @classmethod
    def init(cls, page: Page):
        cls.page = page
        cls.generalManager = GeneralManager()

        page.window_prevent_close = True
        page.on_window_event = cls.window_event

    @classmethod
    def window_event(cls, e):
        if e.data == "close":
            CommonUtils.showAlertDialog("你确定要关闭软件吗?",
                                        actions=[
                                            ElevatedButton('确定', on_click=lambda e: cls.closeDialogYesClick()),
                                            ElevatedButton("取消", on_click=lambda e: cls.closeDialogNoClick())
                                        ])
            cls.page.update()

    @classmethod
    def closeDialogYesClick(cls):
        # 停止所有的线程
        cls.generalManager.getAnswerThread.stop()
        cls.generalManager.text2audioThread.stop()
        cls.generalManager.audioPlayThread.stop()
        # cls.generalManager.idleTaskManager.stopIdleTaskThread()

        cls.page.window_destroy()
        sys.exit()

    @classmethod
    def closeDialogNoClick(cls):
        CommonUtils.closeAlertDialog()
