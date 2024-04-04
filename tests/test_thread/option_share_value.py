import threading
import time


class People():
    stopFlag = False


def judgeStop():
    while True:
        if People.stopFlag:
            print("stop")
            People.stopFlag = False
        time.sleep(1)
        print(f'{People.stopFlag}')


def change():
    People.stopFlag = True


threading.Thread(target=judgeStop).start()

time.sleep(5)

change()

input()

change()
