from queue import Queue

from pydantic import BaseModel

from src.dao.OptionEnum import MsgType


class AskQueueItem(BaseModel):
    # 问题文本
    text:str
    # 是否还有用(用于判断存放temp文件夹下的路径)
    useful:bool=False
    # 类型
    msgType:MsgType=MsgType.DANMAKU
    # 用户姓名
    userName:str='root'

# 大语言模型
class BaseLLM():
    def init(self,model=None):
        pass
    def ask(self,content:str):
        pass
    def askByQueue(self,askQueue:Queue,audioCompoundQueue:Queue):
        pass

