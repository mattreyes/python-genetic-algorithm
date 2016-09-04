import math
import random
from ChromosoneClass import Chromosone

# Create a randomly generated chromosone with 4*k bits
def randChromosone(genesNum,target):
	accStr = ""
	i = 0
	while i < genesNum*4:
		accStr += str(random.randint(0,1))
		i += 1
	return Chromosone(accStr,target)

# Consumes desired population size and desired size of each chromosone,
# returns list of chromosones popSize
def initPopulation(size,genesNum,target):
	i = 0
	population = []
	while(i<size):
		population.append(randChromosone(genesNum,target))
		i += 1
	return population

# Takes two chromosomes with equal length and adds the parents to the population 
# Genes may be crossed at some random point
def crossChromosones(c1,c2,crossRate, mutRate,target, popn):
	assert len(c1.encoding) > 0, "ERROR: Chromosones must have at least one gene."
	if random.uniform(0,1) <= crossRate: # breeding
		crossPoint = random.randint(0,len(c1.encoding)-1)
		cross1 = c1.encoding[:crossPoint] + c2.encoding[crossPoint:]
		cross2 = c2.encoding[:crossPoint] + c1.encoding[crossPoint:]
		c1 = Chromosone(cross1,target)
		c2 = Chromosone(cross2,target)
		# put crossed Chromosones into back to the pool, with possible mutation
		popn.append(mutateChromosone(c1,target,mutRate))
		popn.append(mutateChromosone(c2,target,mutRate))
		return True
	else: # no breeding
		popn.append(c1)
		popn.append(c2)
		return False

# Flips bits of c based on mutRate and returns a newly mutated chromosone. 
def mutateChromosone(c, target, mutRate):
	accStr = ""
	for char in c.encoding:
		r = random.uniform(0,1)	
		if r <= mutationRate:
			if char == "0":
				accStr += "1"
			elif char == "1":
				accStr += "0"
		else:
			accStr += char
	return Chromosone(accStr,target)

# Calculates the total fitness score of a population. returns a positive float
# or if it is a tolerable solution in population, returns a chormosone object.
def totalFitness(population,target):
	total = 0
	for c in population:
		# -1 indicates a flag to terminate. 
		if c.fitnessScore == -1:
			return c
		else:
			total += c.fitnessScore
	return total

# Roulette-wheel selection via stochastic acceptance; O(1) time.
# Source: http://arxiv.org/pdf/1109.3627v2.pdf
def rouletteSelection(population, totalScore):
	while len(population) != 0:
		randC = random.choice(population)
		prob = randC.fitnessScore/totalScore
		if random.uniform(0,1) <= prob:
			return randC

###############################################################
# Algorithm
###############################################################

# Parameters (can be tuned)
populationSize = 20
numGenes = 15
maxIterations = 2000
crossoverRate = 0.7
mutationRate = 0.001

print("Enter your target number:")
target = float(input())

from operator import attrgetter

def geneticAlgorithm(populationSize,numGenes,target,maxIterations,crossoverRate,mutationRate):
	assert (populationSize > 2), "You need to have a population greater than 2."
	print("Searching...")
	currPop = initPopulation(populationSize, numGenes,target) # Initialize population
	numIterations = 0
	while (numIterations < maxIterations):
		currPopScore = totalFitness(currPop,target)
		if not (isinstance(currPopScore,int) or isinstance(currPopScore,float)):
			print("Solution found! " + currPopScore.getEncoding() + " with target " 
				+ str(target) + " Took " + str(numIterations) + " iterations.")
			return # if we get a Chromosone object (exact solution) then return 
		newPop = []
		while (len(newPop) < populationSize): # loop to breed next generation
			parent1 = rouletteSelection(currPop,currPopScore)
			parent2 = rouletteSelection(currPop,currPopScore)
			if parent1 != parent2:
				crossChromosones(parent1,parent2,crossoverRate, mutationRate,target,newPop)
		numIterations += 1
		if numIterations % 500 == 0:
			print("Generation " + str(numIterations))
		currPop = newPop

	closeSoln = max(currPop, key=attrgetter('fitnessScore'))
	print("Max generation reached. Closest solution is " + closeSoln.getEncoding() + "=" 
		+ str(closeSoln.result) + " with target " + str(target))


geneticAlgorithm(populationSize,numGenes,target,maxIterations,crossoverRate,mutationRate)