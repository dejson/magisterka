import pickle
import matplotlib.pyplot as plt
import sys

def main(filename):
    with open(filename, 'rb') as f:
        l = pickle.load(f)

        for x in l:
            plt.plot(x[0], x[1])

        plt.show()


if __name__ == '__main__':
    main(sys.argv[1])
