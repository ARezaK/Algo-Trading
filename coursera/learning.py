from __future__ import division
from numpy import loadtxt, zeros, ones, array, linspace, logspace, array, transpose
from pylab import scatter, show, title, xlabel, ylabel, plot, contour
import numpy as np
import matplotlib.pyplot as plt, mpld3

# https://github.com/JWarmenhoven/Coursera-Machine-Learning/blob/master/notebooks/Programming%20Exercise%201%20-%20Linear%20Regression.ipynb


def hypothesis_function(theta, x_):
    #return theta[0]*x_[0] + theta[1]*x_[1]
    #return np.transpose(theta).dot(x_)
    return x_.dot(theta)

def compute_cost(x_,y_,theta):
    # # for a given theta 0 and tehta 1 determine teh cost fucntion
    # samples_size = y_.size
    #
    #
    # H = hypothesis_function(theta,x_)
    # sqErrors = np.subtract(H, y_) # it looks like its putting everything into the first elemtn?
    # #sqErrors = (predictions - y_)
    # sqErrors = np.square(sqErrors)
    #
    # J = (1.0/(2*samples_size)) * sqErrors[0].sum() # so i just grab everythign in tehf irst element and use that. WTF
    # print "cost fucntion is: ", J
    # return J

    m = y_.size
    J = 0

    h = x_.dot(theta)

    J = 1 / (2 * m) * np.sum(np.square(h - y_))
    print J
    return (J) # thats interseting. using this guys code I get 3111 as teh cost function intially. which is the same problem I had before


def gradient_descent(alpha, iterations, x_, y_, theta):
    m = y_.size
    J_history = np.zeros(iterations)

    for iter in np.arange(iterations):
        h = x_.dot(theta)
        theta = theta - alpha * (1 / m) * (x_.T.dot(h - y_))
        J_history[iter] = compute_cost(x_, y_, theta)
    #print theta, J_history
    print('theta: ', theta.ravel())
    return (theta, J_history)
    # cost_function_history = zeros(shape=(int(iterations), 1))
    # sample_size = y_.size
    # theta_temps = zeros(shape=(theta.size, 1))
    #
    #
    # for i in range(iterations):
    #
    #
    #     for num in range(theta.size):
    #         predictions = array([hypothesis_function(theta, x__)for x__ in x_])
    #         whatev = np.subtract(predictions, y_)
    #
    #         whatev = np.multiply(whatev[0],x_[:,num]) # again it puts everything into the first element so
    #         whatev = whatev.sum()
    #         whatev = whatev * (alpha)
    #         whatev = whatev * (1.0/sample_size)
    #
    #         theta_temps[num][0] = theta[num] - whatev
    #
    #     print theta_temps
    #     theta = theta_temps
    #
    #     cost_function_history[i] = compute_cost(x_,y_, theta=theta)
    #
    # print cost_function_history
    # print theta



f = loadtxt('ex1data1.txt', delimiter=',', dtype=np.float64)
print("f: " )
#print(f)

#test = np.hsplit(f,2) # split it donw vertically?
column_one = f[:, 0]
column_two = f[:, 1]
print column_two


#Add a column of ones to X (interception data)
it = ones(shape=(97, 2))

it[:, 1] = column_one
#it[:, 1] = test[0]

#print it



#plt.scatter(x, y, alpha=1)
#plt.show()


#lets try this guys example
it = np.c_[np.ones(f.shape[0]),f[:,0]]
column_two = np.c_[f[:,1]] ## WTF IT WORKS NOW IF I USE THIS GUYS EXAMPLE>
print "-"*40
print column_two



thetas = zeros(shape=(2,1))
alpha = 0.01
iterations = 1500



compute_cost(it,column_two,thetas)
#compute_cost(it,test[1],thetas)
gradient_descent(alpha, iterations, it, column_two, thetas)