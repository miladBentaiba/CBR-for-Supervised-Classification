from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC, LinearSVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import Perceptron
from sklearn.linear_model import SGDClassifier
from sklearn.tree import DecisionTreeClassifier
from random import shuffle


import init
from constants import ALL_FEATURES, SOLUTION


S = init.Singleton.get_instance()
_c = S.cursor()
_c.execute('select {1}, {0} from cases where expert = 1'.format(SOLUTION, ','.join(ALL_FEATURES)), ())
dictionaries_cases = []
results = _c.fetchall()
shuffle(results)
X_train = []
Y_train = []
X_test = []
Y_test = []
for i, row in enumerate(results):
    if i < 70:
        X_train.append([row[0], row[1], row[2], row[3], row[4]])
        Y_train.append(row[5])
    else:
        X_test.append([row[0], row[1], row[2], row[3], row[4]])
        Y_test.append(row[5])

# # Logistic Regression
# lg = LogisticRegression(random_state=0, solver='lbfgs', multi_class='multinomial')
# lg.fit(X_train, Y_train)
# acc_lg = round(lg.score(X_train, Y_train) * 100, 2)
# print(acc_lg) #98.57
# acc_lg = round(lg.score(X_test, Y_test) * 100, 2)
# print(acc_lg) #100

# # Support Vector Machines
# svc = SVC(kernel="sigmoid")
# svc.fit(X_train, Y_train)
# acc_svc = round(svc.score(X_train, Y_train) * 100, 2)
# print(acc_svc) #98.57 #100
# acc_svc = round(svc.score(X_test, Y_test) * 100, 2)
# print(acc_svc) #100   #96

# # K Nearest Neighbors
# knn = KNeighborsClassifier(n_neighbors=1, weights="distance")
# knn.fit(X_train, Y_train)
# acc_knn = round(knn.score(X_train, Y_train) * 100, 2)
# print(acc_knn) #100
# acc_knn = round(knn.score(X_test, Y_test) * 100, 2)
# print(acc_knn) #96 #100

# # Gaussian Naive Bayes
# gaussian = GaussianNB(var_smoothing=1e-09)
# gaussian.fit(X_train, Y_train)
# acc_gaussian = round(gaussian.score(X_train, Y_train) * 100, 2)
# print(acc_gaussian) #97.4
# acc_gaussian = round(gaussian.score(X_test, Y_test) * 100, 2)
# print(acc_gaussian) #96


# # Perceptron
# perceptron = Perceptron()
# perceptron.fit(X_train, Y_train)
# acc_perceptron = round(perceptron.score(X_train, Y_train) * 100, 2)
# print(acc_perceptron) #92.86
# acc_perceptron = round(perceptron.score(X_test, Y_test) * 100, 2)
# print(acc_perceptron) #92


# # Linear SVC
# linear_svc = LinearSVC(loss="hinge", multi_class="crammer_singer")
# linear_svc.fit(X_train, Y_train)
# acc_linear_svc = round(linear_svc.score(X_train, Y_train) * 100, 2)
# print(acc_linear_svc) #98.57
# acc_linear_svc = round(linear_svc.score(X_test, Y_test) * 100, 2)
# print(acc_linear_svc) #100


# # Stochastic Gradient Descent
# sgd = SGDClassifier()
# sgd.fit(X_train, Y_train)
# acc_sgd = round(sgd.score(X_train, Y_train) * 100, 2)
# print(acc_sgd) #94.29
# acc_sgd = round(sgd.score(X_test, Y_test) * 100, 2)
# print(acc_sgd) #92


# # Decision Tree
# decision_tree = DecisionTreeClassifier(criterion="entropy", splitter="random")
# decision_tree.fit(X_train, Y_train)
# acc_decision_tree = round(decision_tree.score(X_train, Y_train) * 100, 2)
# print(acc_decision_tree) #100
# acc_decision_tree = round(decision_tree.score(X_test, Y_test) * 100, 2)
# print(acc_decision_tree) #96


# Random Forest
random_forest = RandomForestClassifier(n_estimators=10)
random_forest.fit(X_train, Y_train)
random_forest.score(X_train, Y_train)
acc_random_forest = round(random_forest.score(X_train, Y_train) * 100, 2)
print(acc_random_forest) #100
acc_random_forest = round(random_forest.score(X_test, Y_test) * 100, 2)
print(acc_random_forest) #96
