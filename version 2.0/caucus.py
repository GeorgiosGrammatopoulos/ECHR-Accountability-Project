import judge as js
import random as rd
import pandas as pd
import judge
import odbc
import utility as ut

#This class generates the caucus that we need to adjudicate a case. Each caucus is unique to a case - hence, the workings here correspond with the Cases table in the database (check odbc).

class Caucus:
    
    #Take particular note of the law and fact arguments: they are allowing for parameterized assessments later on
    def __init__(self, application_no, application_date, countryname, caucus, judgement_date, section, law = None, fact = None):
        
        session = odbc.exportData('Judges')
        for i in caucus:
            
            judgeinfo = session[(session['lastname'] == caucus[0]) & (session['section'] == section)]            
            
                 
        self.application_no = application_no
        self.application_date = application_date
        self.caucus = caucus
        self.favor = forvote
        self.against = againstvote
        self.casepolicy = casepolicy
        self.countryname = countryname
        self.law = law
        self.fact = fact
        self.judgement_date = judgement_date
        self.section = section
        
               

    def importCaucus(self):
                
        conn = odbc.connectData()
        
        odbc.importData(
            'Cases', 
            application_no = self.application_no,
            application_date = self.application_date,
            judgement_date = self.judgement_date,
            section = self.section)
            
        odbc.importData(
            'Reasonings',
            application_no = self.application_no,
            favor = self.favor,
            against = self.against)
            
            
        return odbc.exportData('Countries', 'Judges', 'Cases', 'Reasonings')
        
        
        
#class Subcaucus(Caucus):
    
    #def __init__: