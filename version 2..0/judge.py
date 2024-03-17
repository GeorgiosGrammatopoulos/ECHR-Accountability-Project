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

#This init function allows for policy input, if we become aware of a judge's policies. By default, we are unaware. Same goes for end of term.

    def __init__ (self, startterm, countrynames, firstnames, lastnames, role, section, endterm = None, policies = None #dictionary):
        
        
        self.countryname = countrynames
        self.firstname = firstnames
        self.lastname = lastnames
        self.role = role
        self.policy = policy
        self.specifics = specifics
        self.section = section
        self.startterm = startterm
        self.endterm = endterm
        
#Function for inputting judges and making sure that their potential promotions are accounted for
    
    def judgeAppointment (self):
        
        fulls = odbc.exportData('Judges')
        
        if not ((fulls['lastname'] == self.lastname) & (fulls['firstname'] == self.firstname) & (fulls['role'] == self.role)).any():
        #contigency: if a judge becomes promoted, they are re-inserted, only under a different role
        #will prove useful when we will test individual records and weights of presidents' opinion
                  
            nfirstname = str(self.firstname)
            nlastname = str(self.lastname)
            nrole = str(self.role)
            nstartterm = str(self.startterm)
            nendterm = str(self.endterm)
            ncountryname = str(self.countryname)
                    
            odbc.importData('Judges', firstname = f'{nfirstname}', lastname = f'{nlastname}', role = f'{nrole}', startterm = f'{nstartterm}', endterm = f'{nendterm}', countryname = f'{ncountryname}')
                  
            return self
        
        else:
            
            return False