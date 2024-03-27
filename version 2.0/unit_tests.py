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
#odbc.createDatabase()
#completed = 0
#processes = []
#for i in range(0, 5):
#    p = Process(target=generateReasoning)
#    processes.append(p)
#   p.start()
#    print(f'Completed: {i}%')
#    completed += 10
#p.join()
#df = odbc.exportData('Reasonings')
#print(df.head(20))
#print(df.describe())

#Result: success

#----------------------------------------------------------------------#
