import asyncio
import json
import logging
import threading
import time
import traceback

import websockets

import test_websockets


async def on_message(ws, message):
    # global last_liveroom_data, last_username_list, config, config_path
    # global global_idle_time

    message_json = json.loads(message)
    # logging.debug(message_json)
    if "Type" in message_json:
        type = message_json["Type"]
        data_json = json.loads(message_json["Data"])

        if type == 1:
            # 弹幕信息
            # 闲时计数清零
            global_idle_time = 0

            username = data_json["User"]["Nickname"]
            content = data_json["Content"]

            print(f'[📧直播间弹幕消息] [{username}]：{content}')

            # data = {
            #     "platform": platform,
            #     "username": username,
            #     "content": content
            # }
            #
            # my_handle.process_data(data, "comment")

            pass

        elif type == 2:
            # 点赞信息
            username = data_json["User"]["Nickname"]
            count = data_json["Count"]

            print(f'[👍直播间点赞消息] {username} 点了{count}赞')

        elif type == 3:
            # 用户进入直播间
            username = data_json["User"]["Nickname"]

            print(f'[🚹🚺直播间成员加入消息] 欢迎 {username} 进入直播间')

            # data = {
            #     "platform": platform,
            #     "username": username,
            #     "content": "进入直播间"
            # }
            #
            # # 添加用户名到最新的用户名列表
            # add_username_to_last_username_list(username)
            #
            # my_handle.process_data(data, "entrance")

        elif type == 4:
            # 用户关注
            username = data_json["User"]["Nickname"]

            print(f'[➕直播间关注消息] 感谢 {data_json["User"]["Nickname"]} 的关注')

            # data = {
            #     "platform": platform,
            #     "username": username
            # }

            # my_handle.process_data(data, "follow")

            pass

        elif type == 5:
            # 用户送礼物
            username = data_json["User"]["Nickname"]
            # 礼物数量
            num = data_json["GiftCount"]
            gift_name = data_json["GiftName"]
            # 礼物重复数量
            repeat_count = data_json["RepeatCount"]

            print(
                f'[🎁直播间礼物消息] 用户：{username} 赠送 {num} 个 {gift_name}')

            # data = {
            #     "platform": platform,
            #     "gift_name": gift_name,
            #     "username": username,
            #     "num": num,
            #     "unit_price": discount_price / 10,
            #     "total_price": combo_total_coin / 10
            # }

            # my_handle.process_data(data, "gift")

        elif type == 6:
            # 直播间信息
            print(f'[直播间数据] {data_json["Content"]}')
            # {'OnlineUserCount': 50, 'TotalUserCount': 22003, 'TotalUserCountStr': '2.2万', 'OnlineUserCountStr': '50',
            # 'MsgId': 7260517442466662207, 'User': None, 'Content': '当前直播间人数 50，累计直播间人数 2.2万', 'RoomId': 7260415920948906807}
            # print(f"data_json={data_json}")

            last_liveroom_data = data_json

            # 当前在线人数
            OnlineUserCount = data_json["OnlineUserCount"]

            print(f'在线人数:{OnlineUserCount}')
            pass

        elif type == 8:
            # 分享直播间
            print(f'[分享直播间] 感谢 {data_json["User"]["Nickname"]} 分享了直播间')

            pass


async def on_error(error):
    # 处理错误
    logging.error(f"Error: {error}")

async def on_close():
    # 处理连接关闭
    logging.debug("WebSocket connection closed")

async def on_open():
    # 处理连接建立
    logging.debug("WebSocket connection established")

async def websocket_client():
    uri = "ws://127.0.0.1:8888"
    async with websockets.connect(uri, ping_interval=None) as websocket:
        await on_open()
        try:
            async for message in websocket:
                await on_message(websocket,message)
        except websockets.exceptions.ConnectionClosedError:
            await on_close()


def print_message():
    while True:
        print("55555555555")
        time.sleep(3)

if __name__ == "__main__":
    # 创建并启动打印消息的线程
    thread = threading.Thread(target=print_message)
    thread.start()

    asyncio.run(websocket_client())
