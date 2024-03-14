###This is an input-output functionality. It is supposed to connect in and out of an existing database. modify as appropriate.

import pyodbc

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

# instantiate database: a database which is synced with a running pandas dataframe

def connectData():
    
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 18 for SQL Server};
        'SERVER=test;
        'DATABASE=test;
        'UID=user;
        'PWD=password')
    
    return conn
    
    # look up https://learn.microsoft.com/en-us/sql/connect/odbc/dsn-connection-string-attribute?view=sql-server-ver16 for connection keywords
    
# database creation function. only to be run once, if a database does not already exist.
# attention! the database will not run if another instance is online!

def createDatabase():
    
    
    try:
    
        conn = connectData()
        cursor = conn.cursor()

        cursor.execute('CREATE DATABASE data')

        cursor.execute('USE data')
        
        cursor.execute('CREATE TABLE Countries (name VARCHAR(30) PRIMARY KEY)')
        
        cursor.execute(f'INSERT INTO Countries (name) VALUES {', '.join([f'({i})' for i in states])}')

        cursor.execute('CREATE TABLE Sections (name VARCHAR(3) PRIMARY KEY)')
        
        cursor.execute('CREATE TABLE Judges
            'firstname VARCHAR(30),
            'lastname VARCHAR(30),
            'role VARCHAR(3)
            'country VARCHAR(30) FOREIGN KEY REFERENCES Countries(name),
            'startterm DATE,
            'endterm DATE,
            'section VARCHAR(3) FOREIGN KEY REFERENCES Sections(name),
            'PRIMARY KEY firstname, lastname, role)
            )
                
        cursor.execute('CREATE TABLE Applicants
            'firstname VARCHAR(30),
            'lastname VARCHAR(30),
            'nationality VARCHAR(30) FOREIGN KEY REFERENCES Countries(name),
            'PRIMARY KEY firstname, lastname, nationality)
            )
        
        cursor.execute('CREATE TABLE Cases (
            'application_no VARCHAR(30) PRIMARY KEY,
            'name VARCHAR(30)
            'application_date DATE,   
            'respondent VARCHAR(30) FOREIGN KEY REFERENCES Countries(name),
            'judgement_date DATE,
            'reference VARCHAR(100),
            'footnote VARCHAR(100),
            'link VARCHAR(100),
            'section VARCHAR(3) FOREIGN KEY REFERENCES Sections(name)
            )
        
        cursor.execute('CREATE TABLE Reasonings (
            'application_no VARCHAR(30) FOREIGN KEY REFERENCES Cases(application_no),
            'firstname VARCHAR(30),
            'lastname VARCHAR(30),
            'contest_law BIT,
            'contest_lawres BIT,
            'contest_fact BIT,
            'contest_factres BIT
            'statute VARCHAR(3),
            'for INT,
            'against INT,
            'dissent_nj BIT,
            'material_ask INT,
            'non_material_ask INT,
            'ce_ask INT,
            'material_award INT,
            'non_material_award INT,
            'ce_award INT,
            'material_diff INT,
            'non-material_diff INT,
            'ce_diff INT,
            'PRIMARY KEY application_no, firstname, lastname, statute'
            )


    except pyodbc.Error as e:
        
        print(f'Fatal error: {e}\nPlease contact systems administration')
        
        
def importData():
        
        # after the creation of database code


#This dataframe classifies a range of sensitive groups
applicant_col = [
    'firstname',
    'lastname',    #the first and lastname of the applicant(s). using that instead of the case identifier, because a single applicant may be engaged in plenty of cases
    'female',   #dummy indicator of female applicants
    'natural', #dummy indicator of natural persons (to exclude corporate entities etc)
    'southeast_asian_nationality',  #dummy of nationals of south-east Asian countries
    'asian_nationality', #dummy of nationals of Asian countries; grouping serves the function of commonplace biases
    'african_nationality', #dummy of nationals of African countries
    'undocumented', #dummy of nationals of undocumented migrants
    'religion_lack', #dummy of nationals who do not belong in an organized religion
    'religion_muslim', #dummy of Muslim individuals; they are a particularly sensitive group in Europe
    'religion_other', #dummy of nationals who do not belong in one of the predominant Christian denominations
    'sexuality_other', #dummy of non-straight individuals
    'gender_other',   #dummy of individuals who do not identify with the gender assigned to them at birth
    'radical_political',   #dummy of individuals who expressed views which are considered politically radical in their states of residence 
    'radical_social',   #dummy of individuals who expressed views which are considered socially radical in their states of residence
    'criminal',   #dummy of individuals who have committed a criminal offence
    'felon',  #dummy of individuals who have committed a serious offence according to their countries of origin
    'official', #dummy of individuals who held public office at the time of the violation
    'relevance'  #dummy indicating whether the identity of the applicant is related anyhow to their complaint
]

#This dataframe associates applicants with cases. Helpful in dealing with joined cases and multi-applicant cases
instance_col = [
    'case_id',   #the ID assigned to the case;
    'statute', #the statute whose violation is alleged
    'firstname', #the first name of one of the applicants;
    'lastname', #the last name of one of the applicants
    'win',  #whether the court found for a violation against the applicant
    'material_ask', #the amount asked by the applicant for material harm
    'non_material_ask', #the amount asked by the applicant for non-material harm
    'ce_ask',   #the amount asked by the applicant in costs and expenses
    'material_award',  #the amount awarded to the applicant for material harm
    'non_material_award', #the amount awarded to the applicant for non-material harm
    'ce_award', #the amount awarded to the applicant in costs and expenses
    'material_diff',    #the difference between ask and get for the material claims
    'non-material_diff',    #the difference between as and get for the non-material claims
    'ce_diff'    #the difference between ask and get for costs and expenses
]

#This dataframe maintains certain metrics of specific cases, which are deemed important for the research in hand
reasoning_col = [
    'case_id',   #the ID assigned to the case
    'respondent',  #the respondent state
    'contest_law', #dummy indicating whether there was a contest in law; when both parties agree on the law, they seek to have the facts established
    'contest_fact',  #dummy indicating whether there was a contest in fact; when both parties agree on the facts and the court dismisses the case, there is no room for factual bias
    'law_reasoning',  #dummy indicating whether there was a legal reasoning
    'fact_reasoning',  #dummy indicating whethere there was a factual reasoning; bias may manifest in the court accepting legal principles, but not fact assertions
    'national_judge', #dummy indicating the vote of the national judge. useful for regression analysis - so far, the only positively known dependence we are aware of
    'for', #number of votes in favor
    'total'  #number of votes in total
]

meta_col = [
    'case_id',   #the case ID assigned by the court
    'date',  #the date of the case
    'reference',  #the official reference for the case
    'footnote',   #the footnote for the case
    'link'   #the link to the case
]

dummy_columns = [
    'national_judge', 'female', 'natural', 'southeast_asian_nationality', 'asian_nationality', 
    'african_nationality', 'undocumented', 'religion_lack', 'religion_muslim', 
    'religion_other', 'sexuality_other', 'gender_other', 'radical_political', 
    'radical_social', 'criminal', 'felon', 'official', 'relevance', 
    'contest_law', 'contest_fact', 'law_reasoning', 'fact_reasoning', 'win'
]