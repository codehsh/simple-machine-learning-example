import numpy as np
from itertools import permutations

citys=np.array([[3,1,7,6,2,8],[2,5,3,2,6,5],[1,3,1,2,2,5],[4,7,7,8,3,2],[2,0,3,2,4,5],[3,6,7,3,4,5]])

def swap(i,temp_a,temp_b):
    if i not in temp_b:
        return i
    else:
        idx=temp_b.index(i)
        if temp_a[idx] in temp_b:
            return swap(temp_a[idx],temp_a,temp_b)
        else:
            return temp_a[idx]

def pmx(list_a, list_b, start_index, end_index):     
    result_a=[]
    result_b=[]
    temp_a=list_a[start_index:end_index+1]
    temp_b=list_b[start_index:end_index+1]

    for i in range(len(list_a)):
        if i in range(start_index,end_index+1):
            result_a.append(list_b[i])
            result_b.append(list_a[i])            
        else:
            result_a.append(swap(list_a[i],temp_a,temp_b))
            result_b.append(swap(list_b[i],temp_b,temp_a))

    return result_a,result_b

class GeneticAlgorithm:
    
    def __init__(self, target_city):
        self.num_pop=20
        self.target_city=target_city
        self.population=[self.genChromosome() for i in range(self.num_pop)]
        self.best = None
    
    def genChromosome(self):
        to_permute=list(range(len(citys)))
        to_permute.remove(self.target_city)
        return list(np.random.permutation(to_permute))
    
    def evalChromosome(self,chromosome):
        result = 0
        for i in range(len(chromosome)):
            if i==0: 
                result += citys[0][chromosome[i]]
            elif i==(len(chromosome)-1):
                result += citys[chromosome[i]][0]
            else:
                result += citys[chromosome[i-1]][chromosome[i]]
        return result
    
    def evalGeneration(self):
        result = []
        
        for generation in self.population:
            result.append([self.evalChromosome(generation),generation])
        
        result.sort()
        return result
    
    def genNextGeneration(self,evalgen):
        
        a = 5
        b = 5
        mutation_num = 5
        result = []
        
        start_index=1
        end_index=3
        
        # carry over
        for i in range(a):
            result.append(evalgen[i][1])
            
        # cross over
        for i in range(a,a+b):
            cross = pmx(evalgen[i][1], evalgen[i+1][1], start_index, end_index)
            result.append(cross[0])
            result.append(cross[1])
            
        # mutation 
        for i in range(mutation_num):
            result.append(self.genChromosome())
            
        self.population = result
    
    def do_algorithm(self):
        bestvalue = None
        GenCount = 0
        
        while True:
            
            GenCount += 1

            # if bestvalue no longer changes until gencount becomes 6, this loop terminates 
            if GenCount > 5:
                break
                
            evalGen = self.evalGeneration()
            
            if bestvalue == None or bestvalue > evalGen[0][0]:
                bestvalue = evalGen[0][0]
                self.best = evalGen[0]
                GenCount = 0
                
            self.genNextGeneration(evalGen)
           
        return    

gen=GeneticAlgorithm(0)

gen.do_algorithm()

print(gen.best)
