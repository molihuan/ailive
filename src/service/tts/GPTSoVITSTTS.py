import uuid
from queue import Queue

import requests
from pydantic import BaseModel

from src.service.tts.BaseTTS import BaseTTS, AudioCompoundQueueItem, AudioPlayQueueItem

# 请求模型
from src.utils.FileUtils import FileUtils
from src.utils.LogUtils import LogUtils


class TextToAudioReqModel(BaseModel):
    refer_wav_path:str=None
    prompt_text:str=None
    prompt_language:str="zh"
    text:str=None
    text_language:str="zh"

class GPTSoVITSTTS(BaseTTS):

    def __init__(self,refer_wav_path,prompt_text):
        # 参考音频路径
        self.refer_wav_path: str = refer_wav_path
        # 参考音频文本
        self.prompt_text: str = prompt_text
        pass

    def init(self):
        pass

    def text2audio(self,text:str,audio_path:str):
        LogUtils.d(f'TTS文本:{text}')

        text_to_audio_req_model = TextToAudioReqModel(
            refer_wav_path=self.refer_wav_path,
            prompt_text=self.prompt_text,
            text=text
        )

        params=text_to_audio_req_model.dict()

        response = requests.get("http://127.0.0.1:9880", params=params)

        # 检查响应状态码
        if response.status_code == 200:

            with open(audio_path, 'wb') as f:
                f.write(response.content)

            LogUtils.d(f'TTS合成音频完成:{audio_path}')

            return audio_path
        else:
            print("请求失败，状态码：", response.status_code)
            return None

    # 音频合成队列、音频播放队列
    def text2audioByQueue(self, audioCompoundQueue: Queue, audioPlayQueue: Queue):
        while True:

            item:AudioCompoundQueueItem=audioCompoundQueue.get()
            audioPath=self.text2audio(item.text,item.audioPath)

            if audioPath is None:
                continue

            audio_play_queue_item = AudioPlayQueueItem(
                audioPath=audioPath,
                useful=item.useful
            )

            audioPlayQueue.put(audio_play_queue_item)


