import random
import operator
import csv
import itertools
import numpy
from deap import algorithms
from deap import base
from deap import creator
from deap import tools
from deap import gp

# Following guide : https://deap.readthedocs.io/en/master/examples/gp_spambase.html

def read(filename):
    data_in = open(filename, "r")
    x = []
    next(data_in)
    for line in data_in:
        y = []
        # add line
        line_data_f = line.split(" ")
        del line_data_f[len(line_data_f)-1]
        line_data = [float(line_data_f[ii].strip()) for ii in range(0,len(line_data_f)-1)]
        line_data.append(line_data_f[len(line_data_f)-1].strip())
        x.append(line_data)
    return x

# Sum correct instances
def evalSatellite(individual):
    func = toolbox.compile(expr=individual)
    correct = 0
    for i in range(0,len(data)):
        target = data[i][len(data[i])-1]
        target_bool = True
        if target == "'Anomaly'":
            target_bool = False
        predict = func(*data[i][:len(data[i])-1])
        if target_bool == predict:
            correct+=1
    return correct,

# Define a protected division function
def protectedDiv(left, right):
    try:
        return left / right
    except ZeroDivisionError:
        return 1

# Define a new if-then-else function
def if_then_else(input, output1, output2):
    if input:
        return output1
    else:
        return output2



# Define a new primitive set for strongly typed GP
pset = gp.PrimitiveSetTyped("MAIN", itertools.repeat(float, 36),bool,"IN")

# Boolean Operators
pset.addPrimitive(operator.and_, [bool, bool], bool)
pset.addPrimitive(operator.or_, [bool, bool], bool)
pset.addPrimitive(operator.not_, [bool], bool)

# Floating Point Operators
pset.addPrimitive(operator.add, [float, float], float)
pset.addPrimitive(operator.sub, [float, float], float)
pset.addPrimitive(operator.mul, [float, float], float)
pset.addPrimitive(protectedDiv, [float, float], float)

# Logic Operators
pset.addPrimitive(operator.lt, [float, float], bool) # Less than
pset.addPrimitive(operator.eq, [float, float], bool) # ==
pset.addPrimitive(if_then_else, [bool, float, float], float)

# Terminals
pset.addEphemeralConstant("rand100", lambda: random.random() * 100, float)
pset.addTerminal(True, bool)
pset.addTerminal(False, bool)

# Creator
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMax)

toolbox = base.Toolbox()
toolbox.register("expr", gp.genHalfAndHalf, pset=pset, min_=1, max_=2)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("compile", gp.compile, pset=pset)



toolbox.register("evaluate", evalSatellite)
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("mate", gp.cxOnePoint)
toolbox.register("expr_mut", gp.genFull, min_=0, max_=2)
toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr_mut, pset=pset)
toolbox.decorate("mate", gp.staticLimit(key=operator.attrgetter("height"), max_value=17))
toolbox.decorate("mutate", gp.staticLimit(key=operator.attrgetter("height"), max_value=17))

#random.seed(10)



training = read("training.txt")
test = read("test.txt")


data = training

pop = toolbox.population(n=100)
hof = tools.HallOfFame(1)
stats = tools.Statistics(lambda ind: ind.fitness.values)
stats.register("avg", numpy.mean)
stats.register("std", numpy.std)
stats.register("min", numpy.min)
stats.register("max", numpy.max)


cxpb = 0.9 # crossover rate
mutpb = 0.1 # mutation probability
ngen = 51 # number of generations
pop, log = algorithms.eaSimple(pop, toolbox, cxpb, mutpb, ngen, stats=stats,
                               halloffame=hof,verbose=True)
# Training accuracy
accuracyTraining = evalSatellite(hof[0])[0]/len(training)

# Now test on test
data = test
accuracyTest = evalSatellite(hof[0])[0]/len(test)
print()
print(hof[0])
print("Training Fitness = ",accuracyTraining)
print("Test accuracy = ",accuracyTest)


