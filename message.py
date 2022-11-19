import time

# 定义标准数值上下限

HEAD_HIGH_DISTANCE = 45  # 头到纸的最大距离
HEAD_LOW_DISTANCE = 30  # 头到纸的最小距离

HAND_HIGH_DISTANCE = 4  # 手到笔尖最大距离
HAND_LOW_DISTANCE = 2  # 手到笔尖最小距离

HIGH_LUX = 600  # 最大环境亮度
LOW_LUX = 400  # 最小环境亮度


# TODO:def timeFormat(timestamp=0):
#     time_1 = timestamp
#     time_tuple_1 = time.localtime(time_1)
#     bj_time = time.strftime("%Y/%m/%d %H:%M:%S", time_tuple_1)
#     return bj_time
#       时间戳转换为北京时间方法
#       2022_11_07_22:10 未解决

class Message:  # 定义消息类
    __time = 0
    __id = 0
    __headDistance = 0
    __handDistance = 0
    __lux = 0

    def judgmentParameters(self):
        print(self.getTime())  # 打印当前检测时间
        isHeadDistance = self.isHeadDistance()
        isHandeDistance = self.isHandDistance()
        isLux = self.isLux()
        if isHandeDistance and isHandeDistance and isLux:  # 当传感器三个参数都符合标准条件时
            print("当前符合标准书写条件")

    def isHeadDistance(self):  # 判断头和纸的距离
        if self.__headDistance > HEAD_HIGH_DISTANCE:
            print("头和纸的距离太远！")
            return False
        elif self.__headDistance < HEAD_LOW_DISTANCE:
            print("头和纸的距离太近！")
            return False
        else:
            return True

    def isHandDistance(self):  # 判断手到笔尖的距离
        if self.__handDistance < HAND_LOW_DISTANCE:
            print("手握距离太近！")
        elif self.__handDistance > HAND_HIGH_DISTANCE:
            print("手握距离太远！")
        else:
            return True

    def isLux(self):  # 判断环境亮度
        if self.__lux > HIGH_LUX:
            print("亮度太高！")
            return False
        elif self.__lux < LOW_LUX:
            print("亮度太低！")
            return False
        else:
            return True

    def getTime(self):  # 获取当前时间
        # self.__time = timeFormat(self.__time）
        # 时间戳转换方法（未实现）
        return self.__time

    def getMessageID(self):  # 获取当前消息编号，用于唯一标识消息对象
        return self.__id

    def __init__(self, data):  # data为mysql单条查询结果 将字段拆分后使用构造方法封装到message对象
        self.__time = data[0]
        self.__id = data[1]
        self.__handDistance = data[2]
        self.__headDistance = data[3]
        self.__lux = data[4]
