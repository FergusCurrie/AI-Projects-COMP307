import sys
import math
import random

# Returns euclidean distance between test and training point
def get_distance(pointa,line,r):
    # Convert line from line into array of point data -> pointb
    pointb = line.split(" ")
    distance = 0
    for x in range(0,len(pointa)-1):
        distance += ((float(pointa[x]) - float(pointb[x]))**2)/(r[x]**2)
    distance = math.sqrt(distance)
    return distance

# Main KMC algorthim
def kmc(k):
    print()
    # Combine data sets ( assuming 'use the wine data set' means this )
    wine = []
    for line_test in file_testset:
        if not line_test[0].isalpha():
            wine.append(line_test)
    for line_training in file_trainingset:
        if not line_training[0].isalpha():
             wine.append(line_training)

    # Calculate range
    rng = []
    for x in range(0, 13):
        highest = float(-1)
        lowest = sys.float_info.max
        for line in wine:
            if not line[0].isalpha():
                value = float(line.split(" ")[x])
                if value > highest: highest = value
                if value < lowest: lowest = value
        rng.append(highest - lowest)

    # Choose three random points as means
    means = []
    for i in range(0,k):
        ri = int(random.random() * len(wine))
        means.append(wine[ri].split(" "))

    # Loop until means are  not changing
    changing = True
    clusters = []
    while changing:
        # Cluster instances
        clusters = []
        for x in range(0,k):
            clusters.append([])
        for line in wine:
            # Find instance's closest mean
            dist = get_distance(means[0],line,rng)
            i = 0
            for m in range(0,len(means)):
                if get_distance(means[m],line,rng) < dist:
                    dist = get_distance(means[m],line,rng)
                    i = m
            clusters[i].append(line)
        # Calculate new means
        new_means = []
        for cluster in clusters:
            count = 0
            total = [0,0,0,0,0,0,0,0,0,0,0,0,0]
            for element in cluster:
                count += 1
                element_array = element.split(" ")
                element_array.pop(13)
                for i in range(0,len(element_array)):
                    total[i] += float(element_array[i])
            new_mean = [0,0,0,0,0,0,0,0,0,0,0,0,0]
            for i in range(0,len(new_mean)):
                new_mean[i] = total[i]/count
            new_means.append(new_mean)
        # Check if means are still changing
        changing = False
        for mi in range(0,k):
            for ei in range(0,13):
                if means[mi][ei] != new_means[mi][ei]:
                    changing = True
        # Set means to new means
        means = new_means
    # Calculate accuracy
    cluster_size = []
    for c in clusters:
        cluster_size.append(len(c))
    print(" For k = ",k," the number of instances in each cluster are : ",cluster_size)

# Open file
file_testset = open(sys.argv[2],"r")
file_trainingset = open(sys.argv[1],"r")

# Run knn
kmc(5)