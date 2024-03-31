import requests
from pydantic import BaseModel



class Mo(BaseModel):
    refer_wav_path:str=r'E:\DesktopSpace\Development\Python\GPT-SoVITS\audio\badXT\badXT_77.wav'
    prompt_text:str=r'其他都很完美，她确实是啊她，她这个人身材又不好脾气又差不知道为什么能当主播呢？'
    prompt_language:str="zh"
    text:str=None
    text_language:str="zh"

if __name__ == '__main__':
    m = Mo()
    m.text ='我很好'

    print(m.dict())

    # 发送 GET 请求
    response = requests.get("http://127.0.0.1:9880",params=m.dict())
    audio_path="t1.mp3"
    # 检查响应状态码
    if response.status_code == 200:

        with open(audio_path, 'wb') as f:
            f.write(response.content)
    else:
        print("请求失败，状态码：", response.status_code)
