import pandas as pd
import numpy as np
import visualize as v
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import argparse

alpha = [0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1, 5, 10] # list of alpha value

# training the linear model
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
        result[i][2: 5] = np.around(w, 3)

    result = pd.DataFrame(result)
    return result
    # print result

# visualize the linear model by each feature 
def print_fet(df, r):
    w = r[2:5]
    for i in xrange(2):
        ax = df.plot(x = i, y = 2, kind='scatter')
        xmin, xmax = ax.get_xlim()

        def y(x):
            return w[i + 1] * x + w[0]

        line_start = (xmin, xmax)
        line_end = (y(xmin), y(xmax))
        line = mlines.Line2D(line_start, line_end, color='red')
        ax.add_line(line)
        ax.set_title('alpha' + str(r[0]) + "feature" + str(i + 1))
        plt.show()
        # plt.savefig('alpha' + str(r[0]) + "feature" + str(i + 1) + ".png")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input')
    parser.add_argument('output')
    parser.add_argument('--visual', action = 'store_true')
    args = parser.parse_args()

    data = pd.read_csv(args.input, header = None)
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
    r = train(X, y).values

    # when alphs is 1 the model has best result thus choose it as the answer
    r = np.append(r, [r[6]], axis = 0)
    pd.DataFrame(r).to_csv(args.output, header = None, index = False)

    if args.visual:
        for i in xrange(len(alpha)):
            print_fet(data, r[i])
            v.visualize_3d(data, lin_reg_weights = r[i][2:5], alpha = r[i][0])

if __name__ == "__main__":
    main()
