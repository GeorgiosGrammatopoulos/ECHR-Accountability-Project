import judge as js
import random as rd
import pandas as pd
import judge
import odbc
import utility

class Caucus:
    
            
    def __init__(
        self, 
        application_no = None, 
        application_date = None, 
        casepolicy = None, 
        countryname = None, 
        law = None, 
        fact = None, 
        caucus = 7, 
        judgement_date = None,
        section = None
        ):
            
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
            'Ukraine']
            
        if application_no == None:
            application_no = rd.randint(0,999999)
        
        if application_date == None:
            application_date = input('Please fill in the application date:')
            
        if casepolicy == None:
            casepolicy = input('Please fill in the case policy weight:')
            
        if countryname == None:
            countryname = rd.choice(states)
            
        if law == None:
            law = input('Please fill in the weight for the legal assessment')
            
        if fact == None:
            fact = input('Please fill in the weight for the factual assessment')
            
        if judgement_date == None:
            judgement_date = input('Please fill in the judgement date')
            
        if section == None:
            section = input('Please fill in the section number')
            
        members = []
        composition = []
        favor = 0
        against = 0
        
            
        while True:
            
            current = len(members)
            
            myjudge = js.Judge('2024-03-14', '2024-03-14')
            
            if (len(members) == caucus - 1) and (countryname not in composition) and (myjudge.countryname != countryname):
                continue
            
            if myjudge.countryname in composition:
                continue
            else:
                members.append(myjudge)
                composition.append(myjudge.countryname)
            
            
            result = myjudge.topdown(casepolicy, countryname)
            result = myjudge.bottomup (law, fact, result)
            
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
        
        
        
#class Subcaucus(self, ):
    
    #def __init__: 
        
        
        
        




#############################  TESTS  ##################################
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

casepolit = rd.randint(-10, 10)


for i in range(1000):
    
    legal = rd.randint(-10, 10)
    factual = rd.randint(-10, 10)
    section = rd.randint (1, 10)

    example = Caucus(
        application_date = '2024-03-18', 
        casepolicy = casepolit, 
        law = legal, 
        fact = factual, 
        judgement_date = '2024-03-18',
        section = '10'
        )
            
    example.importCaucus()
    
odbc.exportData('Countries', 'Judges', 'Cases', 'Reasonings')

