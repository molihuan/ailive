from flet import Page

from src.models.configs.ConfigsModel import ConfigsModel, LivePlatform


# 数据管理者
class DataManager():
    page: Page = None
    configs: ConfigsModel = None

    @classmethod
    def setPage(cls, page: Page):
        cls.page = page

    @classmethod
    def init(cls):
        cls.configs = cls.getConfigs()
        if cls.configs is None:
            cls.configs = ConfigsModel()
            # cls.setConfigs(cls.configs)

    @classmethod
    def remove(cls, key):
        cls.page.client_storage.remove(key)

    @classmethod
    def resetConfigs(cls):
        cls.remove("MLH_AiLive_Configs")
        cls.init()

    @classmethod
    def saveConfigs(cls):
        return cls.page.client_storage.set("MLH_AiLive_Configs", cls.configs)

    @classmethod
    def setConfigs(cls, value: ConfigsModel):
        return cls.page.client_storage.set("MLH_AiLive_Configs", value)

    @classmethod
    def getConfigs(cls):
        value = cls.page.client_storage.get("MLH_AiLive_Configs")
        if value:
            # 重新转换为对象
            value = ConfigsModel(**value)
        return value
