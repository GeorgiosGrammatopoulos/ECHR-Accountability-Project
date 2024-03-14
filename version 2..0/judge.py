###Necessary package imports
import random as rd
import utility as ut
import numpy as np


###Ckass representing the operations of an ordinary judge
class Judge:

###Judges have pre-existent policy preferences according to which they
###decide
###In the instantiation of judges, we need to assume that they already
###have their policy preferences
###For this version, we presume all judges are proficient and protected

    def __init__ (self):
        
        policy = []
        specifics = []
        states = [
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
        
        for i in range(0, 10, 1):
            
            number = rd.randint(0,5)
            if number != 0:
                policy.append(number)   #hard-coded stop

            
        for i in range(0, len(policy), 1):
            
            specifics.append(rd.randint(-7, 7))   #hard-coded stop
            
        state = rd.choice(states)
        
        self.firstname = ut.random_name(8)
        self.lastname = ut.random_name(8)
        self.policy = policy
        self.specifics = specifics
        self.state = state
            

###When judges decide, they first make an assessment
    
    def topdown (self, casepolicy, casestate):
        
        outcomes = [10, 0] #being a national judge is a positive measure
        weights = [0.8, 0.2] #hard-coded weight according to Voeten
    
        denom = 0
        priority = 1
        
        if self.state == casestate:
            
            denom += -15
            priority -=1
        
        for i in self.policy:
            
            for k in range (0, len(casepolicy), 1):
                
                if i == casepolicy[k]:
                    
                    try:
                    
                        denom += self.specifics[self.policy.index(i)]//(k + priority)
                        break
                        
                    except ZeroDivisionError:
                        
                        denom += self.specifics[self.policy.index(i)]// (k + (priority-1))
                        break
                        
                    
        return denom 
        
        
    def bottomup (self, law, fact, intuition):
        
        if law == 0:
            pass
        elif law == 1:
            intuition +=17
        elif law == -1:
            intuition -=17
            
            
        if fact == 0:
            pass
        elif fact == 1:
            intuition +=10
        elif fact == -1:
            intuition -=10
            
            
        return intuition
            
        
        
        
        





#############################  TESTS  ##################################
        
        
def onetest(myjudge, casepolicy, casestate, law, fact):     ###testing function

    intuition = myjudge.topdown(casepolicy, casestate)
    
    intuition = myjudge.bottomup(law, fact, intuition)

    #print (myjudge.firstname, myjudge.lastname)
    #print (f'Home state: {myjudge.state}')
    #print ("Inclinations:")

    #for i in range (0, len(myjudge.policy), 1):
        #print (f'{myjudge.policy[i]}: {myjudge.specifics[i]}', end = ", ")
        
    #print(f'\n\n\nCase policy considerations: {casepolicy}')
    #print(f'Respondent state: {casestate}')
    #print(f'\n\n\nAssessment: {intuition}')
    
    return intuition
    
    
def multitest(myjudge, casestate = None):
    
    assess = [-1, 0, 1]
    casepolicy = []
    casespecifics = []
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
        
    
    return onetest (myjudge, casepolicy, casestate, law, fact)
    
    
def execute():
    
    pos = 0
    neg = 0
    posstat = 0
    negstat = 0



        
    for i in range (0, 10000, 1):
        
        myjudge = Judge()
        intuition = multitest(myjudge)
        if intuition > 0:
            pos += 1
        elif intuition <= 0:
            neg += 1
                
            
    print (f'In 10000 iterations:\npercentage of positives: {pos/100}\npercentage of negatives: {neg/100}')
