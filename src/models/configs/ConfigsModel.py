from enum import Enum
from typing import List

from pydantic import BaseModel


# 直播平台
class LivePlatform(Enum):
    BILIBILI = 'Bilibili'
    DOUYIN = '抖音'


# 大语言模型
class LLMType(Enum):
    # 复读机
    REPEATER = 'Repeater'
    OLLAMA_LLM = "Ollama"
    ANYTHING_LLM = "AnythingLLM"


# 文本转语音
class TTSType(Enum):
    GPT_SOVITS = 'GPT_SoVITS'


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
    # AnythingLLM配置
    # 请求头中需要Authorization: Bearer 7HEQ8QN-QEBM5N1-J5QTM7M-PJ9M788
    llmAnythingLLMApiAddr: str = 'http://127.0.0.1:3001'
    # 工作区Slug
    llmAnythingLLMWorkspaceSlug: str = 'ailive'
    llmAnythingLLMKey: str = '7HEQ8QN-QEBM5N1-J5QTM7M-PJ9M788'

    # curl -X 'POST' \
    #   'http://localhost:3001/api/v1/workspace/ailive/chat' \
    #   -H 'accept: application/json' \
    #   -H 'Authorization: Bearer 7HEQ8QN-QEBM5N1-J5QTM7M-PJ9M788' \
    #   -H 'Content-Type: application/json' \
    #   -d '{
    #   "message": "What is AnythingLLM?",
    #   "mode": "chat"
    # }'
    # chat地址
    llmAnythingLLMChatAddr: str = f'{llmAnythingLLMApiAddr}/api/v1/workspace/{llmAnythingLLMWorkspaceSlug}/chat'

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

    # 抖音直播间配置
    # 直播间号
    douyinLiveRoomNumber: str = "483662997209"
