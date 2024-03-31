import threading
from queue import Queue

from src.service.llm.BaseLLM import BaseLLM, AskQueueItem
from src.service.llm.OllamaLLM import OllamaLLM
from src.service.player.BaseAudioPlayer import BaseAudioPlayer
from src.service.player.PygameAudioPlayer import PygameAudioPlayer
from src.service.tts.BaseTTS import BaseTTS


from src.service.tts.GPTSoVITSTTS import GPTSoVITSTTS

# 总管理者
class GeneralManager():
    def __init__(self):
        # 初始化llm、tts、音频播放器
        self.llm:BaseLLM = OllamaLLM()

        refer_wav_path: str = r'E:\DesktopSpace\Development\Python\GPT-SoVITS\audio\badXT\badXT_77.wav'
        prompt_text: str = r'其他都很完美，她确实是啊她，她这个人身材又不好脾气又差不知道为什么能当主播呢？'

        self.tts:BaseTTS = GPTSoVITSTTS(refer_wav_path,prompt_text)
        self.audioPlayer:BaseAudioPlayer = PygameAudioPlayer()
        self.llm.init()
        self.tts.init()
        self.audioPlayer.init()

        # 问题队列
        self.askQueue = Queue()
        # 音频合成队列
        self.audioCompoundQueue = Queue()
        #音频播放队列
        self.audioPlayQueue = Queue()

        # 输入数据
        item = AskQueueItem(text="你好")
        item.text = "你好"
        self.askQueue.put(item)

        # 开启闲时任务

        # 开启直播弹幕监听
    def startThread(self):
        # 获取答案线程
        getAnswerThread = threading.Thread(target=self.llm.askByQueue, args=(self.askQueue, self.audioCompoundQueue,))
        getAnswerThread.start()
        # 文本转语音线程
        text2audioThread = threading.Thread(target=self.tts.text2audioByQueue, args=(self.audioCompoundQueue, self.audioPlayQueue,))
        text2audioThread.start()
        # 音频播放线程
        audioPlayThread = threading.Thread(target=self.audioPlayer.playByQueue, args=(self.audioPlayQueue,))
        audioPlayThread.start()
