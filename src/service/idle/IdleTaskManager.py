# 空闲任务管理者
import threading
import uuid

from src.dao.DataManager import DataManager
from src.models.configs.ConfigsModel import IdleType
from src.service.ServiceManager import ServiceManager
from src.service.llm.BaseLLM import AskQueueItem
from src.service.tts.BaseTTS import AudioCompoundQueueItem, AudioPlayQueueItem
from src.utils.FileUtils import FileUtils
from src.utils.ThreadUtils import SuperThread


class IdleTaskManager():
    def init(self):
        # 时间
        self.limitIdleTime = DataManager.configs.limitIdleTime
        self.globalIdleTime = 0
        self.stopFlag = False
        pass

    # 文字闲时任务
    def textIdleTaskThread(self):
        idleTextList = []
        # 运行闲时线程
        while True:
            if self.globalIdleTime > self.limitIdleTime:
                # 做闲时任务
                for idleText in idleTextList:
                    if self.stopFlag:
                        # 停止做闲时任务,并没有停止闲时线程
                        break
                    # 设置准备生成音频的路径
                    temp_audio_name = str(uuid.uuid4()) + '.wav'

                    if False:
                        temp_audio_path = FileUtils.fileInTempUsefulPath(temp_audio_name)
                    else:
                        temp_audio_path = FileUtils.fileInTempUselessPath(temp_audio_name)

                    audioCompoundQueue = ServiceManager.generalManager.audioCompoundQueue
                    item = AudioCompoundQueueItem(text=idleText, audioPath=temp_audio_path)
                    audioCompoundQueue.put(item)

    # 音频闲时任务
    def audioIdleTaskThread(self):
        idleAudioList = []

        # 运行闲时线程
        while True:
            if self.globalIdleTime > self.limitIdleTime:
                # 做闲时任务
                for idleAudio in idleAudioList:
                    if self.stopFlag:
                        # 停止做闲时任务,并没有停止闲时线程
                        break
                    audioPlayQueue = ServiceManager.generalManager.audioPlayQueue
                    item = AudioPlayQueueItem(audioPath=idleAudio)
                    audioPlayQueue.put(item)

    # 开启闲时任务
    def startIdleTask(self):

        idleType = DataManager.configs.idleType

        if idleType == IdleType.AUDIO:
            audioIdleThread = SuperThread(target=self.audioIdleTaskThread)
            audioIdleThread.start()
        elif idleType == IdleType.TEXT:
            textIdleThread = SuperThread(target=self.textIdleTaskThread)
            textIdleThread.start()

    def stopIdleTask(self):
        pass
