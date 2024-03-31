from datetime import datetime
import logging
import logging.config

import yaml

from src.utils.LogUtils import LogUtils

loggingConfigPath = r'E:\DesktopSpace\Development\Python\ailive\logging.yaml'

# 获取当前日期
current_date = datetime.now().strftime("%Y-%m-%d")

with open(loggingConfigPath) as yaml_file:
	config_dict = yaml.load(yaml_file, Loader=yaml.FullLoader)

config_dict['handlers']['fileHandler']['filename'] = config_dict['handlers']['fileHandler']['filename'].format(date=current_date)

logging.config.dictConfig(config_dict)


logging.debug('debug message')


if __name__ == '__main__':
	LogUtils.init()
	LogUtils.i("777")
