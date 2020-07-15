import sys
import math

# Returns euclidean distance between test and training point
def get_distance(test_point,training_point,r):
    distance = 0
    test_nums = test_point.split(" ")
    training_nums = training_point.split(" ")
    for x in range(0,len(test_nums)-1):
        distance += ((float(test_nums[x]) - float(training_nums[x]))**2)/(r[x]**2)
    distance = math.sqrt(distance)
    return distance

def knn(k):
    correct = 0
    count = 0
    a_return = []

    # For looping a file consumes the file so I convert to list then nested loop through it
    array_test = []
    array_training = []
    for line_test in file_testset:
        array_test.append(line_test)
    for line_training in file_trainingset:
        array_training.append(line_training)

    # Finding range for normalising distance measure
    rng = []
    for x in range(0,13):
        highest = float(-1)
        lowest = sys.float_info.max
        for line_training in array_training:
            if not line_training[0].isalpha():
                value = float(line_training.split(" ")[x])
                if value > highest: highest = value
                if value < lowest: lowest = value
        rng.append(highest-lowest)
    # For all test points
    for line_test in array_test:
        # Get all distances into a list, a_distance is 2D array containing distance and classification
        a_distance = []
        bad_train = True
        for line_training in array_training:
            bad_train = (line_test[0].isalpha() or line_training[0].isalpha())
            if not bad_train:
                a_distance.append([get_distance(line_test,line_training,rng),line_training.split(" ")[13]])
        # Chose K smallest and make decision
        result = [0,0,0]
        if not bad_train:
            for kth in range(0,k):
                smallest = sys.float_info.max
                smallest_index = -1
                for x in range(0,len(a_distance)):
                    if a_distance[x][0] < smallest:
                        smallest = a_distance[x][0]
                        smallest_index = x
                i = int(a_distance[smallest_index][1])
                result[i-1] = result[i-1]+1
                a_distance.pop(smallest_index)
            # Check if classification correct
            largest = -1
            if result[0] > result[1] and result[0] > result[2]:
                largest = 1
            elif result[1] > result[2] and result[1] > result[0]:
                largest = 2
            else:
                largest = 3
            if largest == int(line_test.split(" ")[13]):
                correct += 1
            a_return.append(largest)
            count+=1
    return float(correct) / float(count)

##################################################################################

# Open file
file_testset = open(sys.argv[2],"r")
file_trainingset = open(sys.argv[1],"r")
# Run knn
k_value = 1
print("ACCURACY = ", knn(k_value)," with k =",k_value)

