import math


class MyPoint(object):

    def __init__(self, x=0, y=0,z=0, point_set=None, classification=0):
        self.x = x
        self.y = y
        self.z = z
        self.point_set = point_set
        self.classification = classification & 31

    def get_distance(self, p):
        dx = abs(self.x - p.x)
        dy = abs(self.y - p.y)
        dz = abs(self.z - p.z)

        return math.sqrt(dx*dx + dy*dy + dz*dz)

    def is_neighbour(self, p, C=0.5, classify=False):
        distance = self.get_distance(p)

        if distance < C:
            return True
        elif classify and distance < C*2 and self.classification == p.classification and self.classification != 0:
            return True

        return False
