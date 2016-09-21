import math


class MySet(object):

    def __init__(self, p=None):
        self._point_list = []

        self._average = 0.0
        self._sd = 0.0
        self._sum = 0.0

        if p is not None:
            self.append(p)

    def append(self, p):
        self._point_list.append(p)
        lenght = float(len(self._point_list))
        self._sum += p.z
        self._average = self._sum / lenght

        x = len(self._point_list)
        # calculate standard derrivation
        if x > 1:
            self._calculate_sd(lenght)

    def _calculate_sd(self, lenght):
        s = sum((p.z - self._average) ** 2 for p in self._point_list)
        self._sd = math.sqrt(s/lenght)

    def average(self):
        return self._average

    def sd(self):
        return self._sd

    def get_list(self):
        return self._point_list

    def delete_point(self, p):
        self._point_list.remove(p)
        lenght = len(self._point_list)

        if lenght == 0:
            return

        lenght = float(lenght)
        self._sum -= p.z
        self._average = self._sum / lenght

        x = len(self._point_list)
        # calculate standard derrivation
        if x > 1:
            self._calculate_sd(lenght)
        else:
            self._sd = 0.0
