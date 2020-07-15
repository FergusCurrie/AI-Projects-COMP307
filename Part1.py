import random

def calc_y(x):
    summ = 0
    for i in range(0,m+1):
        summ += weight[i] * x[i]
    if summ > 0:
        return 1
    else:
        return 0

def epoch():
    # Open data and skip headings on first line
    data = open("dataset", "r")
    next(data)
    correct = 0
    for line in data:
        # Find d and y
        line_data = line.split(" ")
        line_data = [float(line_data[ii].strip()) for ii in range(0,len(line_data))]
        d = line_data[len(line_data)-1]
        del line_data[len(line_data)-1]
        line_data.insert(0,1) #bias
        #print(line_data)
        y = calc_y(line_data)

        # For calculating accuracy
        if y == d:
            correct += 1

        # Adjust weights
        for ii in range(1, m+1):
            weight[ii] = weight[ii] + (n * (d - y) * line_data[ii])
    return correct


# Open file , run with command $ python Part1.py
n = 0.2
m = 3
weight = [random.random(),random.random(),random.random(),random.random()]

# Do 200 epoch
for z in range(0,200):
    epoch()

# Accuracy
print("Accuracy Part 1 = ",epoch()/8)







