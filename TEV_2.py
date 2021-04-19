#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from math import log


class TevAlgorithm:
    def __init__(self, current_average: list = None, current_average_30: float = None,
                 other_current_average: float = None, current_all: list = None):
        """
        :param current_average:     当前设备当前传感器平均放电幅值 基本判断
        :param current_average_30: 当前设备30天前的平均放电幅值     横向分析
        :param other_current_average:当前其余所有设备平均放电幅值    纵向分析
        :param current_all:当前其余所有设备平均放电幅值    同排柜子的所有平均放电幅值 要求：元素不可小于1，如果小于一置为0.1
        """
        self.__current_average = current_average[0]
        self.__current_average_30 = current_average_30
        self.__other_current_average = other_current_average
        self.__current_all = current_all
        # if self.__current_average is not None:
        #     return ("on" + 'current_average',)
        if self.__current_average < 1.00:
            self.__current_average = 0.1
        self.__P_current_average = 20 * log(((int(self.__current_average) - 24.04) / 5.08), 10)
        self.__P_current_average_30 = None
        self.__P_other_current_average = None
        self.__Grade = 1
        self.Px = None
        self.Mx = None

    def diagnosis(self):
        if self.__P_current_average <= 25:
            self.__Grade = 1
        if self.__P_current_average <= 55:
            self.__Grade = 2
        else:
            self.__Grade = 3
        """
        当设备状态等级为“注意”及以上时，进行纵向分析与横向分析。
        纵向分析比较设备当前信号强度与该设备30天前的信号强度变化量，
        得到，其中PX为当前信号强度，P0为30天前的信号强度 
        PX%=(Px-P0)/P0
        """
        if self.__current_average_30 is not None:
            if self.__current_average_30 < 1.00:
                self.__current_average_30 = 0.1
            self.__P_current_average_30 = 20 * log(((int(self.__current_average_30) - 24.04) / 5.08), 10)
            self.Px = (self.__P_current_average - self.__P_current_average_30) / self.__P_current_average_30
        if self.__other_current_average is not None:
            if self.__other_current_average < 1.00:
                self.__other_current_average = 0.1
            self.__P_other_current_average = 20 * log(((int(self.__other_current_average) - 24.04) / 5.08), 10)
            self.Mx = (self.__P_current_average - self.__P_other_current_average) / self.__P_other_current_average

        if self.Mx and self.Px is None:
            return self.__Grade
        if self.Mx or self.Px >= 0.5:
            self.__Grade = 3
        return self.__Grade

    def influence_diagnosis(self):

        if type(self.__current_all) == list:
            # 先生成对应的信号强度列表P_list
            P_list = [20 * log(((int(install) - 24.04) / 5.08), 10) for install in self.__current_all]

            if P_list == P_list[::-1]:
                return (3,)
            List_max = max(P_list)
            Max_index = P_list.index(List_max)
            Cont_r = 0
            Cont_f = 0
            for install in range(Max_index, len(P_list) - 1):
                if Cont_r == 0:
                    print(P_list[install])
                else:
                    if P_list[install] < P_list[install - 1] and P_list[install - 1] - P_list[install] > 2:
                        Cont_r += 1
            for install in range(Max_index, 0, -1):
                if Cont_f == 0:
                    print(P_list[install])
                else:
                    if P_list[install] < P_list[install + 1] and P_list[install + 1] - P_list[install] > 2:
                        Cont_f += 1
            if Cont_r or Cont_f != 0:
                return Max_index, Cont_f, Cont_r
            else:
                return '存在异常干扰'
        else:
            return 'not list'


def tev_main(current_average: list = None, current_average_30: float = None,
             other_current_average: float = None, current_all: list = None):
    """
    生成对象
    :param current_average:
    :param current_average_30:
    :param other_current_average:
    :param current_all: 返回TevAlgorithm对象
    :return:
    """
    return TevAlgorithm(current_average=current_average, current_average_30=current_average_30,
                        other_current_average=other_current_average, current_all=current_all)


def tev_diagnosis(tev_algorithm=None):
    """
    当前预警诊断调用
    :param tev_algorithm: tev_main对象
    :return:
    """
    return tev_algorithm.influence_diagnosis()


def tev_influence_diagnosis(tev_algorithm=None):
    """
    横排柜子干扰诊断
    :param tev_algorithm:
    :return:
    """
    return tev_algorithm.diagnosis()


if __name__ == '__main__':
    # tev_main()
    # tev_diagnosis()
    # tev_influence_diagnosis()
    cps = TevAlgorithm(current_average=[200, 100], current_average_30=100, other_current_average=100,
                       current_all=[100, 200, 300, 200, 500])
    print(cps.influence_diagnosis())
