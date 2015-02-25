import numpy as np
import matplotlib.pyplot as plt
import time
import mpl_toolkits.mplot3d as axes3d
from sklearn import decomposition
from sklearn import datasets, linear_model
from sklearn.pipeline import Pipeline
from sklearn.grid_search import GridSearchCV

logistic = linear_model.LogisticRegression()
pca = decomposition.PCA()
pipe = Pipeline(steps=[('pca',pca),('logistic',logistic)])
digits = datasets.load_digits()

#loading data from matlab
import matlab_wrapper

mat = matlab_wrapper.MatlabSession()

mat.eval("load cities")

categories = mat.get('categories')
ratings = mat.workspace.ratings

X_digits = ratings

####
pca.fit(X_digits)


"""
plt.figure(1, figsize=(4, 3))
plt.clf()
plt.axes([.2, .2, .7, .7])
plt.plot(pca.explained_variance_, linewidth=2)
plt.axis('tight')
plt.xlabel('N_components')
plt.ylabel("expalined_varaince")
plt.show()
time.sleep(20)
"""

transform = pca.transform(X_digits)



"""
np.random.seed(5)

centers = [[1, 1], [-1, -1], [1, -1]]

iris = datasets.load_iris()

X = iris.data
Y = iris.target

fig = plt.figure(1, figsize=(4,3))
plt.clf()

ax = axes3d(fig, rect=[0,0,.95, 1], elev=48, azim=134)

plt.cla()

pca = decomposition.PCA(n_components=3)
pca.fit(X)
new_X = pca.transform(X)

"""
