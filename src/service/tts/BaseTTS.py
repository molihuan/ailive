from queue import Queue

from pydantic import BaseModel

# 音频合成队列的item
from src.dao.OptionEnum import MsgType


class AudioCompoundQueueItem(BaseModel):
    # 是否还有用(用于判断存放temp文件夹下的路径)
    useful:bool
    text:str
    # 准备存放音频的路径
    audioPath:str
    # 类型
    msgType:MsgType=MsgType.DANMAKU
    # 用户姓名
    userName:str='root'

# 音频播放队列的item
class AudioPlayQueueItem(BaseModel):
    # 是否还有用(用于判断存放temp文件夹下的路径)
    useful:bool
    # 音频生成的路径
    audioPath:str
    # 类型
    msgType:MsgType=MsgType.DANMAKU
    # 用户姓名
    userName:str='root'


class BaseTTS():
    def init(self):
        pass
    def text2audio(self,text:str,audio_path:str):

        pass
    def text2audioByQueue(self,audioCompoundQueue:Queue,audioPlayQueue:Queue):

        pass
    # 过滤违禁词
    def doFilter(self,text:str):
        pass