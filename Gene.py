'''
Created on 01/07/2015

@author: Mollinetti
'''
import random, Parameters,Profile

class Gene():
    
    population = 0
        
    def __init__(self, param = Parameters):
        self.genotype = []
        self.fitness = float("inf")
        self.violations = float("inf")
        self.socialFitness = float(0)
        self.totalFitness = float(0)
        self.restrictions = []
        
        
        #generating optimization parameters
        for i in range(0,param.dim):
            self.genotype.append(random.uniform(param.lowBound[i], param.uppBound[i]))
        
        #generating strategy profile
        self.profile = Profile.Profile(param)

        Gene.population +=1
                
    def traverse(self):
        print(self.genotype)
    
    @classmethod
    def howmany(cls):
        print ("currently {:d} genes".format(cls.population))
        
        
