###Necessary package imports
import random as rd
import numpy as np
import pandas as pd
import odbc
import utility as ut


###Ckass representing the operations of an ordinary judge
class Judge:

###Judges have pre-existent policy preferences according to which they
###decide
###In the instantiation of judges, we need to assume that they already
###have their policy preferences
###For this version, we presume all judges are proficient and protected

    def __init__ (self, startterm = None, endterm = None, countrynames = None, firstnames = None, lastnames = None, role = None):
        
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
            
        if countrynames == None:
            countrynames = rd.choice(states)
        self.countryname = countrynames
        if firstnames == None:
            firstnames = ut.random_name(8)
        self.firstname = firstnames
        if lastnames == None:
            lastnames = ut.random_name(8)
        self.lastname = lastnames
        if role == None:
            role = 'Judge'
        self.role = role
        self.policy = policy
        self.specifics = specifics
        self.startterm = ut.dateInput('Please enter the judge\s start date: ', startterm)
        self.endterm = ut.dateInput('Please enter the judge\s end date: ', endterm)
        
        
    def judgeAppointment (self):
        
        fulls = odbc.exportData('Judges')
        
        if not ((fulls['lastname'] == self.lastname) & (fulls['firstname'] == self.firstname)).any():
            
            nfirstname = str(self.firstname)
            nlastname = str(self.lastname)
            nrole = str(self.role)
            nstartterm = str(self.startterm)
            nendterm = str(self.endterm)
            ncountryname = str(self.countryname)
                    
            odbc.importData('Judges', firstname = f'{nfirstname}', lastname = f'{nlastname}', role = f'{nrole}', startterm = f'{nstartterm}', endterm = f'{nendterm}', countryname = f'{ncountryname}')
        
        else:
            
            fulls.query(f"lastname == '{self.lastname}' and firstname == '{self.firstname}'")
        
        
        
        
            

###When judges decide, they first make an assessment
    
    def topdown (self, casepolicy, casestate):
        
        outcomes = [10, 0] #being a national judge is a positive measure
        weights = [0.8, 0.2] #hard-coded weight according to Voeten
    
        denom = 0
        priority = 1
        
        if self.countryname == casestate:
            
            denom += -15
            priority -=1
        
        for i in self.policy:
            
            for k in range (0, casepolicy, 1):
                
                if i == casepolicy:
                    
                    try:
                    
                        denom += self.specifics[self.policy.index(i)]//(k + priority)
                        break
                        
                    except ZeroDivisionError:
                        
                        denom += self.specifics[self.policy.index(i)]// (k + (priority-1))
                        break
                        
                    
        return denom 
        
        
    def bottomup (self, law, fact, ruling):
        
        if law == 0:
            pass
        elif law == 1:
            ruling +=17
        elif law == -1:
            ruling -=17
            
            
        if fact == 0:
            pass
        elif fact == 1:
            ruling +=10
        elif fact == -1:
            ruling -=10
            
            
        return ruling
            
        
        
        
        





#############################  TESTS  ##################################
        
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

for i in range(1000):

    example = Judge(startterm = '2014-03-17', endterm = '2019-03-17')
    example.judgeAppointment()
    
df = odbc.exportData('Judges', 'Countries')
print(df.head(150))

    


