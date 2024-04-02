from flet import Page

from src.models.configs.ConfigsModel import ConfigsModel, LivePlatform


# 数据管理者
class DataManager():
    page: Page = None
    configs: ConfigsModel = None

    @staticmethod
    def setPage(page: Page):
        DataManager.page = page

    @classmethod
    def init(cls):
        cls.configs = cls.getConfigs()
        if cls.configs is None:
            cls.configs = ConfigsModel()
            cls.configs.livePlatform = LivePlatform.DOUYIN
            cls.setConfigs(cls.configs)
            pass

    @staticmethod
    def setConfigs(value):
        return DataManager.page.client_storage.set("MLH_Configs", value)

    @staticmethod
    def getConfigs():
        value = DataManager.page.client_storage.get("MLH_Configs")
        return value
