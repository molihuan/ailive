from enum import Enum

# 选项枚举类
class MsgType(Enum):
    # 弹幕
    DANMAKU = 1
    # 点赞
    LIKE = 2
    # 进入直播间
    ENTER_LIVE_ROOM = 3
    # 关注
    FOLLOW = 4
    # 礼物
    GIFT = 5
    # 直播间信息
    LIVE_ROOM_INFO = 6
    # 分享直播间
    SHARE_LIVE_ROOM = 7
    # 闲时
    IDLE=100

# if __name__ == '__main__':
#     print(MsgType.DANMAKU.value)