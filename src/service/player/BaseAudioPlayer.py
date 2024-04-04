from queue import Queue


class BaseAudioPlayer():
    def init(self):
        pass

    def getIdleDataListIndex(self):
        pass

    # 播放
    def play(self, file_path: str):
        pass

    # 播放
    def playByQueue(self, audioPlayQueue: Queue):
        pass

    # 暂停
    def pause(self):
        pass

    # 继续
    def resume(self):
        pass

    # 停止
    def stop(self):
        pass

    def replay(self):
        pass

    def setProgress(self, pos):
        pass

    def getProgress(self):
        pass
