import threading
import time
from queue import Queue

import pygame

from src.service.player.BaseAudioPlayer import BaseAudioPlayer

# pygame播放器
from src.service.tts.BaseTTS import AudioPlayQueueItem
from src.utils.LogUtils import LogUtils


class PygameAudioPlayer(BaseAudioPlayer):

    def init(self):
        self.mixer = pygame.mixer
        self.mixer.init()# 初始化音频模块
        self.audioPlayer = self.mixer.music


    # 播放
    def play(self,file_path:str, start=0,loops=0, fade_ms=0):
        self.audioPlayer.load(file_path)
        self.audioPlayer.play(loops,start,fade_ms)
        while self.audioPlayer.get_busy():
            # pygame.time.Clock().tick(10)
            pass
    # 播放
    def playByQueue(self,audioPlayQueue:Queue):
        while True:
            audioPlayQueueItem:AudioPlayQueueItem = audioPlayQueue.get()
            self.play(audioPlayQueueItem.audioPath)
            LogUtils.d(f'播放完成:{audioPlayQueueItem.audioPath}')
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

        pass

    def setProgress(self,pos):
        self.audioPlayer.set_pos(pos)
        pass

    def getProgress(self):
        return self.audioPlayer.get_pos()/1000


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