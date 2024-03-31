import logging
from datetime import datetime
import logging.config
import yaml


class LogUtils():
    logger: logging.Logger

    @classmethod
    def init(cls,loggingConfigPath = r'E:\DesktopSpace\Development\Python\ailive\logging.yaml'):

        # 获取当前日期
        current_date = datetime.now().strftime("%Y-%m-%d")

        with open(loggingConfigPath) as yaml_file:
            config_dict = yaml.load(yaml_file, Loader=yaml.FullLoader)

        config_dict['handlers']['fileHandler']['filename'] = config_dict['handlers']['fileHandler']['filename'].format(
            date=current_date)

        logging.config.dictConfig(config_dict)

        cls.logger=logging.getLogger()

        cls.i("日志正常启动...")

    @classmethod
    def i(cls,msg):
        cls.logger.info(msg)
    @classmethod
    def d(cls,msg):
        cls.logger.debug(msg)
    @classmethod
    def w(cls,msg):
        cls.logger.warning(msg)
    @classmethod
    def e(cls,msg):
        cls.logger.error(msg)

