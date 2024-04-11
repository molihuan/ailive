import os

from flet_core import Page, Container, Column, ElevatedButton, ScrollMode, MainAxisAlignment, alignment, \
    Ref, ControlEvent, Switch, TextField, Row, Text

from src.dao.DataManager import DataManager
from src.pages.BasePage import BasePage
from src.service.tts.GPTSoVITSTTS import GPTSoVITSTTS
from src.utils.CommonUtils import CommonUtils
from src.utils.FileUtils import FileUtils
from src.utils.StrUtils import StrUtils


# 闲时页面
class IdlePage(BasePage):
    def __init__(self, parent: Page):
        super().__init__()
        self.parent = parent

        self.limitIdleTimeTF = Ref[TextField]()

        self.idleTextSwitch = Ref[Switch]()
        self.idleAudioSwitch = Ref[Switch]()

        self.idleTextTF = Ref[TextField]()
        self.idleAudioTF = Ref[TextField]()

        self.btn_save = Ref[ElevatedButton]()

    def initData(self):
        self.page.update()

    def did_mount(self):
        # 挂载后调用
        self.initData()
        pass

    def switch_change(self, e: ControlEvent):
        view = e.control
        if view == self.idleTextSwitch.current:
            if view.value:
                self.idleAudioSwitch.current.value = False
                print(f'Audio:False')

        elif view == self.idleAudioSwitch.current:
            if view.value:
                self.idleTextSwitch.current.value = False
                print(f'Text:False')

        self.page.update()

    def btn_click(self, e: ControlEvent):
        view = e.control
        if view == self.btn_save.current:
            self.configs.idleTextEnable = self.idleTextSwitch.current.value
            self.configs.idleAudioEnable = self.idleAudioSwitch.current.value

            self.configs.idleTextList = StrUtils.str2strList(self.idleTextTF.current.value)
            self.configs.idleAudioList = StrUtils.str2strList(self.idleAudioTF.current.value)

            self.configs.limitIdleTime = int(self.limitIdleTimeTF.current.value)

            if DataManager.saveConfigs():
                CommonUtils.showSnack("保存成功")
            else:
                CommonUtils.showSnack("保存失败")

    def idleText2Audio(self):
        tf_raw = self.idleTextTF.current.value
        textList = StrUtils.str2strList(tf_raw)
        useful_path = FileUtils.getTempUsefulPath()
        vitstts = GPTSoVITSTTS()
        audioPathList = []
        for index, text in enumerate(textList):
            if StrUtils.removeSpace(text).isspace():
                continue
            audioPath = os.path.join(useful_path, str(index) + ".wav")
            vitstts.text2audio(text, audioPath)
            audioPathList.append(audioPath)
        result = StrUtils.strList2str(audioPathList)
        print(result)
        self.idleAudioTF.current.value = result
        self.idleAudioTF.current.update()

    def build(self):
        return Container(
            content=Column([
                Row([
                    Text('触发闲时任务时间'),
                    TextField(
                        ref=self.limitIdleTimeTF,
                        value=self.configs.limitIdleTime,
                        hint_text="单位秒",
                        width=100
                    ),
                    Text('秒')
                ]),

                Switch(ref=self.idleTextSwitch, label="闲时文案模式", on_change=self.switch_change,
                       value=self.configs.idleTextEnable),
                TextField(
                    ref=self.idleTextTF,
                    value=StrUtils.strList2str(self.configs.idleTextList),
                    label='闲时文案',
                    hint_text="一句一行",
                    multiline=True,
                    min_lines=5,
                    max_lines=10,
                ),
                ElevatedButton(text='转换', on_click=lambda e: self.idleText2Audio()),
                Switch(ref=self.idleAudioSwitch, label="闲时音频模式", on_change=self.switch_change,
                       value=self.configs.idleAudioEnable),
                TextField(
                    ref=self.idleAudioTF,
                    value=StrUtils.strList2str(self.configs.idleAudioList),
                    label='闲时音频',
                    hint_text="输入音频路径,一个一行",
                    multiline=True,
                    min_lines=5,
                    max_lines=10,
                ),
                ElevatedButton(ref=self.btn_save, text='保存', on_click=self.btn_click)
            ],
                scroll=ScrollMode.ALWAYS,
                alignment=MainAxisAlignment.CENTER
            ),
            alignment=alignment.center

        )
