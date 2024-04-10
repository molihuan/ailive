from queue import Queue

from pydantic import BaseModel

from src.dao.DataManager import DataManager
from src.dao.OptionEnum import MsgType
from src.utils.CommonUtils import CommonUtils


class AskQueueItem(BaseModel):
    # 问题文本
    text: str
    # 是否还有用(用于判断存放temp文件夹下的路径)
    useful: bool = False
    # 类型
    msgType: MsgType = MsgType.DANMAKU
    # 用户姓名
    userName: str = 'root'


# 大语言模型
class BaseLLM():
    def __init__(self):
        self.configs = DataManager.configs

    def init(self):
        pass

    # 处理回答后的文本
    def handleAnswerText(self, answerText: str):
        # 空数据结束
        if answerText == "" or answerText is None:
            return None
        # 去除两端空格
        answerText = answerText.strip()

        # 是否有链接
        if CommonUtils.is_url_check(answerText):
            return None
        
    def ask(self, content: str):
        pass

    def askByQueue(self, askQueue: Queue, audioCompoundQueue: Queue):
        pass
