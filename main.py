from flet import Page, CrossAxisAlignment, app

from src.dao.DataManager import DataManager
from src.pages.route.AppRoutes import AppRoutes
from src.service.ServiceManager import ServiceManager
from src.utils.CommonUtils import CommonUtils
from src.utils.FileUtils import FileUtils
from src.utils.LogUtils import LogUtils


# https://live.douyin.com/483662997209
def fletApp(page: Page):
    page.title = " "
    page.horizontal_alignment = CrossAxisAlignment.CENTER

    # 日志工具初始化
    LogUtils.init(FileUtils.fileInWorkPath("logging.yaml"))
    # 数据管理者初始化
    DataManager.setPage(page)
    DataManager.init()
    # 初始化路径
    FileUtils.initPath()
    # 通用工具初始化
    CommonUtils.init(page)
    # 业务管理者初始化
    ServiceManager.init(page)

    # 路由配置
    appRoutes = AppRoutes(page)
    page.on_route_change = appRoutes.route_change
    page.on_view_pop = appRoutes.view_pop
    page.go(page.route)


if __name__ == '__main__':
    app(target=fletApp)
    # app(target=fletApp, view=AppView.WEB_BROWSER)
