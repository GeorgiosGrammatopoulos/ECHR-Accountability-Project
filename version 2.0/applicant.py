class Applicant:
    
    def __init__(
        firstname,
        lastname,
        nationality,
        female,
        natural,
        sa_nationality,
        ee_nationality,
        asian_nationality,
        african_nationality,
        undocumented,
        non_religious,
        muslim,
        other_religion,
        other_sexuality,
        other_gender,
        radical_political, 
        radical_social,
        criminal,
        felon,
        official,
        relevance,
        application_no = None
        )
            
        self.firstname = firstname
        self.lastname = lastname
        self.application_no = application_no
        self.nationality = nationality
        self.female = female
        self.natural = natural
        self.sa_nationality = sa_nationality
        self.ee_nationality = ee_nationality
        self.asian_nationality = asian_nationality
        self.african_nationality = african_nationality
        self.undocumented = undocumented
        self.non_religious = non_religious
        self.muslim = muslim
        self.other_religion = other_religion
        self.other_sexuality = other_sexuality
        self.other_gender = other_gender
        self.radical_political = radical_political
        self.radical_social = radical_social
        self.criminal = criminal
        self.felon = felon
        self.official = official
        self.relevance = relevance
        
            
    def importApplcant(self):
        
        if not ((fulls['lastname'] == self.lastname) & (fulls['firstname'] == self.firstname) & (fulls['role'] == self.role)).any():
        #contigency: if a judge becomes promoted, they are re-inserted, only under a different role
        #will prove useful when we will test individual records and weights of presidents' opinion
        
            odbc.importData(
                'Judges',          
                firstname = f'{self.firstname}',
                lastname = f'{self.lastname}',
                application_no = f'{self.application_no}',
                nationality = f'{self.nationality}',
                female = f'{self.female = female}',
                natural = f'{self.natural = natural}',
                southeast_asian_nationality = f'{self.sa_nationality}',
                asian_nationality = f'{self.ee_nationality}',
                eastern_european_antionality = f'{self.asian_nationality}',
                african_nationality = f'{self.african_nationality}',
                undocumented = f'{self.undocumented}',
                religion_lack = f'{self.non_religious}',
                religion_muslim = f'{self.muslim}',
                religion_other = f'{self.other_religion}',
                sexuality_other = f'{self.other_sexuality}',
                gender_other = f'{self.other_gender}',
                radical_political = f'{self.radical_political}',
                radical_social = f'{self.radical_social}',
                criminal = f'{self.criminal}',
                felon = f'{self.felon}',
                official = f'{self.official}',
                relevance = f'{self.relevance}')
                    
            firstname = f'{nfirstname}', lastname = f'{nlastname}', role = f'{nrole}', startterm = f'{nstartterm}', endterm = f'{nendterm}', countryname = f'{ncountryname}')
                  
            return self
        
        else:
            
            return False
