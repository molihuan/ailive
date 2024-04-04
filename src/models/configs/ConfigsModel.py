from enum import Enum
from typing import List

from pydantic import BaseModel


# 直播平台
class LivePlatform(Enum):
    BILIBILI = 1
    DOUYIN = 2


# 大语言模型
class LLMType(Enum):
    # 复读机
    REPEATER = 1
    OLLAMA_LLM = 2


# 文本转语音
class TTSType(Enum):
    GPT_SOVITS = 1


# 闲时任务
# class IdleType(Enum):
#     TEXT = 1
#     AUDIO = 2


class ConfigsModel(BaseModel):
    # 直播平台
    livePlatform: LivePlatform = LivePlatform.DOUYIN
    # 是否需要本地问答
    localQAEnable: bool = True
    # 本地问答库配置

    # LLM配置
    llmType: LLMType = LLMType.REPEATER
    # ollama配置
    llmOllamaApiAddr: str = 'http://127.0.0.1:11434'
    llmOllamaModel: str = 'qwen:4b-chat'

    # TTS配置
    ttsType: TTSType = TTSType.GPT_SOVITS
    # GPT_SOVITS配置
    ttsGptSovitsApiAddr: str = 'http://127.0.0.1:9880'
    # SovitsModel模型设置
    ttsGptSovitsSovitsModelPath: str = ''
    # GptModel模型设置
    ttsGptSovitsGptModelPath: str = ''
    # 参考音频
    ttsGptSovitsReferWavPath: str = r'E:\DesktopSpace\Development\Python\GPT-SoVITS\audio\badXT\badXT_77.wav'
    # 参考音频文本
    ttsGptSovitsPromptText: str = r'其他都很完美，她确实是啊她，她这个人身材又不好脾气又差不知道为什么能当主播呢？'
    # 参考音频文本语言
    ttsGptSovitsPromptLanguage: str = 'zh'
    # 输入文本语言
    ttsGptSovitsTextLanguage: str = 'zh'

    # 闲时任务配置
    idleTextEnable: bool = False
    idleAudioEnable: bool = False
    # idleType: IdleType = IdleType.AUDIO
    limitIdleTime: int = 60
    idleTextList: List[str] = []
    idleAudioList: List[str] = []
