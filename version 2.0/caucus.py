import judge as js
import random as rd
import pandas as pd
import judge
import odbc
import utility as ut
import string
import reasonings as rs

#This class generates the caucus that we need to adjudicate a case. 
#Each caucus is unique to a case - hence, the workings here correspond with the Cases table in the database (check odbc).

class Caucus:
    
    #Take particular note of the law and fact arguments: they are allowing for parameterized assessments later on
    def __init__(
        self, 
        application_no, 
        application_date, 
        countryname, 
        judgement_date,
        pool = None, #mutually exclusive with instance. either you have judge objects, or judges' names
        instance = None, 
        casepolicy = None, 
        law = None, 
        fact = None
        ):
        
        
        if instance:
            session = odbc.exportData('Judges')
            instances = instance.split(',')  #in input functions, the caucus will be a string of judge lastnames
            pool = []
            for i in range(0, len(instances)):
                #make sure it''s the right judge, in the right session
                #it may become necessary to constrain terms for seizing
                
                lookup = str(instances[i])
                querying= session.query(f"lastname == '{lookup}'").index 
                member = judge.Judge(
                    startterm = str(session['startterm'].iloc[querying]), 
                    countrynames = str(session['countryname'].iloc[querying]), 
                    firstnames =  str(session['firstname'].iloc[querying]), 
                    lastnames = str(session['lastname'].iloc[querying]),
                    role = str(session['role'].iloc[querying]), 
                    section = str(session['section'].iloc[querying]), 
                    endterm = str(session['endterm'].iloc[querying])
                    )
                pool.append(member)
            
                 
        self.application_no = application_no
        self.application_date = application_date
        self.caucus = pool
        self.casepolicy = casepolicy
        self.countryname = countryname
        self.law = law
        self.fact = fact
        self.judgement_date = judgement_date        
               
    #Function to import caucus information. Bear in mind: This stores to Cases!
    def importCaucus(self):
                
        conn = odbc.connectData()
        
        members = []
        
        for i in self.caucus:
            members.append(i.lastname)
            
        members = ",".join(members)
        
        odbc.importData(
            'Cases', 
            application_no = str(self.application_no),
            application_date = str(self.application_date),
            judgement_date = str(self.judgement_date),
            countryname = str(self.countryname),
            caucus = str(members)
            )            
            
        return odbc.exportData('Countries', 'Judges', 'Cases')
        
        
     #vote casting. the  president votes last, which must affect group dynamics
     #but that is a matter of refinement rather than specific policy
    def votingProcess (self, respondent, casepolicy, law, fact):
        
        tallyfavor = []
        votefavor = 0
        tallyagainst = []
        voteagainst= 0
        opinions = []
         
        
        for i in self.caucus:
            
            opinion = rs.topdown(i, casepolicy, respondent) 
            
            opinion = rs.bottomup (i, law, fact, opinion)
            
            
            if opinion > 0:        #the applicant bears the burden of proof. than amounts for the 0
                i.vote = True
                votefavor += 1
                tallyfavor.append(i)
            if opinion<= 0:
                i.vote = False
                voteagainst += 1
                tallyagainst.append(i)
                
            i.opinion = opinion
            opinions.append(opinion)
            
            
        if votefavor > voteagainst:
            
            outcome = True
            
        else:
            
            outcome = False
            
        opinions = dict(zip(self.caucus, opinions))
            
        return [tallyfavor, tallyagainst, outcome, opinions]
        
        
#after voting, judges tend to congregate. this subclass represents that
class Subcaucus(Caucus):
    
    def __init__(self, label, supers, evaluate=0):  #label is a boolean which determines win-loss
                                                        #supers is an instance of Caucus - must exist before instantiating
        members = []
        evaluation = evaluate      
        
        self.label = label
        for i in supers.caucus:
            
            if i.vote == label:
                
                members.append(i)
                evaluation += i.opinion   #splitting judges according to their vote
                
            
        self.application_no = supers.application_no
        self.application_date = supers.application_date
        self.countryname = supers.countryname
        self.judgement_date = supers.judgement_date
        self.caucus = members
        self.evaluation = evaluation
        
    
    #static to form the two subacucuses    
    @staticmethod
    def formulating(supers):
        
        grouping = []
        indicators = [False, True]
        
        for i in indicators:  #notice how the indexes represent true and false
            
            interobj = Subcaucus(i, supers)
            grouping.append(interobj)
            
            
        return tuple(grouping)
