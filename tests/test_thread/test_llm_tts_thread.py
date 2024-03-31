import threading
from queue import Queue

from src.service.llm.BaseLLM import BaseLLM, AskQueueItem
from src.service.llm.OllamaLLM import OllamaLLM
from src.service.player.BaseAudioPlayer import BaseAudioPlayer
from src.service.player.PygameAudioPlayer import PygameAudioPlayer
from src.service.tts.BaseTTS import BaseTTS
from src.service.tts.GPTSoVITSTTS import GPTSoVITSTTS

if __name__ == '__main__':

    llm: BaseLLM = OllamaLLM()

    refer_wav_path: str = r'E:\DesktopSpace\Development\Python\GPT-SoVITS\audio\badXT\badXT_77.wav'
    prompt_text: str = r'其他都很完美，她确实是啊她，她这个人身材又不好脾气又差不知道为什么能当主播呢？'

    tts: BaseTTS = GPTSoVITSTTS(refer_wav_path, prompt_text)
    audioPlayer: BaseAudioPlayer = PygameAudioPlayer()
    llm.init()
    tts.init()
    audioPlayer.init()


    askQueue = Queue()
    audioCompoundQueue = Queue()
    audioPlayQueue = Queue()
    item = AskQueueItem(text="你好")
    item.text = "你好"
    askQueue.put(item)

    getAnswerThread =threading.Thread(target=llm.askByQueue,args=(askQueue,audioCompoundQueue,))
    text2audioThread =threading.Thread(target=tts.text2audioByQueue,args=(audioCompoundQueue,audioPlayQueue,))
    audioPlayThread =threading.Thread(target=audioPlayer.playByQueue,args=(audioPlayQueue,))

    getAnswerThread.start()
    text2audioThread.start()
    audioPlayThread.start()

    getAnswerThread.join()
    text2audioThread.join()
    audioPlayThread.join()