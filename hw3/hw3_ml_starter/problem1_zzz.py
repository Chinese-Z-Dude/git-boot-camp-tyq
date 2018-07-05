import pandas as pd
from numpy import dot
from visualize import visualize_scatter

learning_rate = 0.2
epoch = 30 # number of iteration for training
unit_step = lambda x: -1 if x < 0 else 1

def train(data):
    w = [0, 0, 0]
    X = data.iloc[:, 0 : 2]
    y = data.iloc[:, 2]
    result = [list(w)]
    for i in xrange(epoch):
        for index, x in X.iterrows():
            pred = unit_step(dot(x, w[0 : 2]) + w[2])
            # print "epoch" + str(i) + ": expect = " + str(y[index]) + " predict = " + str(pred)
            w[0] += learning_rate * (y[index] - pred) * x[0]
            w[1] += learning_rate * (y[index] - pred) * x[1]
            w[2] += learning_rate * (y[index] - pred)
        result.append(list(w))
    result = pd.DataFrame(result)
    # print result
    result.to_csv("p1_output.csv", header = None, index = False)
    return w

def main():
    data = pd.read_csv('input1.csv', header=None)
    w = train(data)
    visualize_scatter(data, weights = w)

if __name__ == "__main__":
    main()
