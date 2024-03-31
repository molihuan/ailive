from src.service.managers.GeneralManager import GeneralManager

# 业务管理者
class ServiceManager():
    generalManager:GeneralManager
    @classmethod
    def init(cls):
        cls.generalManager=GeneralManager()
