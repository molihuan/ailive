from queue import Queue

import requests
from pydantic import BaseModel

from src.dao.OptionEnum import MsgType
from src.service.idle.IdleTaskManager import IdleTaskManager
from src.service.tts.BaseTTS import BaseTTS, AudioCompoundQueueItem, AudioPlayQueueItem

from src.utils.LogUtils import LogUtils


class TextToAudioReqModel(BaseModel):
    refer_wav_path: str = None
    prompt_text: str = None
    prompt_language: str = "zh"
    text: str = None
    text_language: str = "zh"


class GPTSoVITSTTS(BaseTTS):
    needResults: bool = True

    def __init__(self):
        super().__init__()
        # 参考音频路径
        self.refer_wav_path: str = self.configs.ttsGptSovitsReferWavPath
        # 参考音频文本
        self.prompt_text: str = self.configs.ttsGptSovitsPromptText
        # TODO 设置模型、切换模型
        # 创建一个 Session 对象
        self.session = requests.Session()

    def init(self):
        pass

    def getSendRequestTool(self):
        return self.session

    def setNeedResults(self, need):
        GPTSoVITSTTS.needResults = need

    # def judgeSendRequestToolClosed(self):
    #     return self.session.closed

    def text2audio(self, text: str, audio_path: str):
        # LogUtils.d(f'TTS文本:{text}')

        text_to_audio_req_model = TextToAudioReqModel(
            refer_wav_path=self.refer_wav_path,
            prompt_text=self.prompt_text,
            text=text
        )

        params = text_to_audio_req_model.dict()

        # http请求
        # response = requests.get(self.configs.ttsGptSovitsApiAddr, params=params)
        # # 检查响应状态码
        # if response.status_code == 200:
        #     with open(audio_path, 'wb') as f:
        #         f.write(response.content)
        #     LogUtils.d(f'TTS合成音频完成:{audio_path}')
        #     return audio_path
        # else:
        #     print("请求失败，状态码：", response.status_code)
        #     return None

        # 判断是否需要结果
        if not GPTSoVITSTTS.needResults:
            GPTSoVITSTTS.needResults = True
            print(f'停止获取音频数据')
            return None

        response = self.session.get(self.configs.ttsGptSovitsApiAddr, params=params)

        # 判断是否需要结果
        if not GPTSoVITSTTS.needResults:
            GPTSoVITSTTS.needResults = True
            print(f'停止获取音频数据')
            return None

        # 检查响应状态码
        if response.status_code == 200:
            with open(audio_path, 'wb') as f:
                f.write(response.content)
            # 判断是否需要结果
            if not GPTSoVITSTTS.needResults:
                GPTSoVITSTTS.needResults = True
                print(f'停止获取音频数据')
                return None

            LogUtils.d(f'TTS合成音频完成:{text}')
            return audio_path
        else:
            print("请求失败，状态码：", response.status_code)
            return None

    # 音频合成队列、音频播放队列
    def text2audioByQueue(self, audioCompoundQueue: Queue, audioPlayQueue: Queue):
        while True:

            item: AudioCompoundQueueItem = audioCompoundQueue.get()
            audioPath = self.text2audio(item.text, item.audioPath)

            if audioPath is None:
                continue

            audio_play_queue_item = AudioPlayQueueItem(
                audioPath=audioPath,
                useful=item.useful,
                msgType=item.msgType,
                userName=item.userName,
                startPlayPos=item.startPlayPos,
                idleDataListIndex=item.idleDataListIndex
            )
            LogUtils.e(f'播放队列+:{item.text}')
            audioPlayQueue.put(audio_play_queue_item)

            # 判断是否是是弹幕,如果是则音频闲时任务停止
            if item.msgType == MsgType.DANMAKU:
                IdleTaskManager.stopDoAudioIdleTaskFlag = True
