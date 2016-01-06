# -*- coding: utf-8 -*-
"""
Created on Tue Jan 05 22:29:51 2016

@author: simon
"""

#knn演算法
def knn():
    from sklearn import datasets
    import numpy as np
    iris = datasets.load_iris()
    iris_X = iris.data
    iris_Y = iris.target
    np.random.seed(0)
    indices = np.random.permutation(len(iris_X))
    iris_X_train = iris_X[indices[:-10]]
    iris_Y_train = iris_Y[indices[:-10]]
    iris_X_test = iris_X[indices[-10:]]
    iris_Y_test = iris_Y[indices[-10:]]
    from sklearn.neighbors import KNeighborsClassifier
    knn = KNeighborsClassifier()
    knn.fit(iris_X_train,iris_Y_train)
    knn.predict(iris_X_test)
    print(iris_Y_test)
 
def decisiontree(): 
    #決策樹演算法
    from sklearn import datasets
    import numpy as np
    from sklearn import tree
    iris = datasets.load_iris()
    iris_X = iris.data
    iris_Y = iris.target
    np.random.seed(0)
    indices = np.random.permutation(len(iris_X))
    iris_X_train = iris_X[indices[:-10]]
    iris_Y_train = iris_Y[indices[:-10]]
    iris_X_test = iris_X[indices[-10:]]
    iris_Y_test = iris_Y[indices[-10:]]
    clf = tree.DecisionTreeClassifier()
    clf.fit(iris_X_train,iris_Y_train)
    from sklearn.externals.six import StringIO
    tree.export_graphviz(clf)
    clf.predict(iris_X_test)
    print(iris_Y_test)

knn()
decisiontree()