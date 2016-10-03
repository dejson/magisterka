from script import *
import matplotlib.pyplot as plt
import array
import copy
import time
import random
from my_point import MyPoint
from mpl_toolkits.mplot3d import Axes3D

def prepare_data(n):
    r = random.Random()
    result = []

    for _ in range(0, n):
        x = r.random()
        y = r.random()

        if x < 0.4 or x > 0.6 or y < 0.4 or y > 0.6:
            z = r.random() * 0.1
        else:
            z = r.random() * 0.1 + (x-0.4)*5

        result.append(MyPoint(x,y,z))

    return result

#data = get_random(1000)
data = prepare_data(1000)
b_data = copy.deepcopy(data)

def plot_points(data):
    data1 = filter(lambda p: p.z > 0.1, data)
    data2 = filter(lambda p: p.z <= 0.1, data)
    
    for d in [data1, data2]:
        c = 'ro' if d is data1 else 'bo'
    
        plt.plot(
                [p.x for p in d],
                [p.y for p in d],
                c
                )


plot_points(data)
plt.axis([-0.2, 1.2, -0.2, 1.2])
plt.show()

#3d plot

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

for p in data:
    c = 'r' if p.z > 0.1 else 'b'
    ax.scatter(p.x, p.y, p.z, c=c)

plt.show()

#test naive algorythm
start = time.time()

p_map, dx, dy = get_map(data)

set_list = neighbours(p_map, int(dy), int(dx))
set_list = [x for x in set_list if len(x) >= 4]
print len(set_list)

last_list = []
for s in set_list:
    x, y = alpha_shape(s, 0.4)

    mean = sum(point.z for point in s) / len(s)
    a, b = x.boundary.coords.xy
    c = array.array('d', [mean for _ in range(0,len(a))])
    last_list.append((a, b, c))

end = time.time()

print("Algorytm naiwny: " + str((end - start)))

plot_points(data)
for p in last_list:
    plt.plot( p[0], p[1], linewidth=2.0)

plt.axis([-0.2, 1.2, -0.2, 1.2])
plt.show()

# lagorytm iteracyjny
data = copy.deepcopy(b_data)

start = time.time()

p_map, dx, dy = get_map(data)

set_list = []
set_list = neighbours_std(p_map, int(dy), int(dx), set_list)
f_list = [x.get_list() for x in set_list if len(x.get_list()) >= 4]
print len(f_list)

last_list = []
for s in f_list:
    x, y = alpha_shape(s, 0.4)

    mean = sum(point.z for point in s) / len(s)
    a, b = x.boundary.coords.xy
    c = array.array('d', [mean for _ in range(0,len(a))])
    last_list.append((a, b, c))

iter1 = time.time()

plot_points(data)
for p in last_list:
    plt.plot( p[0], p[1], linewidth=2.0)

plt.axis([-0.2, 1.2, -0.2, 1.2])
plt.show()


#druga runda
for _ in range(1,7):
    set_list = neighbours_std(p_map, int(dy), int(dx), set_list)
f_list = [x.get_list() for x in set_list if len(x.get_list()) >= 4]
print len(f_list)

last_list = []
for s in f_list:
    x, y = alpha_shape(s, 0.4)

    mean = sum(point.z for point in s) / len(s)
    a, b = x.boundary.coords.xy
    c = array.array('d', [mean for _ in range(0,len(a))])
    last_list.append((a, b, c))

end = time.time()

print("Pierwsza iteracja: " + str((iter1 - start)))
print("Iteracyjny: " + str((end - start)))

plot_points(data)
for p in last_list:
    plt.plot( p[0], p[1], linewidth=2.0)

plt.axis([-0.2, 1.2, -0.2, 1.2])
plt.show()
