from flet_core import UserControl, Page, Container, Column, ElevatedButton, ScrollMode, MainAxisAlignment, alignment, \
    Ref, ControlEvent, Dropdown, dropdown, Card, ListTile, Row, TextField, Icon, icons, Text, TextButton, colors

from src.dao.DataManager import DataManager
from src.models.configs.ConfigsModel import LLMType
from src.pages.BasePage import BasePage
from src.utils.CommonUtils import CommonUtils

# 大语言设置页面
from src.utils.LogUtils import LogUtils


class LiveRoomPage(BasePage):
    """
    直播间设置页面
    """

    def __init__(self, parent: Page):
        super().__init__()
        self.tf_llmAnythingLLMKey = Ref[TextField]()
        self.tf_llmAnythingLLMWorkspaceSlug = Ref[TextField]()
        self.tf_llmAnythingLLMApiAddr = Ref[TextField]()
        self.card_anything_llm_settings = Ref[Card]()
        self.card_ollama_settings = Ref[Card]()
        self.column_card_area = Ref[Column]()
        self.tf_llmOllamaModel = Ref[TextField]()
        self.tf_douyinLiveRoomNumber = Ref[TextField]()
        self.parent = parent
        self.btn_save = Ref[ElevatedButton]()
        self.dd_select_llm_type = Ref[Dropdown]()

    def initData(self):
        # 配置读取
        # 大语言类型设置
        self.dd_select_llm_type.current.value = self.configs.llmType.value
        ddSelectLlmTypeList = []
        for llmType in LLMType:
            ddSelectLlmTypeList.append(dropdown.Option(llmType.value))
        self.dd_select_llm_type.current.options = ddSelectLlmTypeList
        self.dd_select_llm_type.current.update()

        self.tf_douyinLiveRoomNumber.current.value = self.configs.douyinLiveRoomNumber
        self.tf_douyinLiveRoomNumber.current.update()

        self.tf_llmOllamaModel.current.value = self.configs.llmOllamaModel
        self.tf_llmOllamaModel.current.update()

        self.tf_llmAnythingLLMApiAddr.current.value = self.configs.llmAnythingLLMApiAddr
        self.tf_llmAnythingLLMApiAddr.current.update()

        self.tf_llmAnythingLLMWorkspaceSlug.current.value = self.configs.llmAnythingLLMWorkspaceSlug
        self.tf_llmAnythingLLMWorkspaceSlug.current.update()

        self.tf_llmAnythingLLMKey.current.value = self.configs.llmAnythingLLMKey
        self.tf_llmAnythingLLMKey.current.update()

    def did_mount(self):
        # 挂载后调用
        self.initData()
        pass

    def btn_click(self, e: ControlEvent):
        view = e.control
        if view == self.btn_save.current:
            self.configs.llmType = LLMType(self.dd_select_llm_type.current.value)
            self.configs.douyinLiveRoomNumber = self.tf_douyinLiveRoomNumber.current.value.strip()
            self.configs.llmOllamaModel = self.tf_llmOllamaModel.current.value.strip()

            self.configs.llmAnythingLLMKey = self.tf_llmAnythingLLMKey.current.value.strip()
            self.configs.llmAnythingLLMApiAddr = self.tf_llmAnythingLLMApiAddr.current.value.strip()
            self.configs.llmAnythingLLMWorkspaceSlug = self.tf_llmAnythingLLMWorkspaceSlug.current.value.strip()
            LogUtils.d(self.configs)
            if DataManager.saveConfigs():
                CommonUtils.showSnack("保存成功")
            else:
                CommonUtils.showSnack("保存失败")

    def llmTypeSelectChanged(self, e: ControlEvent):
        self.configs.llmType = LLMType(self.dd_select_llm_type.current.value)
        print(e.control.value)

    def build(self):
        return Container(
            content=Column([
                Dropdown(
                    ref=self.dd_select_llm_type,
                    label='直播类型',
                    on_change=self.llmTypeSelectChanged,
                    options=[],
                ),

                Column(
                    ref=self.column_card_area,
                    controls=[
                        Card(
                            ref=self.card_ollama_settings,
                            visible=True,
                            content=Container(
                                content=Column(
                                    [
                                        ListTile(
                                            title=Text("抖音配置", size=18, color=colors.PURPLE),
                                        ),
                                        TextField(ref=self.tf_douyinLiveRoomNumber, label='直播间号',
                                                  width=self.page.width / 2),
                                        TextField(ref=self.tf_llmOllamaModel, label='待定',
                                                  width=self.page.width / 2),
                                    ]
                                ),
                                # width=400,
                                padding=8,
                                margin=15,
                            )
                        ),
                        Card(
                            ref=self.card_anything_llm_settings,
                            visible=True,
                            content=Container(
                                content=Column(
                                    [
                                        ListTile(
                                            title=Text("AnythingLLM配置", size=18, color=colors.PURPLE),
                                        ),
                                        TextField(ref=self.tf_llmAnythingLLMApiAddr, label='AnythingLLM地址',
                                                  width=self.page.width / 2),
                                        TextField(ref=self.tf_llmAnythingLLMWorkspaceSlug, label='工作区Slug',
                                                  width=self.page.width / 2),
                                        TextField(ref=self.tf_llmAnythingLLMKey, label='Key',
                                                  width=self.page.width / 2),
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
