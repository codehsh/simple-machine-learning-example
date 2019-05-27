import csv
import math 
import numpy as np
from itertools import permutations

def getcsvdata(filename):
    f = open(filename, 'r', encoding='utf-8')
    rdr = csv.reader(f)
    dic = dict()

    for line in rdr:
        dic[line[1]] = [line[2],line[3]]
    
    f.close() 
    return dic
    
def haversine(lat1, lon1, lat2, lon2): 
      
    # distance between latitudes 
    # and longitudes 
    dLat = (lat2 - lat1) * math.pi / 180.0
    dLon = (lon2 - lon1) * math.pi / 180.0
  
    # convert to radians 
    lat1 = (lat1) * math.pi / 180.0
    lat2 = (lat2) * math.pi / 180.0
  
    # apply formulae 
    a = (pow(math.sin(dLat / 2), 2) + 
         pow(math.sin(dLon / 2), 2) * 
             math.cos(lat1) * math.cos(lat2)); 

    rad = 6371
    c = 2 * math.asin(math.sqrt(a)) 
    return rad * c 

def maketable(filename):
    
    data = getcsvdata(filename)
    column_list = list(data.keys())[1:]
    result = dict()
    
    for city1_key in column_list:
                    
        city1_data = data[city1_key] 
        dict_data = dict()
        
        for city2_key in column_list:
            
            city2_data = data[city2_key]
            dict_data[city2_key] = haversine(
                float(city1_data[0]),
                float(city1_data[1]),
                float(city2_data[0]),
                float(city2_data[1]))
            
        result[city1_key] = dict_data
            
    return result

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
    
    def __init__(
        self, target_city,
        population_num,
        crossover_num,
        mutation_num,
        carryover_num
        ):

        self.target_city=target_city
        self.population_length = population_num
        self.crossover_length = crossover_num
        self.mutation_length = mutation_num
        self.carryover_length = carryover_num

        self.matrix = maketable('filename')

        self.population=[self.genChromosome() for i in range(self.population_length)]

        self.best = None

    def genChromosome(self):
        to_permute=list(self.matrix.keys())
        to_permute.remove(self.target_city)
        return list(np.random.permutation(to_permute))
    
    def evalChromosome(self,chromosome):
        result = 0
        for i in range(len(chromosome)):
            if i==0: 
                result += self.matrix[self.target_city][chromosome[i]]
            elif i==(len(chromosome)-1):
                result += self.matrix[chromosome[i]][self.target_city]
            else:
                result += self.matrix[chromosome[i-1]][chromosome[i]]
        return result
    
    def evalGeneration(self):
        result = []
        
        for generation in self.population:
            result.append([self.evalChromosome(generation),generation])
        
        result.sort()
        return result
    
    def genNextGeneration(self,evalgen):
        
        result = []
        
        start_index=int(len(self.population[0]))-int(self.crossover_length/2)
        end_index=start_index + self.crossover_length
        
        # Carry Over
        for i in range(self.carryover_length):
            result.append(evalgen[i][1])
            
        # Cross Over
        for i in range(self.carryover_length,self.carryover_length+int(self.crossover_length/2)):
            cross = pmx(evalgen[i][1], evalgen[i+1][1], start_index, end_index)
            result.append(cross[0])
            result.append(cross[1])
            
        # Mutation 
        for i in range(self.mutation_length):
            result.append(self.genChromosome())
            
        self.population = result
    
    def do_algorithm(self):
        bestvalue = None
        GenCount = 0
        
        while True:
            
            GenCount += 1
            
            if GenCount > 10:
                break
                
            evalGen = self.evalGeneration()
            
            if bestvalue == None or bestvalue > evalGen[0][0]:
                bestvalue = evalGen[0][0]
                self.best = evalGen[0]
                GenCount = 0
                
            self.genNextGeneration(evalGen)
           
        return   

bestvalue = None
iternum = None

for i in range(iternum):
    population = np.random.randint(10,1000,size=1)[0]
    carryover = np.random.randint(0,population,size=1)[0]
    crossover = np.random.randint(0,population-carryover,size=1)[0]
    mutation = np.random.randint(0,population-crossover-carryover,size=1)[0]

    genetic = GeneticAlgorithm(
        'Paris',
        population,
        crossover,
        mutation,
        carryover
    )

    genetic.do_algorithm()

    if bestvalue == None or bestvalue[0] > genetic.best[0]:
        bestvalue = genetic.best
