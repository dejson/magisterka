from shapely.ops import cascaded_union, polygonize
import shapely.geometry as geometry
from scipy.spatial import Delaunay
import numpy as np
import math
import random
from liblas import file
from my_point import MyPoint
import progressbar
 
def alpha_shape(points, alpha):
    """
    Compute the alpha shape (concave hull) of a set
    of points.
 
    @param points: Iterable container of points.
    @param alpha: alpha value to influence the
        gooeyness of the border. Smaller numbers
        don't fall inward as much as larger numbers.
        Too large, and you lose everything!
    """
    if len(points) < 4:
        # When you have a triangle, there is no sense
        # in computing an alpha shape.
        return geometry.MultiPoint(list(points)).convex_hull
 
    def add_edge(edges, edge_points, coords, i, j):
        """
        Add a line between the i-th and j-th points,
        if not in the list already
        """
        if (i, j) in edges or (j, i) in edges:
             # already added
            return
        edges.add( (i, j) )
        edge_points.append(coords[ [i, j] ])
 
    coords = np.array([[point.x, point.y]
                       for point in points])
 
    tri = Delaunay(coords)
    edges = set()
    edge_points = []
    # loop over triangles:
    # ia, ib, ic = indices of corner points of the
    # triangle
    for ia, ib, ic in tri.vertices:
        pa = coords[ia]
        pb = coords[ib]
        pc = coords[ic]
 
        # Lengths of sides of triangle
        a = math.sqrt((pa[0]-pb[0])**2 + (pa[1]-pb[1])**2)
        b = math.sqrt((pb[0]-pc[0])**2 + (pb[1]-pc[1])**2)
        c = math.sqrt((pc[0]-pa[0])**2 + (pc[1]-pa[1])**2)
 
        # Semiperimeter of triangle
        s = (a + b + c)/2.0
 
        # Area of triangle by Heron's formula
        area = math.sqrt(s*(s-a)*(s-b)*(s-c))
        circum_r = a*b*c/(4.0*area)
 
        # Here's the radius filter.
        #print circum_r
        if circum_r < 1.0/alpha:
            add_edge(edges, edge_points, coords, ia, ib)
            add_edge(edges, edge_points, coords, ib, ic)
            add_edge(edges, edge_points, coords, ic, ia)
 
    m = geometry.MultiLineString(edge_points)
    triangles = list(polygonize(m))
    return cascaded_union(triangles), edge_points


def get_map(points):
    X = [p.x for p in points]
    Y = [p.y for p in points]

    xmin = math.floor(min(X))
    dx = math.ceil(math.ceil(max(X)) - min(X))

    ymin = math.floor(min(Y))
    dy = math.ceil(math.ceil(max(Y)) - min(Y))

    l = [[ [] for _ in range(0,int(dx))] for _ in range(0,int(dy))]

    bar = progressbar.ProgressBar()
    for p in bar(points):
        x = int(math.floor(p.x - xmin))
        y = int(math.floor(p.y - ymin))
        l[y][x].append(p)

    return l, xmin, ymin


def read_from_file(name):
    points = []
    try:
        bar = progressbar.ProgressBar()
        f = file.File(name)
        for p in bar(f):
            points.append(MyPoint(p.x, p.y, p.z, classification=p.classification))
    except Exception as e:
        print("Teribble exception %s" % str(e))
    finally:
        f.close()

    return points


def get_distance(p, q):
    x = abs(p[0] - q[0])
    y = abs(p[1] - q[1])
    z = abs(p[2] - q[2])

    d = math.sqrt(x*x + y*y + z*z)

    return d


def find_neighbour(l, p, a, b, d, xmax, ymax, set_list):
    """
    l - point map
    p - point
    a,b - quad that point p is in
    s - set that point p is in
    d - distance
    """

    x = p.x - math.floor(p.x)
    y = p.y - math.floor(p.y)

    if x - d < 0:
        x = -1
    else:
        x = 1

    if y - d < 0:
        y = -1
    else:
        y = 1

    n = []
    n.append(l[a][b])
    if ymax > a+y >=0:
        n.append(l[a+y][b])
    if xmax > b+x >=0:
        n.append(l[a][b+x])
    if  ymax > a+y >=0 and xmax > b+x >=0:
        n.append(l[a+y][b+x])

    usless_x = 0

    for n_list in n:
        for point in n_list:
            if point is not p:
                if p.is_neighbour(point):
                    if point.point_set is None:
                        set_list[p.point_set].append(point)
                        point.point_set = p.point_set
                        usless_x = 2
                    elif point.point_set != p.point_set:
                        union_sets(point.point_set, p.point_set, set_list)
                        usless_x = 1
                    else:
                        usless_x = 0


def union_sets(p, q, set_list):
    if len(set_list[p]) > len(set_list[q]):
        main_index = p
        small_index = q
    else:
        main_index = q
        small_index = p

    index = main_index
    for point in set_list[small_index]:
        set_list[main_index].append(point)
        point.point_set = index

    set_list[small_index] = []

def neighbours(l):
    set_list = []
    bar = progressbar.ProgressBar()
    for i in bar(range(0,583)):
        for j in range(0,512):
            for p in l[i][j]:
                if p.point_set is None:
                    s = [p]
                    set_list.append(s)
                    p.point_set = len(set_list) - 1
                find_neighbour(l, p, i, j, 0.5, 582,511, set_list)
    return set_list


def get_random(r):
    x = r.random()
    y = r.random()

    if x < 0.4 or x > 0.6 or y < 0.4 or y > 0.6:
        return [x * 10.0, y*10.0, 0, None]
    else:
        return [x*10.0, y*10.0, 1, None]


class PSet(object):

    def __init__(self):
        self._height = 0
        self._points = []

    def add_point(self, point):
        self._points.append(point)

    def get_boundaries(self):
        pass


