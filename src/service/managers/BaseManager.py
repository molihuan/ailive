from src.dao.DataManager import DataManager


class BaseManager():
    # 全局管理者
    generalManager = None

    def __init__(self):
        self.configs = DataManager.configs

    @classmethod
    def setGeneralManager(cls, generalManager):
        cls.generalManager = generalManager
