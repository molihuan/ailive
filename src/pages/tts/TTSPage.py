from flet_core import UserControl, Page, Container, Column, ElevatedButton, ScrollMode, MainAxisAlignment, alignment, \
    Ref, ControlEvent, Dropdown, dropdown, Card, ListTile, Row, TextField, Icon, icons, Text, TextButton, colors

from src.dao.DataManager import DataManager
from src.models.configs.ConfigsModel import LLMType, TTSType
from src.pages.BasePage import BasePage
from src.utils.CommonUtils import CommonUtils
from src.utils.StrUtils import StrUtils


class TTSPage(BasePage):
    def __init__(self, parent: Page):
        super().__init__()

        self.tf_idleText = Ref[TextField]()
        self.column_card_area = Ref[Column]()
        self.card_gpt_sovits_settings = Ref[Card]()
        self.tf_ttsGptSovitsReferWavPath = Ref[TextField]()
        self.tf_ttsGptSovitsPromptText = Ref[TextField]()
        self.tf_ttsGptSovitsApiAddr = Ref[TextField]()
        self.parent = parent
        self.btn_save = Ref[ElevatedButton]()
        self.dd_select_tts_type = Ref[Dropdown]()

    def initData(self):
        # 配置读取
        # 大语言类型设置
        self.dd_select_tts_type.current.value = self.configs.ttsType.value
        ddSelectTtsTypeList = []
        for ttsType in TTSType:
            ddSelectTtsTypeList.append(dropdown.Option(ttsType.value))
        self.dd_select_tts_type.current.options = ddSelectTtsTypeList
        self.dd_select_tts_type.current.update()
        # 设置GptSovits地址
        self.tf_ttsGptSovitsApiAddr.current.value = self.configs.ttsGptSovitsApiAddr
        self.tf_ttsGptSovitsApiAddr.current.update()
        # 设置GptSovits参考音频
        self.tf_ttsGptSovitsReferWavPath.current.value = self.configs.ttsGptSovitsReferWavPath
        self.tf_ttsGptSovitsReferWavPath.current.update()
        # 设置GptSovits参考音频文本
        self.tf_ttsGptSovitsPromptText.current.value = self.configs.ttsGptSovitsPromptText
        self.tf_ttsGptSovitsPromptText.current.update()

    def did_mount(self):
        # 挂载后调用
        self.initData()
        pass

    def btn_click(self, e: ControlEvent):
        view = e.control
        if view == self.btn_save.current:
            self.configs.ttsType = TTSType(self.dd_select_tts_type.current.value)
            self.configs.ttsGptSovitsApiAddr = self.tf_ttsGptSovitsApiAddr.current.value.strip()
            self.configs.ttsGptSovitsReferWavPath = self.tf_ttsGptSovitsReferWavPath.current.value.strip()
            self.configs.ttsGptSovitsPromptText = self.tf_ttsGptSovitsPromptText.current.value.strip()

            if DataManager.saveConfigs():
                CommonUtils.showSnack("保存成功")
            else:
                CommonUtils.showSnack("保存失败")

    def llmTypeSelectChanged(self, e: ControlEvent):
        self.configs.ttsType = LLMType(self.dd_select_tts_type.current.value)
        print(e.control.value)

    def idleText2Audio(self):
        rr = StrUtils.str2strList(self.tf_idleText.current.value)
        print(rr)
        pass

    def build(self):
        return Container(
            content=Column([
                Dropdown(
                    ref=self.dd_select_tts_type,
                    label='类型',
                    on_change=self.llmTypeSelectChanged,
                    options=[],
                ),

                Column(
                    ref=self.column_card_area,
                    controls=[
                        Card(
                            ref=self.card_gpt_sovits_settings,
                            visible=True,
                            content=Container(
                                content=Column(
                                    [
                                        ListTile(
                                            title=Text("GPT_SoVITS配置", size=18, color=colors.PURPLE),
                                        ),
                                        TextField(ref=self.tf_ttsGptSovitsApiAddr, label='GPT_SoVITS地址',
                                                  width=self.page.width / 2),
                                        TextField(ref=self.tf_ttsGptSovitsReferWavPath, label='GPT_SoVITS参考音频',
                                                  width=self.page.width / 2),
                                        TextField(ref=self.tf_ttsGptSovitsPromptText, label='GPT_SoVITS参考音频文本',
                                                  width=self.page.width / 2),
                                    ]
                                ),
                                # width=400,
                                padding=8,
                                margin=15,
                            )
                        ),
                        Card(

                            visible=True,
                            content=Container(
                                content=Column(
                                    [
                                        ListTile(
                                            title=Text("文案转音频", size=18, color=colors.PURPLE),
                                        ),
                                        TextField(
                                            ref=self.tf_idleText,
                                            # value=StrUtils.strList2str(self.configs.idleTextList),
                                            label='文案转音频',
                                            hint_text="一句一行",
                                            multiline=True,
                                            min_lines=5,
                                            max_lines=10,
                                        ),
                                        Row([
                                            ElevatedButton('转换', on_click=lambda _: self.idleText2Audio())
                                        ])
                                    ]
                                ),
                                # width=400,
                                padding=8,
                                margin=15,
                            )
                        ),
                    ]
                ),

                ElevatedButton(ref=self.btn_save, text='保存', on_click=self.btn_click)
            ],
                scroll=ScrollMode.ALWAYS,
                alignment=MainAxisAlignment.CENTER
            ),
            # alignment=alignment.center
        )
