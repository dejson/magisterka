from script import *
import sys
import pickle
import array
import shapely.geometry


def num(s):
    try:
        return int(s)
    except ValueError:
        return float(s)


def main(arg_list):

    input_file = arg_list[0]
    scale = num(arg_list[1])
    min_set_size = 100 / scale

    points = read_from_file(input_file)
    p_map, dx, dy = get_map(points)
    set_list = neighbours(p_map, int(dy), int(dx))

    print(len(set_list))
    set_list = [x for x in set_list if len(x) >= min_set_size]
    print(len(set_list))

    last_list = []
    for s in set_list:
        try:
            x, y = alpha_shape(s, 0.4)
            if type(x) != shapely.geometry.polygon.Polygon:
                x, y = alpha_shape(s, 0.1)

            mean = sum(point.z for point in s) / len(s)
            a, b = x.boundary.coords.xy
            c = array.array('d', [mean for _ in range(0,len(a))])
            last_list.append((a, b, c))
            print("done")
        except:
            print("tego se ne udalo")

    filename = arg_list[2]
    with open(filename, 'wb') as f:
        pickle.dump(last_list, f)    


if __name__ == "__main__":
    main(sys.argv[1:])
