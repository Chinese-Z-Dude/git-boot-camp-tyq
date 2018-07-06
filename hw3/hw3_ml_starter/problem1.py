import pandas as pd
import numpy as np
from numpy import dot
from visualize import visualize_scatter
import argparse

learning_rate = 0.2 # learning_rate of the perceptron
epoch = 30 # number of iteration for training
unit_step = lambda x: -1 if x < 0 else 1 # classified the prediction

# training the perceptron
def train(data, output):
    w = [0, 0, 0]
    X = data.iloc[:, 0 : 2]
    y = data.iloc[:, 2]
    result = np.zeros((epoch, 3))
    for i in xrange(epoch):
        for index, x in X.iterrows():
            pred = unit_step(dot(x, w[0 : 2]) + w[2])
            # print "epoch" + str(i) + ": expect = " + str(y[index]) + " predict = " + str(pred)
            w[0] += learning_rate * (y[index] - pred) * x[0]
            w[1] += learning_rate * (y[index] - pred) * x[1]
            w[2] += learning_rate * (y[index] - pred)
        result[i] = np.around(w, 3)
    result = pd.DataFrame(result)
    # print result
    result.to_csv(str(output), header = None, index = False)
    return w

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input')
    parser.add_argument('output')
    parser.add_argument('--visual', action = 'store_true')
    args = parser.parse_args()

    data = pd.read_csv(args.input, header=None)
    w = train(data, args.output)
    if args.visual:
        visualize_scatter(data, weights = w)

if __name__ == "__main__":
    main()
