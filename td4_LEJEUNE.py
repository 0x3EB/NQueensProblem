# -*- coding: utf-8 -*-
"""
Created on Thu Mar 12 15:48:18 2020

@author: sebas
"""
import random
chessdim=8 #default chess dimension for the problem 


def changeChessDim(dim):
    ''' Change the dimension of the plate '''
    assert dim in range(25), 'The dimension should between 1 and 25'
    global chessdim
    chessdim = dim

class individual :
    def __init__(self,val=None):
        ''' constructor for individual class'''
        if val==None:
            self.val=random.sample(range(chessdim), chessdim)
        else:
            self.val=val
        self.conflictCmpt=self.fitness()
        
    def __str__(self):
        return " ".join([str(i) for i in self.val])
        
    def conflict(p1,p2):
        return p1[0]==p2[0] or p1[1]==p2[1] or abs(p1[0]-p2[0])==abs(p1[1]-p2[1])
    
    def fitness(self):
        ''' fitness method to get the weight '''
        self.conflictCmpt=0
        for i in range(chessdim):
            for j in range(i+1,chessdim):
                if(individual.conflict([i,self.val[i]],[j,self.val[j]])):
                    self.conflictCmpt+=1
        return self.conflictCmpt

def initializationIndividuals(count):
    return [individual() for i in range(count)]

def evaluate(pop):
    if isinstance(pop, list):
        return sorted(pop,key=lambda i: i.fitness())

def selection(pop, hcount, lcount):
    return pop[:hcount]+pop[len(pop)-lcount:]

def crossover(ind1, ind2):
    midupper = chessdim//2 if chessdim%2==0 else (chessdim//2)+1 #get the middle of the chess dimension if it is a even and odd dimension size
    if isinstance(ind1, individual) and isinstance(ind2, individual):
        ind1.val = ind1.val[:midupper]+ind2.val[chessdim//2:]
        ind2.val = ind2.val[:midupper]+ind1.val[chessdim//2:]
    return [ind1,ind2]
            
def mutation(ind):
    l=ind.val[:]
    l[random.randint(0,chessdim-1)]=random.randint(0,chessdim-1)
    return individual(l) #recreate object in the return

def OneUniqueSolution(): 
    pop = initializationIndividuals(25)
    foundSolution = False
    cmpt=0
    while not (foundSolution):
        print("iteration numéro : ", cmpt)
        cmpt += 1
        evaluatedPop = evaluate(pop)
        if evaluatedPop[0].fitness() == 0:
            foundSolution = True
        else:
            selected = selection(evaluatedPop,10,4)
            crossed = []
            for i in range (0,len(selected),2):
                crossed += crossover(selected[i],selected[i+1])
            mutated = []
            for i in selected:
                mutated.append(mutation(i))
            newalea = initializationIndividuals(5)
            pop = selected[:] + crossed[:] + mutated[:] + newalea[:]
    print(evaluatedPop[0])

def AllSolutions(): 
    allsolutions = [] #tab that contains all solutions
    evaluatedPop = []
    pop = initializationIndividuals(25)
    while True:
        print(len(allsolutions))
        evaluatedPop = evaluate(pop)
        if evaluatedPop[0].fitness() == 0:
            if(evaluatedPop[0].val not in [idv.val for idv in allsolutions]):
                allsolutions.append(evaluatedPop[0])
            else:
                evaluatedPop.pop(0)
            pop = evaluatedPop
        else:
            selected = selection(evaluatedPop,10,4)
            crossed = []
            for i in range (0,len(selected),2):
                crossed += crossover(selected[i],selected[i+1])
            mutated = []
            for i in selected:
                mutated.append(mutation(i))
            newalea = initializationIndividuals(5)
            pop = selected[:] + crossed[:] + mutated[:] + newalea[:]

if __name__ == '__main__':
    dim = input("Give the chess dimension (must be between 1 and 25) | PRESS ENTER FOR 8 queens problem ")
    dim = dim if len(dim)>0 else str(chessdim) #converting global variable to string for applying eval() method
    changeChessDim(eval(dim))
    AllSolutions() #display all solutions (infinite loop)
    
    
    