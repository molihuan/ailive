import uuid
from queue import Queue

import ollama

from src.service.llm.BaseLLM import BaseLLM, AskQueueItem
from src.service.tts.BaseTTS import AudioCompoundQueueItem
from src.utils.FileUtils import FileUtils
from src.utils.LogUtils import LogUtils


class OllamaLLM(BaseLLM):
    def init(self,model='qwen:4b-chat'):
        self.model =model
        pass
    def ask(self,content:str):
        LogUtils.d(f'提问:{content}')
        # TODO 进行进行本地问答库回答,获取配置是否需要本地库回答
        response = ollama.chat(model=self.model, messages=[
            {
                'role': 'user',
                'content': content,
            },
        ])
        answer = response['message']['content']
        LogUtils.d(f'LLM回答:{answer}')
        return answer
    # 问题队列，音频合成队列
    def askByQueue(self,askQueue:Queue,audioCompoundQueue:Queue):
        while True:
            askQueueItem:AskQueueItem = askQueue.get()
            # 获取答案
            answerText=self.ask(askQueueItem.text)
            # 封装答案

            # 设置准备生成音频的路径
            temp_audio_name =str(uuid.uuid4()) +'.wav'

            if askQueueItem.useful:
                temp_audio_path=FileUtils.fileInTempUsefulPath(temp_audio_name)
            else:
                temp_audio_path = FileUtils.fileInTempUselessPath(temp_audio_name)

            audio_compound_queue_item = AudioCompoundQueueItem(
                useful=askQueueItem.useful,
                text=answerText,
                audioPath=temp_audio_path
            )

            audioCompoundQueue.put(audio_compound_queue_item)


