from enum import Enum

from pydantic import BaseModel


class LivePlatform(Enum):
    BILIBILI = 1
    DOUYIN = 2

class LLMType(Enum):
    OLLAMA_LLM = 1

class TTSType(Enum):
    GPT_SOVITS = 1

class ConfigsModel(BaseModel):
    # 直播平台
    livePlatform:LivePlatform = LivePlatform.DOUYIN
    #是否需要本地问答
    needLocalQA:bool=True
    #本地问答库配置

    # LLM配置
    llmType:LLMType=LLMType.OLLAMA_LLM
    llmApiAddr:str = 'http://127.0.0.1:11434'
    llmModel:str = 'qwen:4b-chat'

    # TTS配置
    ttsType:TTSType=TTSType.GPT_SOVITS
    ttsApiAddr: str = 'http://127.0.0.1:9880'
    # 参考音频
    ttsReferWavPath:str = r'E:\DesktopSpace\Development\Python\GPT-SoVITS\audio\badXT\badXT_77.wav'
    # 参考音频文本
    ttsPromptText:str = r'其他都很完美，她确实是啊她，她这个人身材又不好脾气又差不知道为什么能当主播呢？'
    # 参考音频文本语言
    ttsPromptLanguage:str = 'zh'
    # 输入文本语言
    ttsTextLanguage:str = 'zh'

