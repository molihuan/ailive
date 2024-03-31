import os

# 文件和路径工具
class FileUtils():

    @classmethod
    def create_folder_if_not_exists(cls,folder_path):
        # 判断文件夹是否存在
        if not os.path.exists(folder_path):
            # 如果不存在，则创建文件夹
            os.makedirs(folder_path)
            print(f"文件夹 '{folder_path}' 已创建")
        else:
            print(f"文件夹 '{folder_path}' 已存在")

    @classmethod
    def initPath(cls):
        # 初始化日志文件夹
        cls.create_folder_if_not_exists(cls.getLogsPath())
        # 初始化资源文件夹
        cls.create_folder_if_not_exists(cls.getAssetsPath())
        # 初始化临时文件夹
        cls.create_folder_if_not_exists(cls.getTempUsefulPath())
        cls.create_folder_if_not_exists(cls.getTempUselessPath())


    @classmethod
    def getWorkPath(cls):
        work_path=os.getcwd()
        return work_path

    @classmethod
    def fileInWorkPath(cls, *paths):
        path = os.path.join(cls.getWorkPath(),*paths)
        return path

    @classmethod
    def fileInTempPath(cls, *paths):
        path = os.path.join(cls.getTempPath(),*paths)
        return path

    @classmethod
    def fileInTempUsefulPath(cls, *paths):
        path = os.path.join(cls.getTempUsefulPath(),*paths)
        return path

    @classmethod
    def fileInTempUselessPath(cls, *paths):
        path = os.path.join(cls.getTempUselessPath(),*paths)
        return path

    @classmethod
    def getLogsPath(cls):
        path=cls.fileInWorkPath('logs')
        return path

    @classmethod
    def getAssetsPath(cls):
        path=cls.fileInWorkPath('assets')
        return path

    @classmethod
    def getTempPath(cls):
        path=cls.fileInWorkPath('temp')
        return path

    @classmethod
    def getTempUsefulPath(cls):
        path=cls.fileInTempPath('useful')
        return path

    @classmethod
    def getTempUselessPath(cls):
        path=cls.fileInTempPath('useless')
        return path

    @classmethod
    def getCurrentPath(cls):
        current_file_path = os.path.realpath(__file__)
        current_dir_path=os.path.dirname(current_file_path)

        return current_dir_path

    @classmethod
    def fileInCurrentPath(cls, *paths):
        filePath = os.path.join(cls.getCurrentPath(),*paths)
        return filePath
