import pandas as pd
import numpy as np
import visualize as v
import matplotlib.pyplot as plt
import matplotlib.lines as mlines

alpha = [0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1, 5, 10]

def train(X, y):
    result = np.zeros((len(alpha), 5))
    for i in xrange(len(alpha)):
        result[i][0 : 2] = [alpha[i], 100]
        w = [0, 0, 0]
        for j in xrange(100):
            err = np.dot(X, w) - y
            for k in xrange(len(w)):
                w[k] = w[k] - (1.0 * alpha[i] / y.size) * sum(X[:, k] * err)
        # print "alpha is " + str(alpha[i]) + " " + str(w)
        result[i][2: 5] = w

    result = pd.DataFrame(result)
    return result
    # print result

def print_fet(df, w):
    print w
    for i in xrange(2):
        ax = df.plot(x = i, y = 2, kind='scatter')
        xmin, xmax = ax.get_xlim()

        def y(x):
            return w[i + 1] * x + w[0]

        line_start = (xmin, xmax)
        line_end = (y(xmin), y(xmax))
        print xmin, xmax, y(xmin), y(xmax)
        line = mlines.Line2D(line_start, line_end, color='red')
        ax.add_line(line)
        plt.show()

def main():
    data = pd.read_csv("input2.csv", header = None)
    mat = data.values

    # normalized data
    for i in range(0, mat.shape[1] - 1):
        stdev = np.std(mat[:, i])
        mean = np.mean(mat[:, i])
        for j in range(0, mat.shape[0]):
            mat[j, i] = (mat[j, i] - mean) / stdev

    data = pd.DataFrame(mat)
    X = np.ones((mat.shape[0], 3))
    X[:, 1 : ] = mat[:, 0 : 2]
    y = mat[:, 2]

    # print X
    #
    # print y

    result = train(X, y)

    # print data[0]
    # print data[1]
    # ax = plt.figure().gca(projection='3d')
    # plt.hold(True)
    # ax.scatter(data[0], data[1], data[2])
    # plt.show()

    r = result.values
    # print r
    # print r
    # print r[3]
    # print r[3][2:5]
    for i in xrange(len(alpha)):
        print_fet(data, r[i][2:5])
    # v.visualize_3d(data, lin_reg_weights = r[3][2:5],
                   # xlim = (1, 9), ylim = (5, 45), zlim = (0.7, 1.5))

    # for i in xrange(result.shape[0]):
    #     v.visualize_3d(data, lin_reg_weights=result.iloc[i, :])

if __name__ == "__main__":
    main()
