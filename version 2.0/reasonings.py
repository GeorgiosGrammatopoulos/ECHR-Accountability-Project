#This is a white-box simulation of how judges decide. It will help build black-box regression models, and provide insight into their results
import random
import numpy as np
import pandas as pd
import utility as ut
import odbc
import judge
import caucus

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


#appending functinon, returns strings, contrary to the tally function

def winLoss (caucus, respondent, casepolicy, law, fact):#whereas members :the participant judges
    
    result = caucus.votingProcess (self, respondent, casepolicy, law, fact)
    
    if result:
            
        return 'win'
            
    else:
            
        return 'loss'
    
    
#general calculation function to estimate the amount
#this function is to be invoked only in the event of a win
#depending on the overall architecture, I may have to introduce it as well

    def amountCalc(instance, ask, counter): #ask and counter: dictionaries
        
        groups = Subcaucus.formulating(instance)
        totalDist = groups[0].evaluation + groups[1].evaluation
        amountDist = ask / totalDist
        amountDict = {
            material: None,
            non_material: None,
            ce: None
        }
        
        #In theory, material losses and expenses are attributed so long as proven
        #unless questionable according to the respondent
        
        amountDict[material] = ask[material] - counter[material]
        amountDict[ce] = ask[ce] - counter[ce]
        
        amountDict[non_material] =  (groups[1].evaluation - groups[0].evaluation) * amountDist
        
        if amountDist <= 0:
            
            amountDist = 0
        
        return amountDict
