import random
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler

# Reads a file with param file name, returns x which is 2d array of inptus e,g [[x1,x2,...,xn],[x1,x2,...,xn]]
# and returns y which is array of target output d
def read(file_name):
    data = open(file_name,"r")
    x = []
    y = []
    next(data)
    correct = 0
    for line in data:
        # add line
        line_features = []
        line_data = line.split(" ")
        line_data = [float(line_data[ii].strip()) for ii in range(0,len(line_data))]
        for val in range(0,len(line_data)-1):
            line_features.append(line_data[val])
        ya = [0,0,0]
        ya[int(line_data[13])-1] = 1
        y.append(ya)
        x.append(line_features)
    return x,y

# Open file , run with command $ python Part2.py
num_inputs = 13
num_outputs = 3
learning_rate = 0.03
num_hidden_nodes = 13

# Get inputs and targets
training = read("wine_training")
test = read("wine_test")
x_train = training[0]
y_train = training[1]
x_test = test[0]
y_test = test[1]

# maybe solver lbfgs vs sgd - solver='lbfgs'
clf = MLPClassifier(hidden_layer_sizes = (num_hidden_nodes,),learning_rate_init = learning_rate,early_stopping = True,
                    max_iter = 800)


scaler = StandardScaler()
scaler.fit(x_train)
x_train = scaler.transform(x_train)
x_test = scaler.transform(x_test)
fitted = clf.fit(x_train,y_train)


accuracyTest = fitted.score(x_test,y_test)
accuracyTrain = fitted.score(x_train,y_train)
print("Accuracy test =",accuracyTest)
print("Accuracy training =",accuracyTrain)









