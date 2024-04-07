import time
from queue import Queue

import pygame

from src.dao.OptionEnum import MsgType
from src.service.idle.IdleTaskManager import IdleTaskManager
from src.service.player.BaseAudioPlayer import BaseAudioPlayer

from src.service.tts.BaseTTS import AudioPlayQueueItem
from src.utils.LogUtils import LogUtils


# pygame播放器
class PygameAudioPlayer(BaseAudioPlayer):

    def init(self):
        self.mixer = pygame.mixer
        self.mixer.init()  # 初始化音频模块
        self.audioPlayer = self.mixer.music
        # 已经播放的进度
        self.alreadyPlayPos = 0.0
        # 闲时任务数据列表的索引
        self.idleDataListIndex = -1

    def getIdleDataListIndex(self):
        return self.idleDataListIndex

    # 播放
    def play(self, file_path: str, msgType=None, start=0.0, loops=0, fade_ms=0):
        self.audioPlayer.load(file_path)
        self.audioPlayer.play(loops, start, fade_ms)
        while self.audioPlayer.get_busy():
            # pygame.time.Clock().tick
            if msgType == MsgType.DANMAKU:
                # 重置闲时时间,防止闲时任务提前进入
                IdleTaskManager.makeGlobalIdleTimeZero()
            time.sleep(1)

    # 播放
    def playByQueue(self, audioPlayQueue: Queue):
        while True:
            audioPlayQueueItem: AudioPlayQueueItem = audioPlayQueue.get()
            # 获取闲事任务的索引
            self.idleDataListIndex = audioPlayQueueItem.idleDataListIndex
            self.alreadyPlayPos = audioPlayQueueItem.startPlayPos
            # 播放
            self.play(audioPlayQueueItem.audioPath, audioPlayQueueItem.msgType, start=audioPlayQueueItem.startPlayPos)
            LogUtils.d(f'播放完成:{audioPlayQueueItem.audioPath}')
            
            # if audioPlayQueueItem.msgType == MsgType.DANMAKU:
            #     # 重置闲时时间
            #     IdleTaskManager.makeGlobalIdleTimeZero()

    # 暂停
    def pause(self):
        self.audioPlayer.pause()
        pass

    # 继续
    def resume(self):
        self.audioPlayer.unpause()
        pass

    # 停止
    def stop(self):
        self.audioPlayer.stop()
        pass

    def replay(self):
        self.audioPlayer.rewind()
        pass

    def setProgress(self, pos):
        self.audioPlayer.set_pos(pos)
        pass

    def getProgress(self):
        return (self.audioPlayer.get_pos() / 1000) + self.alreadyPlayPos

# if __name__ == '__main__':
#
#     t1 = r"E:\DesktopSpace\Development\Python\ailive\assets\t1.mp3"
#     t2 = r"E:\DesktopSpace\Development\Python\ailive\assets\t2.mp3"
#
#     player=PygameAudioPlayer()
#
#
#     thread1 = threading.Thread(target=player.play, args=(t1,))
#     thread1.start()
#
#     time.sleep(5)
#     savePos=player.getProgress()
#     print(savePos)
#
#     thread2 = threading.Thread(target=player.play, args=(t2,))
#     thread2.start()
#
#     time.sleep(5)
#
#     thread1 = threading.Thread(target=player.play, args=(t1,savePos))
#     thread1.start()
#
#     # time.sleep(13)
#     thread1.join()
