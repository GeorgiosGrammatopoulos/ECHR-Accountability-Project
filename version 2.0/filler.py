import random as rd
import pandas as pd
import utility as ut
import datetime
import odbc
import judge
import caucus
import reasonings as rs
import applicant


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
def generateJudge (pool = None, listing = None, index = None):
    
    if pool == None:
            
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
    elif listing:
        
        if index:
            
            return listing[index]
            
        else:
            
            return listing [rd.randint(0, len(listing))]
        
    else:
        
        judges = []
        pool = exportData('Judges')
        
        for i in range(0, pool.shape[0]):
            myjudge = judge.Judge(
                startterm = pool.loc[i, 'startterm'], 
                countrynames = pool.loc[i, 'countrynames'], 
                firstnames = pool.loc[i, 'firstnames'], 
                lastnames = pool.loc[i, 'lastnames'], 
                role = pool.loc[i, 'role'], 
                section = pool.loc[i, 'section'], 
                endterm = pool.loc[i, 'endterm'], 
                opinion = pool.loc[i, 'opinion'],
                )
            judges.append[myjudge]
        
        if index == None:
            indie = len(judges)        
            myjudge = judges[rd.randint(0, indie)]
        else:
            myjudge = judges[index]
            
            
    return myjudge
        
        


def generateCaucus (respondent, application_no = None, pool = None, listing = None, index = None):
    
    members = []
    original = []
    countries = []
    
    
    while True:
        
        myjudge = generateJudge(pool = pool, listing = listing, index = index)

        if myjudge.countryname in countries:
            continue
        if (myjudge.countryname != respondent) and (len(countries) == 6):
            continue
            
        myjudge.judgeImport()
        original.append(myjudge)
        countries.append(myjudge.countryname)
        
        if len(countries) == 7:
            
            break
            
        
    df = odbc.exportData('Judges')
    
    print(df.shape)
        
    for i in range(0, 7):
        
        name = df['lastname'].iloc[i]
        members.append(name)
        
    instance = ','.join(members)
    if application_no == None:
        application_no = rd.randint(0,999999)
    law = rd.randint(-10, 10)
    fact = rd.randint (-10, 10)
    application_date = ut.randomDate()
    judgement_date = ut.randomDate()
    
    
    mycaucus = caucus.Caucus(
        application_no, 
        application_date, 
        respondent, 
        instance, 
        judgement_date,
        law, 
        fact
        )
            
    for i in range (0, len(mycaucus.caucus)):
        
        mycaucus.caucus[i] = original[i]
        
    df = mycaucus.importCaucus()
    
    df = df.dropna(subset = ['lastname']).reset_index(drop = True)
    
    return [mycaucus, df]
    



def generateApplicant(application_no = None):
    
    listed = odbc.exportData('Applicants')
    
    if application_no == None:
        application_no = listed.shape[0]
    
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
            print(f'{key}')
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




def generateCase():
    
    elects = []
    for i in range(0, 300):
        elect = generateJudge()
        elects.append(elect)
        
    listed = odbc.exportData('Cases')
    application_no = listed.shape[0]
    
    countryname = rd.choice(states) 
    
    caucus = generateCaucus(countryname, application_no = application_no, listing = elects)
    
    judges = caucus[0]
    judges = judges.caucus
    
    for i in judges:
        print(i.policy)
    
    main = caucus[0]
    

    x = rd.choices(
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 
        weights=[1000, 500, 300, 200, 100, 50, 250, 120, 6, 3], 
        k=1)[0]
    for i in range (0, x):
        generateApplicant(application_no)
        
    df = odbc.exportData('Cases')
    
    return caucus
    
    
    
def generateReasoning():

    instance = generateCase()
    dfinstance = instance[1]
    instance = instance[0]
    parties = odbc.exportData('Applicants')
    parties = parties.query(f'application_no == {instance.application_no}')
    policies = []
    law = rd.randint(-10, 10)
    fact = rd.randint (-10, 10)
    
    for i in parties.columns.tolist():
        
         for k in range(0, parties.shape[0]):
             
             if parties.loc[k, i] == True:
                 policies.append(i)
    
    first_result = rs.winLoss(instance, instance.countryname, policies, law, fact)
    
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
    
    print(f'Legal position: {law}')
    print(f'Factual assessment: {fact}')
    print(parties.head())
    
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
    
    
    if first_result[2] == 'win':
        
        for i in range(0, parties.shape[0]):
        
            amounts = rs.amountCalc(instance, dictAsk, dictCounter)
            
            print(amounts.items())
            
            mdiff =  dictAsk['material'] - amounts['material']
            print(mdiff)
            nmdiff = int(dictAsk['non_material'] - amounts['non_material'])
            print(nmdiff)
            cediff = dictAsk['ce'] - amounts['ce']
            print(cediff)
            
            odbc.importData('Reasonings',
                application_no = instance.application_no,
                firstname = parties.loc[i, 'firstname'],
                lastname = parties.loc[i, 'lastname'],
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
    
    
    else:
        
        for i in range(0, parties.shape[0]):
            
            odbc.importData('Reasonings',
                application_no = instance.application_no,
                firstname = str(parties.loc[i, 'firstname']),
                lastname = (parties.loc[i, 'lastname']),
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
        
    df = odbc.exportData('Reasonings')
    df = df.query(f'application_no == {instance.application_no}')
    print('\n\n\n\n', first_result[2], '\n\n\n\n')
    return df
            









    
####################### WHITE BOX UNIT TESTS ###########################

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

#Unit 1: Database connection, creation, import, export

#Code:
#odbc.connectData()
#odbc.createDatabase()
#odbc.importData(
#    'Judges', 
#    firstname = ut.random_name(), 
#    lastname = ut.random_name(), 
#    role = 'Judge'
#    )
#df = odbc.exportData('Judges')
#print(df.head(1))

#Result: success

#----------------------------------------------------------------------#

#Unit 2: Judge random generation

#Code
#myjudge = generateJudge()
#print(myjudge.firstname, myjudge.lastname, myjudge.startterm, sep = "\n")

#Result: success

#----------------------------------------------------------------------#

#Unit 3: Parsing judge into database

#Code
#odbc.createDatabase()
#myjudge = generateJudge()
#myjudge.judgeImport()
#df = odbc.exportData('Judges')
#print(df.head(1))

#Result: success

#----------------------------------------------------------------------#

#Unit 4: Building an effective caucus

#Code:
#odbc.createDatabase()
#mycaucus = generateCaucus('Andorra')
#print(mycaucus.head(10))

#Result: success

#----------------------------------------------------------------------#

#Unit 5: Building an effective applicant
#Code:
#odbc.createDatabase()
#for i in range(0, 100):
#    generateApplicant()
#df = odbc.exportData('Applicants')
#print(df.head(100))

#Result: success

#----------------------------------------------------------------------#

#Unit 6: Building an effective case
#Code:
#odbc.createDatabase()
#df = generateCase()
#print (df.head(1))
#applicants = odbc.exportData('Applicants')
#judges = odbc.exportData('Judges')
#print(applicants.head(30))
#print(judges.head(30))

#Result: success

#----------------------------------------------------------------------#


#Unit 7: Building an effective reasoning

#Code:
odbc.createDatabase()
df = generateReasoning()
print(df.head(20))

#Result: success

#----------------------------------------------------------------------#

