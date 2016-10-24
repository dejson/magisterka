import math


class MySet(object):

    def __init__(self, p=None):
        self._point_list = []


        self._len = 0
        self._K = 0
        self._ex = 0.0
        self._ex2 = 0.0

        if p is not None:
            self.append(p)

    def append(self, p):
        self._point_list.append(p)
        if (self._len == 0):
            self._K = p.z

        self._len += 1
        self._ex += p.z - self._K
        self._ex2 += (p.z - self._K) * (p.z - self._K)

    def average(self):
        if self._len > 0:
            return self._K + self._ex / float(self._len)
        else:
            return 0.0

    def sd(self):
        if self._len > 1:
            return math.sqrt(
                    (self._ex2 - (self._ex * self._ex)/float(self._len)) / (float(self._len -1))
                    )
        else:
            return 0.0

    def get_list(self):
        return self._point_list

    def len(self):
        return self._len

    def set_list(self, l):
        if len(l) == 0:
            return 

        for p in l:
            self.append(p)

    def delete_point(self, p):
        self._point_list.remove(p)

        self._len -= 1

        if self._len == 0:
            self._ex = 0.0
            self._ex2 = 0.0
            self._K = 0.0
            return

        self._ex -= (p.z - self._K)
        self._ex2 -= (p.z - self._K) * (p.z - self._K)

    def join(self, s):
        for p in s.get_list():
            s.delete_point(p)
            self.append(p)
            p.set_list = self
