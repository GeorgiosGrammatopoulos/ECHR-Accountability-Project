import pandas as pd
import random as rd
import string
#import utility
#import judge
#import caucus


class Judge:
    
    def __init__ (self, jud, vote, disp):
        
        self.jud = jud
        self.vote = vote
        self.disp = disp
        
        
class Caucus:
    
    def __init__ (self, *judge):
        
        caucus = []
        for i in judge:
            caucus.append(i)
            
        self.caucus = caucus
            

class Subcaucus:
    
    def __init__ (self, caucus, vot):
        
        sub = []
        disps = 0
        
        for i in caucus:
            
            if i.vote == vot:
                
                sub.append(i)
                disps += i.disp
        
        self.caucus = caucus
        self.sub = sub
        self.disps = disps
          
    def compcalc(self, rang0, rang1):
        
        rangtot = rang1 - rang0
        
        rangrd = rangtot / len(self.caucus)
        
        rangtot = 0
        
        for i in self.sub:
            rangtot += (rangrd/10) * i.disp
        
        return rangtot
        
        #motivation should take a part
        
        
        
judge1 = Judge(1, 1, 10)
judge2 = Judge(2, 1, 7)
judge3 = Judge(3, 1, 1)
judge4 = Judge(4, 1, 4)
judge5 = Judge(5, 1, 2)
judge6 = Judge(6, 1, -1)
judge7 = Judge(7, 0, -3)

mycaucus = Caucus(judge1, judge2, judge3, judge4, judge5, judge6, judge7)

subcaucus1 = Subcaucus(mycaucus.caucus, 1)
subcaucus2 = Subcaucus(mycaucus.caucus, 0)

print(subcaucus1.compcalc(0, 10000))
print(subcaucus2.compcalc(0, 10000))