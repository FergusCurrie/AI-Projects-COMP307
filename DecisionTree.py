import sys
import math

# Class of instances => class of instance + data values
class Instance:
    def __init__(self,cl,avals):
        self.clas = cl
        self.att_vals = avals

    def get_att(self,index):
        return self.att_vals[index]

    def get_value(self,att):
        for ii in range(0,len(attribs)):
            if attribs[ii].strip() == att.strip():
                return self.att_vals[ii]

    def get_class(self):
        return self.clas

    def to_string(self):
        print("cat: ",self.clas,"  vals:",self.att_vals)

# Class for decision tree
class Node:
    def __init__(self):
        self.left = None
        self.right = None
        self.att = None
        self.leaf = False
        self.leaf_prob = None
        self.leaf_class = None

    def get_leaf(self):
        return self.leaf

    def draw_tree(self,indent):
        if not self.leaf:
            print(indent+self.att.strip()+" = True")
            self.left.draw_tree(indent+"---")
            print(indent+self.att.strip()+" = False")
            self.right.draw_tree(indent+"---")
        else:
            print(indent+" ",self.leaf_class," , with prob = ",self.leaf_prob)

    def impurity(self,instances):
        m = 0
        n = 0
        for i in instances:
            if i.get_class() == "live":
                m += 1
            if i.get_class() == "die":
                n += 1
        return (m*m)/((m+n)**2)

    def build_tree(self,instances,attributes,probability):
        # Stop conditions
        if len(instances) == 0 :
            self.leaf = True
            self.leaf_class = baseline
            self.leaf_prob = base_prob
            return self
        if self.impurity(instances) == 0 or self.impurity(instances) == 1:
            self.leaf = True
            self.leaf_class = instances[0].get_class().strip()
            self.leaf_prob = probability
            return self
        if len(attributes) == 0:
            self.leaf = True
            self.leaf_prob = probability
            num_live_ = 0
            for i in instances:
                if i.get_class().strip() == "live":
                    num_live_ += 1
            if num_live_ > len(instances) - num_live:
                self.leaf_class = "live"
            else:
                self.leaf_class = "die"
            return self

        # Find best attribute to continue tree with
        best_att = None
        best_true = None
        best_false = None
        best_prob_true = 0
        best_prob_false = 0
        best_purity = -1000
        for i_att in range(0,len(attributes)):
            # Split into true and false
            a_true = []
            a_false = []
            att = attributes[i_att]
            for inst in instances:
                if inst.get_att(i_att).strip() == "true" :
                    a_true.append(inst)
                elif inst.get_att(i_att).strip()  == "false":
                    a_false.append(inst)
                else:
                    print("ERROR")
            # Compute weighted purity using probabilty and purity
            prob_true = len(a_true) / len(instances)
            prob_false = len(a_false) / len(instances)
            weighted_purity_true = 0
            weighted_purity_false = 0
            if len(a_true) != 0:
                weighted_purity_true = self.impurity(a_true) * prob_true
            if len(a_false) != 0:
                weighted_purity_false = self.impurity(a_false) * prob_true
            weighted_purity = weighted_purity_true + weighted_purity_false
            # If better purity remember this instance as the best
            if weighted_purity > best_purity:
                best_att = att
                best_true = a_true
                best_false = a_false
                best_prob_true = prob_true
                best_prob_false = prob_false
                best_purity = weighted_purity
        # Build subtrees
        attributes.remove(best_att)
        attributes_clone = [item for item in attributes]
        self.left = Node().build_tree(best_true,attributes,probability*best_prob_true)
        self.right = Node().build_tree(best_false, attributes_clone,probability*best_prob_false)
        self.att = best_att
        return self

    def traverse(self,inst):
        if self.leaf:
            return self.leaf_class
        inst_att_value = inst.get_value(self.att)
        if inst_att_value == "true":
            return self.left.traverse(inst)
        if inst_att_value == "false":
            return self.right.traverse(inst)


def read():
    first = True
    attribute_names = []
    instances_training = []
    instances_test = []
    for line in file_training:
        a_line = line.split(" ")
        if first:
            [attribute_names.append(item.strip()) for item in a_line if not item == "Class"]
            first = False
        else:
            atts = [a_line[ii].strip() for ii in range(1,len(a_line))]
            instances_training.append(Instance(a_line[0],atts))
    first = True
    for line in file_test:
        a_line = line.split(" ")
        if first:
            first = False
        else:
            atts = [a_line[ii].strip() for ii in range(1,len(a_line))]
            instances_test.append(Instance(a_line[0],atts))
    return instances_training, instances_test, attribute_names


def find_accuracy():
    total_correct =0
    for inst in inst_test:
        if inst.clas.strip() == root.traverse(inst).strip():
            total_correct += 1
    return float(total_correct) / float(len(inst_test))




# Open file , run with command $ python DecisionTree.py hepatitis-test hepatitis-training
file_test = open("part2/" + sys.argv[1],"r")
file_training = open("part2/" + sys.argv[2],"r")

# Run
print()
print()

reading = read()
inst_training = reading[0]
inst_test = reading[1]
attribs = reading[2]

# Find baseline
num_live = 0
baseline = "ERROR"
base_prob = -1
for i in inst_training:
    if i.get_class().strip() == "live":
        num_live += 1
if num_live > len(inst_training) - num_live:
    baseline = "live"
    base_prob = num_live / len(inst_training)
else:
    baseline = "dead"
    base_prob = (len(inst_training) - num_live)/len(inst_training)

# Make and draw treeT
root = Node().build_tree(inst_training,[i for i in attribs],1)
root.draw_tree("")

# Accuracy
print()
accuracy = find_accuracy()
print("accuracy: ",accuracy)
print("baseline prob: ",base_prob)



