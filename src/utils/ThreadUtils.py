import ctypes
import threading
import warnings
from threading import Thread


# 自定义线程
class SuperThread(Thread):
    def __init__(self, callback_func=None, group=None, target=None, name=None, args=(), kwargs=None,
                 daemon=None):
        super().__init__(group=group, target=target, name=name,
                         args=args, kwargs=kwargs, daemon=daemon)

        self.callback_func = callback_func
        self.stopFlag = False

    # 停止线程方式1
    def stop(self):
        print(f'正在停止线程:{self.name}')
        if not self.is_alive():
            return
        exc = ctypes.py_object(SystemExit)
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(self.ident), exc)

        print(f"停止线程:{self.name}的结果:{res}")

        if res == 0:
            warnings.warn("找不到线程ID")
            return
        elif res == 1:
            self.stopFlag = True
        elif res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(self.ident, None)
            warnings.warn("'Exception raise failur")
            return

    def get_id(self):
        if hasattr(self, '_thread_id'):
            return self._thread_id
        for id, thread in threading._active.items():
            if thread is self:
                return id

    # 停止线程方式2
    def cease(self):
        print(f'正在停止线程:{self.name}')
        if not self.is_alive():
            return
        exc = ctypes.py_object(SystemExit)
        thread_id = self.get_id()

        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, exc)

        print(f"停止线程:{self.name}的结果:{res}")

        if res == 0:
            warnings.warn("找不到线程ID")
            return
        elif res == 1:
            self.stopFlag = True
        elif res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
            warnings.warn("'Exception raise failur")
            return

    def run(self):
        try:
            if self._target is not None:
                self._target(*self._args, **self._kwargs)
        finally:
            del self._target, self._args, self._kwargs
            if self.callback_func:
                if self.stopFlag:
                    # 在这里释放资源
                    self.callback_func()
