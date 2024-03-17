###This is an input-output functionality. It is supposed to connect in and out of an existing database. modify as appropriate.

import pyodbc
import pandas as pd
import csv
import os





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
    
    server = 'LAPTOP-7NBR16RS\SQLEXPRESS01' 
    database = 'echr'
    conn = pyodbc.connect('DRIVER={SQL Server};SERVER=' + server + ';DATABASE=' + database + ';Trusted_Connection=yes;')

    return conn
    
    # look up https://learn.microsoft.com/en-us/sql/connect/odbc/dsn-connection-string-attribute?view=sql-server-ver16 for connection keywords
    
# database creation function. only to be run once, if a database does not already exist.
# attention! the database will not run if another instance is online!








def createDatabase():
    
    check = 0
    
    try:
    
        conn = connectData()
        cursor = conn.cursor()
        inserts = ", ".join([f"('{i}')" for i in states])
        
        check += 1
        
    except pyodbc.Error as e:
        
        print(f'Fatal error: {e}\nPlease contact systems administration-0')
        
    try:
        
        cursor.execute('IF OBJECT_ID(\'Applicants\', \'U\') IS NOT NULL DROP TABLE Applicants')
        
        cursor.execute('IF OBJECT_ID(\'Reasonings\', \'U\') IS NOT NULL DROP TABLE Reasonings')
        
        cursor.execute('IF OBJECT_ID(\'Cases\', \'U\') IS NOT NULL DROP TABLE Cases')
        
        cursor.execute('IF OBJECT_ID(\'Judges\', \'U\') IS NOT NULL DROP TABLE Judges')
        
        cursor.execute('IF OBJECT_ID(\'Sections\', \'U\') IS NOT NULL DROP TABLE Sections')
        
        cursor.execute('IF OBJECT_ID(\'Countries\', \'U\') IS NOT NULL DROP TABLE Countries')
        
        check += 1
        
    except pyodbc.Error as e:
        
        print(f'Fatal error: {e}\nPlease contact systems administration-1')
        
    try:

        cursor.execute('USE echr')
        
        check += 1
        
    except pyodbc.Error as e:
        
        print(f'Fatal error: {e}\nPlease contact systems administration-2')
        
    
    try:
        
        cursor.execute('CREATE TABLE Countries (countryname VARCHAR(30) PRIMARY KEY)')
        
        check += 1
        
    except pyodbc.Error as e:
        
        print(f'Fatal error: {e}\nPlease contact systems administration-3')
        
    try:
        
        cursor.execute(f"INSERT INTO Countries (countryname) VALUES {inserts}")
        
        check += 1
        
    except pyodbc.Error as e:
        
        print(f'Fatal error: {e}\nPlease contact systems administration-4')
        

    try:
        
        cursor.execute('CREATE TABLE Judges ('
            'firstname VARCHAR(30),'  #assigned randomly until not
            'lastname VARCHAR(30),'   #assigned randomly until not
            'role VARCHAR(30),'   #promotion record, Judge in instantiation
            'countryname VARCHAR(30) FOREIGN KEY REFERENCES Countries(countryname),'  #assign at instantiation
            'startterm DATE,' #assign at instantiation
            'endterm DATE,' #assign at instantiation, make a corrector
            'section VARCHAR(30),' #assign at assignment, starts as null
            'PRIMARY KEY (firstname, lastname, role))' 
            )
            
        check += 1
            
    except pyodbc.Error as e:
        
        print(f'Fatal error: {e}\nPlease contact systems administration-5')
        
        
    try:
        
        cursor.execute('CREATE TABLE Cases ('
            'application_no VARCHAR(30) PRIMARY KEY,'
            'name VARCHAR(30),'
            'application_date DATE,'
            'countryname VARCHAR(30) FOREIGN KEY REFERENCES Countries(Countryname),'
            'judgement_date VARCHAR(30),'
            'reference VARCHAR(100),'
            'footnote VARCHAR(100),'
            'link VARCHAR(100),'
            'section VARCHAR(30),
            'judges VARCHAR(300))'
            )
            
        check += 1
            
    except pyodbc.Error as e:
        
        print(f'Fatal error: {e}\nPlease contact systems administration-6')
        
                
    try:
        
        cursor.execute('CREATE TABLE Reasonings ('
            'application_no VARCHAR(30) FOREIGN KEY REFERENCES Cases(application_no),'
            'firstname VARCHAR(30),'
            'lastname VARCHAR(30),'
            'contest_law BIT,'
            'contest_lawres BIT,'
            'contest_fact BIT,'
            'contest_factres BIT,'
            'statute VARCHAR(3),'
            'favor INT,'
            'against INT,'
            'dissent_nj BIT,'
            'material_ask INT,'
            'non_material_ask INT,'
            'ce_ask INT,'
            'material_award INT,'
            'non_material_award INT,'
            'ce_award INT,'
            'material_diff INT,'
            'non_material_diff INT,'
            'ce_diff INT,'
            'PRIMARY KEY (application_no, firstname, lastname, statute))'
            )
            
        check += 1

    except pyodbc.Error as e:
        
        print(f'Fatal error: {e}\nPlease contact systems administration-7')
        
    try:
                
        cursor.execute('CREATE TABLE Applicants('
            'firstname VARCHAR(30),'
            'lastname VARCHAR(30),'
            'application_no VARCHAR(30) FOREIGN KEY REFERENCES Cases(application_no),'
            'nationality VARCHAR(30),'
            'female BIT,'   #dummy indicator of female applicants
            'natural BIT,' #dummy indicator of natural persons (to exclude corporate entities etc)
            'southeast_asian_nationality BIT,'  #dummy of nationals of south-east Asian countries
            'asian_nationality BIT,'#dummy of nationals of Asian countries; grouping serves the function of commonplace biases
            'african_nationality BIT,' #dummy of nationals of African countries
            'undocumented BIT,' #dummy of nationals of undocumented migrants
            'religion_lack BIT,'#dummy of nationals who do not belong in an organized religion
            'religion_muslim BIT,' #dummy of Muslim individuals; they are a particularly sensitive group in Europe
            'religion_other BIT,' #dummy of nationals who do not belong in one of the predominant Christian denominations
            'sexuality_other BIT,' #dummy of non-straight individuals
            'gender_other BIT,'   #dummy of individuals who do not identify with the gender assigned to them at birth
            'radical_political BIT,'   #dummy of individuals who expressed views which are considered politically radical in their states of residence 
            'radical_social BIT,'   #dummy of individuals who expressed views which are considered socially radical in their states of residence
            'criminal BIT,'   #dummy of individuals who have committed a criminal offence
            'felon BIT,'  #dummy of individuals who have committed a serious offence according to their countries of origin
            'official BIT,' #dummy of individuals who held public office at the time of the violation
            'relevance BIT,'  #dummy indicating whether the identity of the applicant is related anyhow to their complaint'
            'PRIMARY KEY (firstname, lastname, nationality))'
            )
            
        check += 1
            
    except pyodbc.Error as e:
        
        print(f'Fatal error: {e}\nPlease contact systems administration-8')
        
        
    try:
        
        conn.commit()
        
        check += 1
        
    except pyodbc.Error as e:
        
        print(f'Fatal error: {e}\nPlease contact systems administration-9')
        
    if check == 10:
        
        print("Database creation successful! Bear in mind, your data is no more...")
        
        return True
        
        
        
        
        
        
        
        
def importData(table, **imports):
    
    
    try:
    
        conn = connectData()
        cursor = conn.cursor()
        
    except pyodbc.Error as e:
        
        print(f'Fatal error: {e}\nPlease contact systems administration-0')
        
    columns = ', '.join(imports.keys())  # Correct way to format column names
    placeholders = ', '.join(['?' for _ in imports])  # Correct way to format placeholders
    
    # Prepare SQL statement
    sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
    
    try:
        cursor.execute(sql, tuple(imports.values()))
        conn.commit()
        
        return True
        
    except pyodbc.Error as e:
        
        print(f'Fatal error: {e}\nPlease contact systems administration-10')
        
        return False      
        
        
        
        

def exportData(*args, connstring = None):
    
    global df
    df = pd.DataFrame()
    
    
    
    try:
    
        conn = connectData()
        cursor = conn.cursor()
        
        
    except pyodbc.Error as e:
        
        print(f'Fatal error: {e}\nPlease contact systems administration-0')
        
    
    for i in args:
        
        
        try:
        
           cursor.execute(f'SELECT * FROM {i} {connstring}')
            
            
        except pyodbc.Error as e:
            
            print(f'Fatal error: {e}\nPlease contact systems administration-11.{i}')
            
            
        try:
        
            with open('output.csv', 'w', newline='') as csvfile:
                csvwriter = csv.writer(csvfile)
                headers = [i[0] for i in cursor.description]  # column headers
                csvwriter.writerow(headers)
                for row in cursor:
                    csvwriter.writerow(row)

                
        except pyodbc.Error as e:
            
            print(f'Fatal error: {e}\nPlease contact systems administration-12.{i}')
            
        
        try:
        
            if df.empty:
                
                df = pd.read_csv('output.csv')
                
            else:
                
                df2 = pd.read_csv('output.csv')
                
                dfcol = df.columns.tolist()
                df2col = df2.columns.tolist()
                print(dfcol)
                print(df2col)
                common = None
                
                for i in dfcol:
                    
                    if i in df2col:
                        
                        common = i
                        break
                    
                df[common] = df[common].astype(str)
                df2[common] = df2[common].astype(str)

                df = pd.merge (df, df2, on = common, how='outer')
                    
            os.remove('output.csv')
                
        except pyodbc.Error as e:
            
            print(f'Fatal error: {e}\nPlease contact systems administration-13.{i}')
            
            
    return df
        
    
        
        
        
    

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
]sssss
