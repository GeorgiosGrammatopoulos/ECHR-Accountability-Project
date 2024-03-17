import random as rd
import pandas as pd
import utility as ut
import odbc


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
def generateJudge ():
            
    policy = {} #Dictionary to be filled in the generation of a random judge
            
    df = odbc.exportData('Applicants')  #export a list of potential policies
    potentials = df.columns.tolist()
            
    for i in potentials:
        
        coin = random.choice([True, False])    #This chunk represents the generation of individual bias. In lack of different indications, it is considered random, and it may stem from anywhere
        if coin:
            policy[i] = rd.randint(-7, 7)
        else:
            continue
            
    countrynames = rd.choice(states)   #random state out of the candidates (see list at the beginning)
            
    firstnames = ut.random_name(8)  #random firstname, genderless. Take that into account
    
    lastnames = ut.random_name(8)  #random firstname, genderless. Take that into account
    
    role = 'Judge'   #since there are no weights yet on the impact of the president, all judges will be designated as such
    
    return Judge (startterm, endterm, countrynames, firstnames, lastnames, role, policies)


def generateCaucus ():
    
    application_no = rd.randint(0,999999)
    countryname = rd.choice(states)
    law = randint(-17, 17)
    fact = randint (-10, 10)
    application_date = ut.randomDate()
    judgement_date = ut.randomDate()
    


def generateApplicant(num_entries, applicant_data):
    

    for i in range(num_entries):
        
        natural = rd.choice([True, False])
        
        female = rd.choice([True, False]) if natural == True else False
        
        # Geographical dummies
        geo_dummies = [False, False, False]  # Southeast Asian, Asian, African
        if natural:
            geo_index = random.choices([0, 1, 2, 3], weights=[10, 40, 20, 30], k=1)[0]
            if geo_index != 3:
                geo_dummies[geo_index] = True
        undocumented = any(geo_dummies) and random.choice([True, False])
        religion_lack = random.choice([True, False]) if natural else False
        
        if natural and not religion_lack:
            religion = random.choices([0, 1, 2], weights=[50, 30, 20], k=1)[0]
        else:
            religion = 2
        religion_muslim = religion == 0
        religion_other = religion == 1
        
        sexuality_other = random.choice([True, False]) if natural else False
        gender_other = random.choice([True, False]) if natural else False
        radical_political = random.choice([True, False]) if natural else False
        radical_social = random.choice([True, False]) if natural else False
        criminal = random.choice([True, False]) if natural else False
        felon = random.choice([True, False]) if criminal else False
        official = random.choice([True, False]) if natural else False

        relevance_dummies = [
            female, 
            *geo_dummies, 
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
            official]
        relevant = any(random.choice([True, False]) for dummy in relevance_dummies if dummy)

        entry_dict = {
            'firstname': random_name(),
            'lastname': random_name(),
            'female': female,
            'natural': natural,
            'southeast_asian_nationality': geo_dummies[0],
            'asian_nationality': geo_dummies[1],
            'african_nationality': geo_dummies[2],
            'undocumented': undocumented,
            'religion_lack': religion_lack,
            'religion_muslim': religion_muslim,
            'religion_other': religion_other,
            'sexuality_other': sexuality_other,
            'gender_other': gender_other,
            'radical_political': radical_political,
            'radical_social': radical_social,
            'criminal': criminal,
            'felon': felon,
            'official': official,
            'relevance': relevant
        }
        
        # Create a DataFrame for the current entry
        df = pd.DataFrame([entry_dict])

        # Concatenate the current entry DataFrame to the main DataFrame
        applicant_data = pd.concat([applicant_data, df], ignore_index=True)

    return applicant_data


###The next step is to define the material scope of the case


def generateCase(applicant_df, num_cases):
    casedata = []

    previous_case_id = None

    for i in range(num_cases):
        # Fetch first name and last name from the applicant dataframe
        first_name = applicant_df.loc[i % len(applicant_df), 'firstname']
        last_name = applicant_df.loc[i % len(applicant_df), 'lastname']

        # Generate case ID
        if i == 0 or random.choice([True, False]):  # 50% chance to share a case ID with the previous one
            case_id = f"case_{i + 1}"
        else:
            case_id = previous_case_id

        # Randomly assign values to other columns
        statute = random.randint(1, 20)
        material_ask = random.randint(0, 99999)
        non_material_ask = random.randint(0, 99999)
        ce_ask = random.randint(0, 99999)

        # Prepare the entry
        entry = {
            'case_id': case_id,
            'statute': statute,
            'firstname': first_name,
            'lastname': last_name,
            'win': None,  # To be filled later
            'material_ask': material_ask,
            'non_material_ask': non_material_ask,
            'ce_ask': ce_ask,
            'material_award': None,  # To be filled later
            'non_material_award': None,  # To be filled later
            'ce_award': None  # To be filled later
        }

        instance_data.append(entry)
        previous_case_id = case_id

    return pd.DataFrame(instance_data)



def generate_reasoning_data(instance):
    
    all_entries = []
    used_case_ids = set()
    
    for _, row in instance.iterrows():
        case_id = row['case_id']

        if case_id in used_case_ids:
            continue
        used_case_ids.add(case_id)

        respondent = random.choice(council_of_europe_states)
        contest_law = random.choice([True, False])
        contest_fact = random.choice([True, False])
        law_reasoning = random.choice([True, False]) if contest_law == False else True
        fact_reasoning = random.choice([True, False]) if contest_fact else False

        judge_decision = combined_mock_judge_decision()
        votes_for = judge_decision["In favor of litigant 2 (third party)"]

        entry_df = pd.DataFrame([{
            'case_id': case_id,
            'respondent': respondent,
            'contest_law': contest_law,
            'contest_fact': contest_fact,
            'law_reasoning': law_reasoning,
            'fact_reasoning': fact_reasoning,
            'national_judge': False if national_judge_decision == 1 else True,
            'for': votes_for,
            'total': 7  # Total number of judges
         }])

        all_entries.append(entry_df)

    return pd.concat(all_entries, ignore_index=True)

