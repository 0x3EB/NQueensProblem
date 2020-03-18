# -*- coding: utf-8 -*-
"""
Created on Thu Mar 12 15:48:18 2020

@author: sebastien lejeune Apprenti-A3 (IBO)
"""
import random
chessdim=8 #default chess dimension


def changeChessDim(dim):
    ''' Change the dimension of the plate 
    
    Args:
        dim: the dimension of the plate
    '''
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
    ''' Generate Individuals
    
    Args:
        count: number of individuals
    Returns:
        A list of individuals
    '''
    return [individual() for i in range(count)]

def evaluate(pop):
    ''' Sort all individuals in fonction of their fitness value
    Args:
        pop: list of individuals
    Returns:
        A sorted list of individuals
    '''
    if isinstance(pop, list):
        return sorted(pop,key=lambda i: i.fitness())

def selection(pop, hcount, lcount):
    ''' select a part of the population list
    Args:
        pop: list of individuals
        hcount: number of bests individuals
        lcount: number of worsts individuals
    Returns:
        A sorted list of selected individuals
    '''
    return pop[:hcount]+pop[len(pop)-lcount:]

def crossover(ind1, ind2):
    ''' Combine the genetic information of two parents to generate new offspring
    Args:
        ind1: individual
        ind2: individual
    Returns:
        A list of 2 crossover individuals
    '''
    midupper = chessdim//2 if chessdim%2==0 else (chessdim//2)+1 #get the middle of the chess dimension if it is a even and odd dimension size
    if isinstance(ind1, individual) and isinstance(ind2, individual):
        ind1.val = ind1.val[:chessdim//2]+ind2.val[len(ind2.val)-midupper:]
        ind2.val = ind2.val[:chessdim//2]+ind1.val[len(ind1.val)-midupper:]
    return [ind1,ind2]
            
def mutation(ind):
    ''' Select one random value of the individual and generate an other one
    Args:
        ind: individual
    Returns:
        mutated individual 
    '''
    l=ind.val[:]
    l[random.randint(0,chessdim-1)]=random.randint(0,chessdim-1)
    return individual(l) #recreate object in the return

def OneUniqueSolution(): 
    ''' Display one unique solution of the N Queens problem
    '''
    pop = initializationIndividuals(25)
    foundSolution = False
    cmpt=0
    while not (foundSolution):
        print("iteration : ", cmpt)
        cmpt += 1
        evaluatedPop = evaluate(pop) #sort the list
        if evaluatedPop[0].fitness() == 0:
            foundSolution = True
        else:
            selected = selection(evaluatedPop,10,4) #select the 10 bests and 4 worsts
            crossed = [] #list for the crossover
            for i in range (0,len(selected),2):
                crossed += crossover(selected[i],selected[i+1])
            mutated = [] #list for the mutation 
            for i in selected:
                mutated.append(mutation(i))
            newalea = initializationIndividuals(5)
            pop = selected[:] + crossed[:] + mutated[:] + newalea[:] #recreate the population list with 5 new individuals and all individuals crossed and mutated
    print('One unique solution : [{}]'.format(evaluatedPop[0]))

def AllSolutions(): 
    ''' Display the solutions number of the N Queens problem in the infinite loop
    '''
    allsolutions = [] #tab that contains all solutions
    evaluatedPop = []
    pop = initializationIndividuals(25)
    cmpt = 0
    while True:
        print('iteration : {0} | number of solutions : {1}'.format(cmpt, len(allsolutions))) #number of found solutions
        cmpt += 1
        evaluatedPop = evaluate(pop) #sort the list
        if len(evaluatedPop)>0:
            if evaluatedPop[0].fitness() == 0:
                if(evaluatedPop[0].val not in [idv.val for idv in allsolutions]): #if the solution is not in the list of that avoid duplicate solutions
                    allsolutions.append(evaluatedPop[0]) #add the solution to the AllSolution list
                else:
                    evaluatedPop.pop(0) #remove the solution from the population list
                pop = evaluatedPop[:]
            else:
                selected = selection(evaluatedPop,10,4) #select the 10 bests and 4 worsts
                crossed = [] #list for the crossover
                for i in range (0,len(selected),2):
                    crossed += crossover(selected[i],selected[i+1])
                mutated = [] #list for the mutation        
                for i in selected:
                    mutated.append(mutation(i))
                newalea = initializationIndividuals(5)
                pop = selected[:] + crossed[:] + mutated[:] + newalea[:] #recreate the population list with 5 new individuals and all individuals crossed and mutated
        else:
            break #exit the loop if the list is empty
    print('End of the loop !')
    print('Found {} solution(s)'.format(len(allsolutions)))

if __name__ == '__main__':
    dim = input("Give the chess dimension (must be between 1 and 25) | PRESS ENTER FOR 8 queens problem ")
    dim = dim if len(dim)>0 else str(chessdim) #converting global variable to string to apply 'eval' method
    changeChessDim(eval(dim)) #change the size of the plate
    #OneUniqueSolution()
    AllSolutions() #display all solutions (infinite loop)
    
    
    