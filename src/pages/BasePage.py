from flet_core import UserControl

from src.dao.DataManager import DataManager


class BasePage(UserControl):
    def __init__(self):
        super().__init__()
        self.configs = DataManager.configs
