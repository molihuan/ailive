from queue import Queue

from src.service.idle.IdleTaskManager import IdleTaskManager
from src.service.llm.AnythingLLM import AnythingLLM
from src.service.llm.BaseLLM import BaseLLM
from src.service.llm.OllamaLLM import OllamaLLM
from src.service.managers.BaseManager import BaseManager

from src.service.player.BaseAudioPlayer import BaseAudioPlayer
from src.service.player.PygameAudioPlayer import PygameAudioPlayer
from src.service.tts.BaseTTS import BaseTTS

from src.service.tts.GPTSoVITSTTS import GPTSoVITSTTS

from src.utils.ThreadUtils import SuperThread


# 总管理者
class GeneralManager(BaseManager):

    def __init__(self):
        super().__init__()
        # 初始化llm、tts、音频播放器
        self.llm: BaseLLM = AnythingLLM()
        self.tts: BaseTTS = GPTSoVITSTTS()
        self.audioPlayer: BaseAudioPlayer = PygameAudioPlayer()
        self.llm.init()
        self.tts.init()
        self.audioPlayer.init()

        # 问题队列
        self.askQueue = Queue()
        # 音频合成队列
        self.audioCompoundQueue = Queue()
        # 音频播放队列
        self.audioPlayQueue = Queue()

        # 设置自己为全局管理者
        BaseManager.setGeneralManager(self)
        # 开启线程
        self.startAllThread()

        # 开启直播弹幕监听

    def startAllThread(self):
        # 获取答案线程
        self.getAnswerThread = SuperThread(target=self.llm.askByQueue, args=(self.askQueue, self.audioCompoundQueue,))
        self.getAnswerThread.start()
        # 文本转语音线程
        self.text2audioThread = SuperThread(target=self.tts.text2audioByQueue,
                                            args=(self.audioCompoundQueue, self.audioPlayQueue,))
        self.text2audioThread.start()
        # 音频播放线程
        self.audioPlayThread = SuperThread(target=self.audioPlayer.playByQueue, args=(self.audioPlayQueue,))
        self.audioPlayThread.start()

        # 开启闲时任务
        self.idleTaskManager = IdleTaskManager()
        self.idleTaskManager.startIdleTaskThread()
