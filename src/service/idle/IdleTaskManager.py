# 空闲任务管理者
import threading
import time
import uuid
import math
from queue import Queue

from src.dao.OptionEnum import MsgType
from src.service.managers.BaseManager import BaseManager
from src.service.player.BaseAudioPlayer import BaseAudioPlayer

from src.service.tts.BaseTTS import AudioCompoundQueueItem, AudioPlayQueueItem
from src.utils.CommonUtils import CommonUtils
from src.utils.FileUtils import FileUtils
from src.utils.LogUtils import LogUtils
from src.utils.ThreadUtils import SuperThread


class IdleTaskManager(BaseManager):
    # 全局闲时时间
    globalIdleTime: int = 0
    # 停止做闲时任务的标志位,并不是停止闲时线程,一定要用IdleTaskManager.stopDoAudioIdleTaskFlag,不能用self.stopDoAudioIdleTaskFlag
    stopDoAudioIdleTaskFlag: bool = False
    stopDoTextIdleTaskFlag: bool = False

    def __init__(self):
        super().__init__()
        # 限制时间
        self.limitIdleTime = self.configs.limitIdleTime
        self.idleTextList = self.configs.idleTextList
        self.idleAudioList = self.configs.idleAudioList
        # 音频播放进度
        self.savePlayPos = 0
        # 保存的音频列表索引
        self.saveListIndex = 0

    @staticmethod
    def makeGlobalIdleTimeZero():
        IdleTaskManager.globalIdleTime = 0

    # 文字闲时任务
    def textIdleTaskThread(self):
        audioCompoundQueue = self.generalManager.audioCompoundQueue
        # 运行闲时线程
        while True:
            if IdleTaskManager.globalIdleTime > self.limitIdleTime:
                LogUtils.d(f'闲时时间超过规定')
                # 做闲时任务
                for index, idleText in enumerate(self.idleTextList):
                    if index < self.saveListIndex:
                        # 移动到保存的索引位置
                        continue
                    # 队列中不需要添加太多任务,如果超过最大的数就开始等待
                    if self.judgeStopDoTextIdleTask(audioCompoundQueue, 0):
                        break

                    # 设置准备生成音频的路径
                    temp_audio_name = str(uuid.uuid4()) + '.wav'

                    if True:
                        temp_audio_path = FileUtils.fileInTempUsefulPath(temp_audio_name)
                    else:
                        temp_audio_path = FileUtils.fileInTempUselessPath(temp_audio_name)

                    item = AudioCompoundQueueItem(text=idleText, audioPath=temp_audio_path, msgType=MsgType.IDLE,
                                                  startPlayPos=self.savePlayPos,
                                                  idleDataListIndex=index)
                    LogUtils.w(f'合成队列+:{idleText}')
                    audioCompoundQueue.put(item)
                    # 播放位置复位
                    self.savePlayPos = 0
                    self.saveListIndex = 0
            else:
                time.sleep(1)
                IdleTaskManager.globalIdleTime += 1

    # 判断是否需要停止做文本闲时任务
    def judgeStopDoTextIdleTask(self, queue: Queue, size: int):
        # 退出的条件是前一个任务已经完成,返回False
        # 还有一种是其他的线程更改了IdleTaskManager.stopDoAudioIdleTaskFlag为True,返回True
        # 队列中不需要添加太多任务,如果超过就开始等待
        while queue.qsize() > size:

            # LogUtils.d(f'闲时任务队列中任务太多,开始等待已经运行的任务结束')
            if IdleTaskManager.stopDoTextIdleTaskFlag:
                # 停止做闲时任务,并没有停止闲时线程
                IdleTaskManager.stopDoTextIdleTaskFlag = False
                IdleTaskManager.makeGlobalIdleTimeZero()
                # 清空队列只留下自己
                CommonUtils.clearQueueOneLeft(queue)
                CommonUtils.clearQueue(self.generalManager.audioPlayQueue)
                # 停止正在文字转音频网络请求
                # print(f'needResults：{self.generalManager.tts.needResults}')
                self.generalManager.tts.setNeedResults(False)

                # 停止音频
                player: BaseAudioPlayer = self.generalManager.audioPlayer
                self.savePlayPos = player.getProgress()
                # self.saveListIndex = player.getIdleDataListIndex() - self.saveListIndex
                self.saveListIndex = player.getIdleDataListIndex()
                player.stop()

                LogUtils.d(f'停止做闲时任务')
                return True
            else:
                time.sleep(1)

        return False

    # 音频闲时任务
    def audioIdleTaskThread(self):
        audioPlayQueue: Queue = self.generalManager.audioPlayQueue
        # 运行闲时线程
        while True:
            if IdleTaskManager.globalIdleTime > self.limitIdleTime:
                LogUtils.d(f'闲时时间超过规定')

                # 做闲时任务
                for index, idleAudio in enumerate(self.idleAudioList):
                    if index < self.saveListIndex:
                        # 移动到保存的索引位置
                        continue
                    # 队列中不需要添加太多任务,如果超过0就开始等待
                    if self.judgeStopDoAudioIdleTask(audioPlayQueue, 0):
                        # 有弹幕就直接退出做闲时任务
                        break

                    item = AudioPlayQueueItem(audioPath=idleAudio, msgType=MsgType.IDLE, startPlayPos=self.savePlayPos,
                                              idleDataListIndex=index)
                    LogUtils.e(f'播放队列+,播放起始位置{self.savePlayPos},{idleAudio}')
                    audioPlayQueue.put(item)
                    # 播放位置复位
                    self.savePlayPos = 0
                    self.saveListIndex = 0
            else:
                time.sleep(1)
                IdleTaskManager.globalIdleTime += 1

    # 判断是否需要停止做音频闲时任务
    def judgeStopDoAudioIdleTask(self, queue: Queue, size: int):
        # 退出的条件是前一个任务已经完成,返回False
        # 还有一种是其他的线程更改了IdleTaskManager.stopDoAudioIdleTaskFlag为True,返回True
        # 队列中不需要添加太多任务,如果超过就开始等待
        while queue.qsize() > size:

            # LogUtils.d(f'闲时任务队列中任务太多,开始等待已经运行的任务结束')
            if IdleTaskManager.stopDoAudioIdleTaskFlag:
                # 停止做闲时任务,并没有停止闲时线程
                IdleTaskManager.stopDoAudioIdleTaskFlag = False
                IdleTaskManager.makeGlobalIdleTimeZero()
                # 清空队列只留下自己
                CommonUtils.clearQueueOneLeft(queue)
                # 停止音频
                player: BaseAudioPlayer = self.generalManager.audioPlayer
                self.savePlayPos = player.getProgress()
                print(f'保存播放进度为:{self.savePlayPos}')
                self.saveListIndex = player.getIdleDataListIndex()
                player.stop()

                LogUtils.d(f'停止做闲时任务')
                return True
            else:
                time.sleep(1)

        return False

    # 开启闲时任务线程
    def startIdleTaskThread(self):

        if self.configs.idleAudioEnable:
            audioIdleThread = SuperThread(target=self.audioIdleTaskThread)
            audioIdleThread.start()
        elif self.configs.idleTextEnable:
            textIdleThread = SuperThread(target=self.textIdleTaskThread)
            textIdleThread.start()
        else:
            LogUtils.d(f'闲时任务未开启')
            return
        LogUtils.d(f'开始闲时线程,规定闲时时间为:{self.configs.limitIdleTime}s')

    # 停止闲时任务线程
    def stopIdleTaskThread(self):
        pass
