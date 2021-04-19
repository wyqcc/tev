"""


"""
from math import log


class TevAlgorithm:
    def __init__(self, current_average: float = None, other_average: float = None,
                 other_existence: bool = False, TEV: bool = True, other_tev_30: float = None,
                 other_ae_30: float = None, other_all_average_TEV: float = None, other_all_average_AE: float = None):
        """
        :param current_average:     当前设备当前传感器平均放电幅值
        :param other_average:     当前设备其他传感器平均放电幅值
        :param TEV:  当前设备数据是否为TEV
        :param other_existence:  存在其他检测设备
        :param other_tev_30:  其他设备的传感器TEV
        :param other_ae_30:  其他设备的传感器AE
        :param other_all_average_TEV:  其他所有设备的平均信号强度
        """
        if int(current_average) < 1:
            self.__current_average = 0.1  # 判断预警值是否小于1不能影响对数判断
        else:
            self.__current_average = current_average
        self.__other_average = other_average

        if int(other_average) < 1:
            self.__other_average = 0.1  # 判断预警值是否小于1不能影响对数判断
        else:
            self.__other_average = other_average
        self.__other_existence = other_existence

        self.__other_tev_30 = other_tev_30
        self.__other_ae_30 = other_ae_30
        self.__TEV = TEV
        self.__P1 = 20 * log(((int(self.__current_average) - 24.04) / 5.08), 10)
        if other_existence:
            self.__P2 = 20 * log(((int(self.__other_average) - 24.04) / 5.08), 10)
        if self.__TEV:
            self.__P3 = int(self.__P1) * 0.7 + int(self.__P2) * 0.3
        else:
            self.__P3 = int(self.__P2) * 0.7 + int(self.__P1) * 0.3
        self.__other_all_average_TEV = other_all_average_TEV
        self.__other_all_average_AE = other_all_average_AE

        self.__ST1 = 1
        self.__ST2 = 1
        self.__ST3 = 1
        self.__Grade = 1

    def cabinet_warning(self):

        if self.__P1 <= 25:
            self.__Grade = 3  # 返回正常
        else:
            if (self.__P1 <= 55) == (self.__P2 <= 55) and self.__other_average is not None:
                if self.__P3 <= 25:
                    self.__Grade = 1
                elif self.__P3 <= 55:
                    self.__Grade = 2
                else:
                    self.__Grade = 3

            else:
                if self.prices(self.__P1, self.__P1, self.__TEV) == 1:
                    self.__Grade = 1

                else:
                    if self.flourish(self.__P1) == 2:
                        self.__Grade = 2
                    else:
                        self.__Grade = 3
        return self.__Grade

    """
    置信度方程：
    正常方程：
    x<=20 y=1
    y=0-(1/10)*x+3
    注意方程1：
    30<=x<=50 y=1
    y=(1/10)*x-2
    注意方程2：
    30<=x<=50 y=1
    y=0-(1/10)*x+6
    警告方程：
    x>=60 y=1
    y=(1/10)*x-5
    """

    def prices(self, now, old, now_sensor_type):
        """
        :param now:
        :param old:
        :param now_sensor_type:
        :return:
        """
        if not now_sensor_type:
            now, old = old, now
        SNOW = self.sachet(now)
        SOLD = self.sachet(old)
        SNOW1, SNOW2, SNOW3 = SNOW[0], SNOW[1], SNOW[2]
        SOLD1, SOLD2, SOLD3 = SOLD[0], SOLD[1], SOLD[2]
        S1 = SNOW1 * 0.7 + SOLD1 * 0.3
        S2 = SNOW2 * 0.7 + SOLD2 * 0.3
        S3 = SNOW3 * 0.7 + SOLD3 * 0.3
        list_max = [S1, S2, S3]
        return list_max.index(max(list_max))

    def sachet(self, past):
        """
        :param past:int
        :return:ST1,ST2,ST3-->置信度1,置信度2，置信度3
        """

        if past <= 20:
            self.__ST1 = 1
        elif 20 <= past <= 30:
            self.__ST1 = 0 - (1 / 10) * past + 3
        if 30 <= past <= 50:
            self.__ST2 = 1
        elif 20 <= past <= 30:
            self.__ST2 = (1 / 10) * past - 2
        elif 50 <= past <= 60:
            self.__ST2 = 0 - (1 / 10) * past + 6
        if 60 <= past:
            self.__ST3 = 1
        elif 50 <= past <= 60:
            self.__ST3 = (1 / 10) * past - 5
        return self.__ST1, self.__ST2, self.__ST3

    # 第四阶段预警
    def flourish(self, P1):
        # Px = 0
        # Mx = 0
        # 判定多设备
        if self.__other_existence:
            # 纵向多设备加权

            ps1 = self.__other_tev_30 * 0.7 + self.__other_ae_30 * 0.3
            Px = (P1 - ps1) / ps1

            # 横向多设备加权
            mx_tev = (P1 - 20 * log(((int(self.__other_all_average_TEV) - 24.04) / 5.08), 10)) / 20 * log(
                ((int(self.__other_all_average_TEV) - 24.04) / 5.08), 10)

            mx_ae = (20 * log(((int(self.__other_average) - 24.04) / 5.08), 10) - 20 * log(
                ((int(self.__other_all_average_AE) - 24.04) / 5.08), 10)) / 20 * log(
                ((int(self.__other_all_average_AE) - 24.04) / 5.08), 10)

            Mx = mx_ae * 0.7 + mx_tev * 0.3
        else:
            pxT = 20 * log(((int(self.__other_tev_30) - 24.04) / 5.08), 10)
            Px = (P1 - pxT) / pxT
            OTHER = 20 * log(((int(self.__other_average) - 24.04) / 5.08), 10)
            OTHARc = 20 * log(
                ((int(self.__other_all_average_TEV) - 24.04) / 5.08), 10)
            Mx = (OTHER - OTHARc) / OTHER
        if Px > 0.5 or Mx > 0.5:
            self.__Grade = 3
