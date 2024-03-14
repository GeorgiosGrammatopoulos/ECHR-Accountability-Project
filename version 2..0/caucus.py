import judge as js
import random as rd
import pandas as pd

class Caucus:
        
    def __init__(self, casepolicy, casestate, law, fact, caucus = 7):
            
        members = []
        composition = []
        myjudge = None
        forvote = 0
        againstvote = 0
        outcome = None
        
        
        
            
        while True:
            
            current = len(members)
            
            myjudge = js.Judge()
            
            if (len(members) == caucus - 1) and (casestate not in composition) and (myjudge.state != casestate):
                continue
            
            if myjudge.state in composition:
                continue
            else:
                members.append(myjudge)
                composition.append(myjudge.state)
            
            
            result = myjudge.topdown(casepolicy, casestate)
            result = myjudge.bottomup (law, fact, result)
            
            if result <= 0:
                
                againstvote += 1
                
            if result > 0:
                
                forvote += 1
                
            if len(members) == caucus:
                break
            
            
            
            
                
        if forvote > againstvote:
            
            outcome = True
            
        if forvote < againstvote:
            
            outcome = False
            
        
                
                
        self.members = members
        self.caucus = caucus
        self.forvote = forvote
        self.againstvote = againstvote
        self.outcome = outcome
        

    def tally(self, members, caucus, forvote, against, vote):
        
        
        
class Subcaucus(self, ):
    
    def __init__: 
        
        
        
        




#############################  TESTS  ##################################

def onetest (casepolicy, casestate, law, fact):


    mycaucus = Caucus(casepolicy, casestate, law, fact)


    print("Caucus members:")

    for i in mycaucus.members:
        print(i.firstname, i.lastname)
        if mycaucus.members.index(i) == 6:
            print("\n\n\n")
            
    print("Caucus nationalities:")

    for i in mycaucus.members:
        print(i.state)
        if mycaucus.members.index(i) == 6:
            print("\n\n\n")

    print(f'Membership: {mycaucus.caucus}')
    print(f'Votes  for: {mycaucus.forvote}')
    print(f'Votes against: {mycaucus.againstvote}')
    print(f'Outcome: {mycaucus.outcome}')
    
    return mycaucus.outcome


def multitest(casestate = None):
    
    casepolicy = []
    casespecifics = []
    assess= [-1, 0,1]
    casestates = [
            'Austria', 
            'Belgium', 
            'Cyprus', 
            'Czech Republic', 
            'Denmark', 
            'Estonia', 
            'Finland', 
            'France', 
            'Germany', 
            'Greece', 
            'Hungary', 
            'Iceland', 
            'Ireland', 
            'Italy', 
            'Latvia', 
            'Lithuania', 
            'Luxembourg', 
            'Malta', 
            'Netherlands', 
            'Norway', 
            'Poland', 
            'Portugal', 
            'Slovakia', 
            'Slovenia', 
            'Spain', 
            'Sweden', 
            'Switzerland', 
            'United Kingdom', 
            'Albania', 
            'Andorra', 
            'Armenia', 
            'Azerbaijan', 
            'Bosnia and Herzegovina', 
            'Bulgaria', 
            'Croatia', 
            'Georgia', 
            'Liechtenstein', 
            'Moldova', 
            'Monaco', 
            'Montenegro', 
            'North Macedonia', 
            'Romania', 
            'Russia', 
            'San Marino', 
            'Serbia', 
            'Turkey', 
            'Ukraine'
    ]
    
    if casestate == None:
        
        casestate = rd.choice(casestates)
    
    for i in range(0, 10, 1):
            
        number = rd.randint(0,5)
        if number != 0:
            casepolicy.append(number)   #hard-coded stop

            
    for i in range(0, len(casepolicy), 1):
            
        casespecifics.append(rd.randint(-10, 10))   #hard-coded stop
        
    law = rd.choice(assess)
    fact = rd.choice(assess)
        
    
    return onetest (casepolicy, casestate, law, fact)
    
    
def execute():
    
    pos = 0
    neg = 0

        
    for i in range (0, 10000, 1):
        
        intuition = multitest()
        if intuition > 0:
            pos += 1
        elif intuition <= 0:
            neg += 1
            
        print("\n\n\n\n\n")
                
            
    print (f'In 10000 iterations:\npercentage of positives: {pos/100}\npercentage of negatives: {neg/100}')
    
execute()
