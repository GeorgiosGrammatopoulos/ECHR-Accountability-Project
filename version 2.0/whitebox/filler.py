import random as rd
import pandas as pd
import utility as ut
import datetime
import odbc
import judge
import caucus
import reasonings as rs
import applicant
from multiprocessing import Process, Pool, freeze_support


states = [   #List of the CoE states
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

#function generating one single judge
#the pool parameter is essentially a question: do we have a pool of random judges
#if so, we choose a judge from there; if not, we generate a new one
def generateJudge (countrynames = None, listing = None, index = None):
    
    if listing:        #In case I will need to simulate the behaviour of specific judges
        if index:
            return listing[index]
        else:
            return listing [rd.randint(0, len(listing))]
        

    else:
            
        policies = {} #Dictionary to be filled in the generation of a random judge
                
        df = odbc.exportData('Applicants')  #export a list of potential policies
        potentials = df.columns.tolist()
                
        for i in potentials:
            
            coin = rd.choice([True, False])    #This chunk represents the generation of individual bias. In lack of different indications, it is considered random, and it may stem from anywhere
            if coin:
                policies[i] = rd.randint(-9, 9)
            else:
                continue
                
        startterm = ut.randomDate()
        if countrynames == None:
            countrynames = rd.choice(states)   #random state out of the candidates (see list at the beginning)
        firstnames = ut.random_name(8)  #random firstname, genderless. Take that into account
        lastnames = ut.random_name(8)  #random firstname, genderless. Take that into account
        role = 'Judge'   #since there are no weights yet on the impact of the president, all judges will be designated as such
        myjudge = judge.Judge(
            startterm = startterm, 
            countrynames = countrynames, 
            firstnames = firstnames, 
            lastnames = lastnames, 
            role = role, 
            policy = policies
            )
         
            
    return myjudge
        
        

def generateApplicant(application_no):
    
    listed = odbc.exportData('Applicants')
    
    firstname = ut.random_name()
    
    lastname = ut.random_name()
        
    natural = rd.choice([True, False])

    female = rd.choice([True, False]) if natural == True else False
    
    sa_nationality = False
    ee_nationality = False
    asian_nationality = False
    african_nationality = False
    geo_dummies = {
        'sa_nationality': False, 
        'ee_nationality' : False, 
        'asian_nationality' : False, 
        'african_nationality' : False
        }
    if natural:
        geo_dummies['sa_nationality'] = rd.choices([True, False], weights = [10, 90])[0]
        if geo_dummies['sa_nationality'] == True:
            pass
        else:
            geo_dummies['asian_nationality'] = rd.choices([True, False], weights = [40, 60])[0]
            if geo_dummies['asian_nationality'] == True:
                pass
            else:
                geo_dummies['african_nationality'] = rd.choices([True, False], weights = [20, 80])[0]
                if geo_dummies['african_nationality'] == True:
                    pass
                else:
                    geo_dummies['ee_nationality'] = rd.choices([True, False], weights = [30, 70])[0]
        sa_nationality = geo_dummies['sa_nationality']
        ee_nationality = geo_dummies['ee_nationality']
        asian_nationality = geo_dummies['asian_nationality']
        african_nationality = geo_dummies['african_nationality']
          
            
    undocumented = any(geo_dummies.values()) and rd.choice([True, False])
    
    religion_lack = rd.choice([True, False]) if natural else False
    
    if natural and not religion_lack:
        religion = rd.choices([0, 1, 2], weights=[50, 30, 20], k=1)[0]
    else:
        religion = 2
        
    religion_muslim = religion == 0
    religion_other = religion == 1
        
    sexuality_other = rd.choice([True, False]) if natural else False
    
    gender_other = rd.choice([True, False]) if natural else False
    
    radical_political = rd.choice([True, False]) if natural else False
    
    radical_social = rd.choice([True, False]) if natural else False
    
    criminal = rd.choice([True, False]) if natural else False
    
    felon = rd.choice([True, False]) if criminal else False
    
    official = rd.choice([True, False]) if natural else False
    
    listed = odbc.exportData('Applicants')
    listed = listed.columns.tolist()
    relevant = any(rd.choice([True, False]) for dummy in listed)
    
    nationality = None
    count = 0
    for key,value in geo_dummies.items():
        if value == True:
            nationality = f'{key}'
            break
        else:
            count+=1
    if count == 4:
        nationality = 'first world'
    
    myapplicant = applicant.Applicant(
        firstname,
        lastname,
        nationality,
        female,
        natural,
        sa_nationality,
        asian_nationality,
        ee_nationality,
        african_nationality,
        undocumented,
        religion_lack,
        religion_muslim,
        religion_other,
        sexuality_other,
        gender_other,
        radical_political, 
        radical_social,
        criminal,
        felon,
        official,
        relevant,
        application_no
        )
    
    myapplicant.importApplcant()
    
    return myapplicant




def generateReasoning():

    #Judges are elected and move on with their duties
    elects = []
    for i in states:
        elect = generateJudge(i)
        elects.append(elect)
        elect.judgeImport()


    #Then, judges get to constant work, for an extended period of time
    for q in range(0, 5000):
       
       #When an application is submitted, it essentially contains an application no (secretariat), a respondent and a just satisfaction
        #request
        application_no = q
        countryname = rd.choice(states) 
        dictAsk = {
            'material': rd.randint(1, 99999),
            'non_material': rd.randint(1, 99999),
            'ce': rd.randint(1, 9999)
        }
        dictCounter = {
            'material': 0,
            'non_material': 0,
            'ce': 0
        }    

        original = []                #When the time comes to adjudicate, we assign six random judges and the national one
        countriesrep = []
        lastnames = [] 
        judgeord = list(range(len(elects)))
        rd.shuffle(judgeord)
        for i in judgeord:
            prosp = elects[i]
            if prosp.countryname in countriesrep:
                continue
            if (prosp.countryname != countryname) and (len(countriesrep) == 6):
                continue
            original.append(prosp)
            countriesrep.append(prosp.countryname)
            lastnames.append(prosp.lastname)
            if len(countriesrep) == 7:
                break
                

        #Additional instance information occur with the examination of a case
        law = rd.randint(-10, 10)
        fact = rd.randint (-10, 10)
        application_date = ut.randomDate()
        judgement_date = ut.randomDate()


        mycaucus = caucus.Caucus(        #The caucus forms up to produce a ruling
            application_no, 
            application_date, 
            countryname,
            judgement_date, 
            pool = original,
            law = law, 
            fact = fact
            )
        mycaucus.importCaucus()


        applicants= []    #In examining the case, the judges become familiar with all the facts, regardless relevance
        policy = []
        iterate = rd.randint(1,6)
        for i in range(iterate):
            myapplicant = generateApplicant(application_no)
            applicants.append(myapplicant)
            parties = vars(myapplicant)
            policy.append(parties)

        policies = []
        for i in policy:          #Case political impacts become evident while examining the case
            for quest, value in i.items():
                if value and quest not in policies:
                    policies.append(quest)
        mycaucus.casepolicy = policies
        

        first_result = rs.winLoss(mycaucus, mycaucus.countryname, law, fact)   #the judges determine indepdndently their vote
        contestl = False
        if law > 5 or law < -5:
            contestl = True
        resl = False
        if (first_result[3] == 'win') and (contestl):
            resl = True
        contestlf= False
        if fact > 5 or fact < -5:
            contestf = True
        resf= False
        if first_result[3] == 'win':
            resf = True

        
        
        if first_result[2] == 'win':      #if the applicant wins, compensation becomes relevant

            for i in applicants:
            
                amounts = rs.amountCalc(mycaucus, dictAsk, dictCounter)
                
                
                mdiff =  dictAsk['material'] - amounts['material']
                nmdiff = int(dictAsk['non_material'] - amounts['non_material'])
                cediff = dictAsk['ce'] - amounts['ce']
                
                odbc.importData('Reasonings',
                    application_no = mycaucus.application_no,
                    firstname = i.firstname,
                    lastname = i.lastname,
                    contest_law = contestl,
                    contest_lawres = resl,
                    contest_fact = contestl,
                    contest_factres = resf,
                    statute = '99',
                    favor = len(first_result[0]),
                    against = len(first_result[1]),
                    dissent_nj = False,
                    material_ask = dictAsk['material'],
                    non_material_ask = dictAsk['non_material'],
                    ce_ask = dictAsk['ce'],
                    material_award = amounts['material'],
                    non_material_award = amounts['non_material'],
                    ce_award = amounts['ce'],
                    material_diff = mdiff,
                    non_material_diff = nmdiff,
                    ce_diff = cediff,
                    )
        else:   #in case of loss, there is no relevance in discussing compensation
            for i in applicants:
                odbc.importData('Reasonings',
                    application_no = mycaucus.application_no,
                    firstname = i.firstname,
                    lastname = i.lastname,
                    contest_law = contestl,
                    contest_lawres = resl,
                    contest_fact = contestl,
                    contest_factres = resf,
                    statute = '99',
                    favor = len(first_result[0]),
                    against = len(first_result[1]),
                    dissent_nj = False,
                    material_ask = dictAsk['material'],
                    non_material_ask = dictAsk['non_material'],
                    ce_ask = dictAsk['ce'],
                    material_award = 0,
                    non_material_award =  0,
                    ce_award = 0,
                    material_diff = 0,
                    non_material_diff = 0,
                    ce_diff = 0
                    )
            
        print(f'Completed: {q/50}%')

    print('\n\n\nSample ready!\n\n\n')
    return odbc.exportData('Reasonings')





            
def call_generateReasoning(_):
    # Helper function to call generateReasoning without arguments
    generateReasoning()




def main():

    # Total number of times to run the function
    total_runs = 1
    # Optimal number of processes depends on your system and the nature of the task
    num_processes = 4  # Example, adjust based on your system

    with Pool(num_processes) as pool:
        # Use pool.starmap or pool.map with a dummy iterable when the function takes no arguments
        pool.map(call_generateReasoning, range(total_runs))

    # After all processes have completed, export data
    df = odbc.exportData('Reasonings')
    print(df.head(20))
    print(df.describe())





pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

odbc.createDatabase()
df = generateReasoning()
print(df.describe())

#df = odbc.exportData('Applicants')

#print(df.head(100))

#if __name__ == '__main__':
#    freeze_support()  # For Windows compatibility
#   main()