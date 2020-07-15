from deap import algorithms
from deap import base
from deap import creator
from deap import tools
from deap import gp
import operator
import numpy
import random
import math

# Following guide : https://deap.readthedocs.io/en/master/examples/gp_symbreg.html

def read():
    data_in = open("regression", "r")
    x = []
    y = []
    next(data_in)
    for line in data_in:
        # add line
        line_data = line.split(" ")
        line_data = [float(line_data[ii].strip()) for ii in range(0,len(line_data))]
        x.append(line_data[0])
        y.append(line_data[1])
    return x,y


data = read()


# Define new functions
def protected_div(left, right):
    try:
        return left / right
    except ZeroDivisionError:
        return 1

# Returns MSE : 1/n * sum(current-real)**2
def eval_symb_reg(individual):
    func = toolbox.compile(expr=individual)
    sqe = 0
    for g in range(0,len(data[0])):
        sqe += ((func(data[0][g]) - data[1][g])**2) # MAYBE FUNC AND Y OTHER WAY ROUND ACCORDING TO WIKI?
    return sqe / len(data),



# PRIMITIVES
pset = gp.PrimitiveSet("MAIN", 1)
pset.addPrimitive(operator.add, 2)
pset.addPrimitive(operator.sub, 2)
pset.addPrimitive(operator.mul, 2)
pset.addPrimitive(protected_div, 2)
pset.addPrimitive(operator.neg, 1)
pset.addEphemeralConstant("rand101", lambda: random.randint(-5,5))
pset.renameArguments(ARG0='x')

# CREATOR
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMin)

# TOOLBOX
toolbox = base.Toolbox()
toolbox.register("expr", gp.genHalfAndHalf, pset=pset, min_= 0, max_=3)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("compile", gp.compile, pset=pset)
toolbox.register("evaluate", eval_symb_reg)
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("mate", gp.cxOnePoint)
toolbox.register("expr_mut", gp.genFull, min_=0, max_=3)
toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr_mut, pset=pset)
toolbox.decorate("mate", gp.staticLimit(key=operator.attrgetter("height"), max_value=17))
toolbox.decorate("mutate", gp.staticLimit(key=operator.attrgetter("height"), max_value=17))

# STATS
#random.seed(318)
pop = toolbox.population(n=100)
hof = tools.HallOfFame(1)
stats_fit = tools.Statistics(lambda ind: ind.fitness.values)
stats_size = tools.Statistics(len)
mstats = tools.MultiStatistics(fitness=stats_fit, size=stats_size)
mstats.register("avg", numpy.mean)
mstats.register("std", numpy.std)
mstats.register("min", numpy.min)
mstats.register("max", numpy.max)

# Run

cxpb = 0.9 # crossover rate
mutpb = 0.1 # mutation probability
ngen = 40 # number of generations
pop, log = algorithms.eaSimple(pop, toolbox, cxpb, mutpb, ngen, stats=mstats,
                               halloffame=hof,verbose=True)

# Print best 3 - change to if 1 to print
if 0:
    print("Print best 3")
    best_ind = tools.selBest(pop, 3)
    for i in range(0,len(best_ind)):
        print()
        print(best_ind[i])
        print("MSE=", eval_symb_reg(best_ind[i]))
        print()


# Print MSE of output + formula
if 1:
    print("Print MSE of output")
    print("Equation = ",hof[0])
    print("MSE =",eval_symb_reg(hof[0]))
    print()


# Comparing function to actual data for 5.7
if 0:
    print("Comparing function to actual data for 5.7")
    for z in range(0,len(data[0])):
        x = data[0][z]
        yi = (x**2 + 4*x + 4)
        print("x=",x,"   yi=",yi,"   y=",data[1][z])
        print()