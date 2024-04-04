import re


class StrUtils:
    @staticmethod
    def removeSpace(text):
        """
        去除字符串中的所有空白字符（包括空格、制表符、换行符等）。

        参数：
            text (str): 要处理的文本。

        返回：
            str: 去除空白字符后的文本。
        """
        cleaned_text = re.sub(r'\s+', '', text)
        return cleaned_text

    @staticmethod
    def strList2str(string_list):
        """
        将字符串列表拼接成一个字符串，每个字符串之间使用回车符连接。

        参数：
            string_list (list[str]): 要拼接的字符串列表。

        返回：
            str: 拼接后的字符串。
        """
        return '\n'.join(string_list)

    @staticmethod
    def str2strList(text):
        """
        将包含换行符的字符串拆分成一个字符串列表。

        参数：
            text (str): 要拆分的字符串。

        返回：
            list[str]: 拆分后的字符串列表。
        """
        return text.split('\n')
