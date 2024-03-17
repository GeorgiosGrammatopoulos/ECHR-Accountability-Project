#This is a white-box simulation of how judges decide. It will help build black-box regression models, and provide insight into their results
import random
import numpy as np
import pandas as pd
import utility as ut
import odbc
import judge
import caucus
import applicant

#Function to store win/loss information in dataframes. The duality of outcomes can also be used to validate other data
###When judges decide, they first make an assessment
    
def topdown (judge, casepolicy, respondent):

    denom = 0
    priority = len(judge.policy.keys())
        
    if judge.countryname == respondent:
            
        denom += -15   #imperative weight in favor of the respondent, only surpassed by the law
        priority -=1   #for the moment, there is no specific prioritization in hand
        
    for i, k in self.policy.items():
                
        if i in casepolicy:
                    
            try:
                    
                denom += k//priority
                priority -= 1
                continue
                        
            except ZeroDivisionError:
                        
                denom += k // priority - 1
                priority -= 1
                continue
                        
                    
    return denom
    
        
 #Then, they account for the law and the assessment of the facts.
 #Assessing the facts is a group process. That will become relevant later on.
                  
def bottomup (judge, law, fact, ruling):
        
    if law == 0:    #weight is designed under the assumption that the law is the most imperative outcome
        pass
    elif law == 1:
        ruling +=17
    elif law == -1:
        ruling -=17
            
            
    if fact == 0:   #weight places 
        pass
    elif fact == 1:
        ruling +=10
    elif fact == -1:
        ruling -=10
            
            
    return ruling


#Reasoning for 

def winLoss (favor, against, *member #:the participant judges):
    
    members = []  #turning the tuple into a list
    for i in member:
        members.append(i)
    
    composition = []
    favor = 0
    against = 0
        
    for i in members:
            
        if (len(members) == caucus - 1) and (countryname not in composition) and (myjudge.countryname != countryname):
            continue
            
        if myjudge.countryname in composition:
            continue
        else:
            members.append(myjudge)
            composition.append(myjudge.countryname           
            
        result = topdown(i, casepolicy, countryname)
        result = bottomup (i, law, fact, result)
            
        if result <= 0:
                
            against += 1
                
        if result > 0:
                
            favor += 1
                
        if len(members) == caucus:
            importData('Reasonings', 'favor', favor)
            importData('Reasonings', 'against', against)
            break      
                
    if favor > against:
            
        outcome = True
            
    if favor < against:
            
        outcome = False
    
    caucus = favor + against
    
    if caucus - favor < caucus - against:
        
        return 'loss'
    
    if caucus - favor > caucus - against:
        
        return 'win'
    
    
