import threading
import time

mp3Path = r'E:\DesktopSpace\Development\Python\ailive\assets\t1.mp3'

import pygame


def play_audio_thread(file_path):
    pygame.mixer.init()  # 初始化音频模块
    pygame.mixer.music.load(file_path)  # 加载音频文件
    pygame.mixer.music.play()  # 播放音频
    while pygame.mixer.music.get_busy():
        # pygame.time.Clock().tick(10)
        pass


def pause_audio():
    pygame.mixer.music.pause()  # 暂停音频

def unpause_audio():
    pygame.mixer.music.unpause()  # 继续音频


# pause_audio()  # 暂停音频
#
# unpause_audio()  # 继续音频

thread = threading.Thread(target=play_audio_thread,args=(mp3Path,))

thread.start()

for i in range(30):
    print(f"Main thread is running...{i}")
    if i == 15 :
        pause_audio()
    if i == 25 :
        unpause_audio()
    time.sleep(1)

thread.join()
