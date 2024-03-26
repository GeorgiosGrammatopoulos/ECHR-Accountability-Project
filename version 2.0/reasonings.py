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
    
    slope = 0
    priority = len(judge.policy.keys())
        
    if judge.countryname == respondent:
            
        slope += -15   #imperative weight in favor of the respondent, only surpassed by the law
        priority -=1   #for the moment, there is no specific prioritization in hand
        
    for i, k in judge.policy.items():
                
        if i in casepolicy:
                    
            try:
                    
                slope += k//priority
                priority -= 1
                continue
                        
            except ZeroDivisionError:
                        
                slope += k // priority - 1
                priority -= 1
                continue
                        
                    
    return slope
    
        
 #Then, they account for the law and the assessment of the facts.
 #Assessing the facts is a group process. That will become relevant later on.
                  
def bottomup (judge, law, fact, opinion):
        
    if law >= -5 and law <= 5:
        print('passed')    #weight is designed under the assumption that the law is the most imperative outcome
        pass
    elif law < -5:
        opinion -= 20
    elif law > 5:
        opinion += 20
            
            
    if fact >= -5 and fact <= 5:
        print('passed')    #weight is designed under the assumption that the law is the most imperative outcome
        pass
    elif fact < -5:
        opinion -= 10
    elif fact > 5:
        opinion += 10
        
    print (f'after the process, the opinion is {opinion}')
            
    return opinion


#appending functinon, returns strings, contrary to the tally function

def winLoss (caucus, respondent, casepolicy, law, fact):#whereas members :the participant judges
    
    result = caucus.votingProcess (respondent, casepolicy, law, fact)
    tallyfavor = result[0]
    tallyagainst = result[1]
    opinions = result[3]
    result = result[2]
    
    if result:
            
        return [tallyfavor, tallyagainst, 'win', opinions]
            
    else:
            
        return [tallyfavor, tallyagainst, 'loss', opinions]
    
    
#general calculation function to estimate the amount
#this function is to be invoked only in the event of a win
#depending on the overall architecture, I may have to introduce it as well

def amountCalc(instance, ask, counter): #ask and counter: dictionaries
    
    for i in instance.caucus:
        
        print(i.opinion)
       
    groups = caucus.Subcaucus.formulating(instance)
    print(f'The losing pressure: {groups[0].evaluation}')
    print(f'The winning pressure: {groups[1].evaluation}')
    totalDist = (abs(groups[0].evaluation) + abs(groups[1].evaluation))
    print(f'Total distribution is: {totalDist}')

    #In theory, material losses and expenses are attributed so long as proven
    #unless questionable according to the respondent
    
    
    amountDict = {}
        
    amountDict['material'] = ask['material'] - counter['material']
    amountDict['ce'] = ask['ce'] - counter['ce']
    amountDict['non_material'] =  ask['non_material'] - counter['non_material']
    print(f'Non-adjusted ask is { amountDict["non_material"]}')
    amountDict['non_material'] = amountDict['non_material'] / totalDist * (groups[0].evaluation + groups[1].evaluation)
        
    for key, value in amountDict.items():
        
        if value <= 0:
            
            value = 0
            
    return amountDict
