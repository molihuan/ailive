import asyncio
import json

import websockets

from src.dao.OptionEnum import MsgType
from src.service.ServiceManager import ServiceManager
from src.service.danmaku.BaseDanmaku import BaseDanmaku
from src.service.llm.BaseLLM import AskQueueItem
from src.utils.LogUtils import LogUtils
from src.utils.ThreadUtils import SuperThread


class DouyinBarrageGrabDK(BaseDanmaku):
    """
    通过DouyinBarrageGrab获取抖音弹幕
    """

    def init(self):
        pass

    def getDanmakuTask(self):
        asyncio.run(self.danmakuWebsocket())

    def startGetDanmakuThread(self):
        danmakuWebsocketThread = SuperThread(target=self.getDanmakuTask)
        danmakuWebsocketThread.start()
        pass

    def stopGetDanmakuThread(self):
        pass

    async def on_message(self, ws, message):

        message_json = json.loads(message)
        # LogUtils.d(message_json)
        if "Type" in message_json:
            type = message_json["Type"]
            data_json = json.loads(message_json["Data"])

            if type == MsgType.DANMAKU.value:
                # 弹幕信息
                # 闲时计数清零
                global_idle_time = 0

                username = data_json["User"]["Nickname"]
                content = data_json["Content"]

                LogUtils.d(f'[📧直播间弹幕消息] [{username}]：{content}')

                ask_queue = ServiceManager.generalManager.askQueue
                item = AskQueueItem(text=content)
                ask_queue.put(item)

                pass

            elif type == MsgType.LIKE.value:
                # 点赞信息
                username = data_json["User"]["Nickname"]
                count = data_json["Count"]

                LogUtils.d(f'[👍直播间点赞消息] {username} 点了{count}赞')

            elif type == MsgType.ENTER_LIVE_ROOM.value:
                # 用户进入直播间
                username = data_json["User"]["Nickname"]

                LogUtils.d(f'[🚹🚺直播间成员加入消息] 欢迎 {username} 进入直播间')


            elif type == MsgType.FOLLOW.value:
                # 用户关注
                username = data_json["User"]["Nickname"]

                LogUtils.d(f'[➕直播间关注消息] 感谢 {username} 的关注')

                pass

            elif type == MsgType.GIFT.value:
                # 用户送礼物
                username = data_json["User"]["Nickname"]
                # 礼物数量
                num = data_json["GiftCount"]
                gift_name = data_json["GiftName"]
                # 礼物重复数量
                repeat_count = data_json["RepeatCount"]

                LogUtils.d(
                    f'[🎁直播间礼物消息] 用户：{username} 赠送 {num} 个 {gift_name}')



            elif type == MsgType.LIVE_ROOM_INFO.value:
                # 直播间信息
                LogUtils.d(f'[直播间数据] {data_json["Content"]}')
                # {'OnlineUserCount': 50, 'TotalUserCount': 22003, 'TotalUserCountStr': '2.2万', 'OnlineUserCountStr': '50',
                # 'MsgId': 7260517442466662207, 'User': None, 'Content': '当前直播间人数 50，累计直播间人数 2.2万', 'RoomId': 7260415920948906807}
                pass

            elif type == MsgType.SHARE_LIVE_ROOM.value:
                # 分享直播间
                LogUtils.d(f'[分享直播间] 感谢 {data_json["User"]["Nickname"]} 分享了直播间')
                pass

    async def on_error(self, error):
        # 处理错误
        LogUtils.e(f"Error: {error}")

    async def on_close(self):
        # 处理连接关闭
        LogUtils.d("danmakuWebsocket 关闭")

    async def on_open(self):
        # 处理连接建立
        LogUtils.d("danmakuWebsocket 连接")

    async def danmakuWebsocket(self):
        uri = "ws://127.0.0.1:8888"
        async with websockets.connect(uri, ping_interval=None) as websocket:
            await self.on_open()
            try:
                async for message in websocket:
                    await self.on_message(websocket, message)
            except websockets.exceptions.ConnectionClosedError:
                await self.on_close()
