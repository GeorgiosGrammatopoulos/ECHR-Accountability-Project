###Relational dataframes to populate

#Python packages that will be needed
import pandas as pd
import string
import random
from scipy.special import comb
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, classification_report, roc_auc_score
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score


# List of Council of Europe member states
council_of_europe_states = [
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

data = []


# Set option to display all columns (None means unlimited)
pd.set_option('display.max_columns', None)

# Optionally, you can also adjust the number of rows to display
pd.set_option('display.max_rows', None)



#Functions forming the relational data

applicant= pd.DataFrame(data, columns=applicant_col)
instance= pd.DataFrame(data, columns = instance_col)
reasoning= pd.DataFrame(data, columns=reasoning_col)
meta= pd.DataFrame(data, columns=meta_col)


for col in dummy_columns:
    if col in applicant.columns:
        applicant[col] = applicant[col].astype(bool)
    if col in instance.columns:
        instance[col] = instance[col].astype(bool)
    if col in reasoning.columns:
        reasoning[col] = reasoning[col].astype(bool)


###First step in formulating the complaint: The applicant who files


# Function for randomizing names
def random_name(length=6):
    return ''.join(random.choice(string.ascii_letters) for _ in range(length))

def generate_applicant_data(num_entries, applicant_data):
    
    # Initialize an empty DataFrame to start with

    for _ in range(num_entries):
        
        natural = random.choice([True, False])
        
        female = random.choice([True, False]) if natural == True else False
        
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
        current_entry_df = pd.DataFrame([entry_dict])

        # Concatenate the current entry DataFrame to the main DataFrame
        applicant_data = pd.concat([applicant_data, current_entry_df], ignore_index=True)

    return applicant_data


###The next step is to define the material scope of the case


def generate_instance_data(applicant_df, num_cases):
    instance_data = []

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



###The next step is to see how the judges decide

def mock_national_judge_decision_consequential_bias():
    # Replace this with your actual implementation for national judge decision-making
    return 1 if random.random() < 0.6 else 2  # Example: 60% chance to favor litigant 1

def combined_mock_judge_decision():
    total_judges = 7
    decisions = []

    # Ensure one national judge

    global national_judge_decision

    national_judge_decision = mock_national_judge_decision_consequential_bias()
    decisions.append(national_judge_decision)

    # Process for the remaining non-national judges
    for _ in range(total_judges - 1):  # Subtract one for the national judge already accounted for
        # Non-national judge decision-making process
        decision = 1 if random.choice([True, False]) else 2
        decisions.append(decision)

    decision_count = {
        "In favor of litigant 1 (state)": decisions.count(1),
        "In favor of litigant 2 (third party)": decisions.count(2)
    }

    return decision_count

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

def stats(applicant, reasoning, instance):

    return print(applicant.head(30), applicant.describe(), reasoning.head(30), reasoning.describe(), instance.head(30), instance.describe(), sep= '\n\n\n')

def check_mean(reasoning):

    add = 0

    for i in range (0, 1000):

         add += reasoning['for'].mean()

    return add/1000



# Assuming you have your instance dataframe (instance) ready
applicant = generate_applicant_data(10000, applicant)
instance = generate_instance_data(applicant, 1000)
reasoning = generate_reasoning_data(instance)



###For the final step: make the judges decide on compensation independently, where the applicant has won

# Assuming instance_df and reasoning_df are already defined
# Update instance_df with win/loss and compensation data

for i, row in instance.iterrows():
    case_id = row['case_id']
    reasoning_row = reasoning[reasoning['case_id'] == case_id].iloc[0]

    # Determine win/loss
    win = reasoning_row['for'] >= 4
    instance.at[i, 'win'] = win

    # If the applicant won, calculate awards
    if win:
        majority_votes = reasoning_row['for']
        total_ratio = sum([random.uniform(0.1, 1) for _ in range(majority_votes)]) / majority_votes

        instance.at[i, 'material_award'] = row['material_ask'] * total_ratio
        instance.at[i, 'non_material_award'] = row['non_material_ask'] * total_ratio
        instance.at[i, 'ce_award'] = row['ce_ask'] * total_ratio
        instance.at[i, 'material_diff'] = instance.at[i, 'material_ask'] - instance.at[i, 'material_award']
        instance.at[i, 'non_material_diff'] = instance.at[i, 'non_material_ask'] - instance.at[i, 'non_material_award']
        instance.at[i, 'ce_diff'] = instance.at[i, 'ce_ask'] - instance.at[i, 'ce_award']
    else:
        instance.at[i, 'material_award'] = 0
        instance.at[i, 'non_material_award'] = 0
        instance.at[i, 'ce_award'] = 0
        instance.at[i, 'material_diff'] = instance.at[i, 'material_ask'] - instance.at[i, 'material_award']
        instance.at[i, 'non_material_diff'] = instance.at[i, 'non_material_ask'] - instance.at[i, 'non_material_award']
        instance.at[i, 'ce_diff'] = instance.at[i, 'ce_ask'] - instance.at[i, 'ce_award']



#initial tests
print('Voting patterns:\n\n\n', reasoning['for'].value_counts(), end = '\n\n\n')
print('Winning patterns:\n\n\n', instance['win'].value_counts(), end = '\n\n\n')
stats(applicant, reasoning, instance)
        




#########################################################     LOGISTIC REGRESSION MODEL FOR WIN RATIO     ############################################################################







# Assuming 'instance' and 'applicant' dataframes are ready
# Merging instance data with applicant data on first and last names
merged_df = pd.merge(instance, applicant, on=['firstname', 'lastname'])
merged_df = pd.merge(merged_df, reasoning, on=['case_id'])


print('Binomial logistic regression tests accounting for sensitivity to bias:', end= '\n\n\n')

# Selecting relevant features for the model
# For example: 'material_ask', 'non_material_ask', 'ce_ask', and some applicant features
X = merged_df[[
    'female', 'natural', 'southeast_asian_nationality', 'asian_nationality', 
    'african_nationality', 'undocumented', 'religion_lack', 'religion_muslim', 
    'religion_other', 'sexuality_other', 'gender_other', 'radical_political', 
    'radical_social', 'criminal', 'felon', 'official', 'relevance'
]]  # Add other relevant features
y = merged_df['win'].astype(int)  # Convert boolean to int

# Splitting the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


# Create and train the logistic regression model
logistic_model = LogisticRegression(max_iter=1000)  # Increase max_iter if needed
logistic_model.fit(X_train, y_train)

# Make predictions
y_pred = logistic_model.predict(X_test)
y_pred_proba = logistic_model.predict_proba(X_test)[:, 1]  # Probabilities for ROC-AUC


# Confusion Matrix
conf_matrix = confusion_matrix(y_test, y_pred)
print("Confusion Matrix:\n", conf_matrix)

# Classification Report
class_report = classification_report(y_test, y_pred)
print("\nClassification Report:\n", class_report)

# ROC-AUC Score
roc_auc = roc_auc_score(y_test, y_pred_proba)
print("\nROC-AUC Score:", roc_auc)






print('\n\n\n\n\n\nBinomial logistic regression tests accounting for the vote of the national judge:', end= '\n\n\n')

# Selecting relevant features for the model
# For example: 'material_ask', 'non_material_ask', 'ce_ask', and some applicant features
X = merged_df[['national_judge']]  # Add other relevant features
y = merged_df['win'].astype(int)  # Convert boolean to int

# Splitting the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


# Create and train the logistic regression model
logistic_model = LogisticRegression(max_iter=1000)  # Increase max_iter if needed
logistic_model.fit(X_train, y_train)

# Make predictions
y_pred = logistic_model.predict(X_test)
y_pred_proba = logistic_model.predict_proba(X_test)[:, 1]  # Probabilities for ROC-AUC


# Confusion Matrix
conf_matrix = confusion_matrix(y_test, y_pred)
print("Confusion Matrix:\n", conf_matrix)

# Classification Report
class_report = classification_report(y_test, y_pred)
print("\nClassification Report:\n", class_report)

# ROC-AUC Score
roc_auc = roc_auc_score(y_test, y_pred_proba)
print("\nROC-AUC Score:", roc_auc)




######################################################     LINEAR REGRESSION MODEL FOR SATISFACTION     ############################################################################

#Slight data transformation: drop the lost cases

merged_df = merged_df[merged_df['win'] == True]


# Define your features (independent variables) and target (dependent variable)

print("\n\n\n\nLinear regression model for the differentials between material damage claims and awards for sensitivity groups\n\n")


X = merged_df[[
    'female', 'natural', 'southeast_asian_nationality', 'asian_nationality', 
    'african_nationality', 'undocumented', 'religion_lack', 'religion_muslim', 
    'religion_other', 'sexuality_other', 'gender_other', 'radical_political', 
    'radical_social', 'criminal', 'felon', 'official', 'relevance'
]]
y = merged_df['material_diff']

# Splitting the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create and train the linear regression model
linear_model = LinearRegression()
linear_model.fit(X_train, y_train)

# Make predictions
y_pred = linear_model.predict(X_test)

# Calculate and print metrics
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Mean Squared Error: {mse}")
print(f"R-squared: {r2}")


print("\n\n\n\nLinear regression model for the differentials between non-material damage claims and awards for sensitivity groups\n\n")

y = merged_df['non_material_diff']

# Splitting the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create and train the linear regression model
linear_model = LinearRegression()
linear_model.fit(X_train, y_train)

# Make predictions
y_pred = linear_model.predict(X_test)

# Calculate and print metrics
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Mean Squared Error: {mse}")
print(f"R-squared: {r2}")


print("\n\n\n\nLinear regression model for the differentials between costs and expenses claims and awards for sensitivity groups\n\n")

y = merged_df['ce_diff']

# Splitting the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create and train the linear regression model
linear_model = LinearRegression()
linear_model.fit(X_train, y_train)

# Make predictions
y_pred = linear_model.predict(X_test)

# Calculate and print metrics
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Mean Squared Error: {mse}")
print(f"R-squared: {r2}")







# Define your features (independent variables) and target (dependent variable)

print("\n\n\n\nLinear regression model for the differentials between material damage claims and awards accounting only for the national judge\n\n")


X = merged_df[[
   'national_judge'
]]
y = merged_df['material_diff']

# Splitting the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create and train the linear regression model
linear_model = LinearRegression()
linear_model.fit(X_train, y_train)

# Make predictions
y_pred = linear_model.predict(X_test)

# Calculate and print metrics
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Mean Squared Error: {mse}")
print(f"R-squared: {r2}")


print("\n\n\n\nLinear regression model for the differentials between non-material damage claims and awards accounting only for the national judge\n\n")

y = merged_df['non_material_diff']

# Splitting the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create and train the linear regression model
linear_model = LinearRegression()
linear_model.fit(X_train, y_train)

# Make predictions
y_pred = linear_model.predict(X_test)

# Calculate and print metrics
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Mean Squared Error: {mse}")
print(f"R-squared: {r2}")


print("\n\n\n\nLinear regression model for the differentials between costs and expenses claims and awards accounting only for the national judge\n\n")

y = merged_df['ce_diff']

# Splitting the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create and train the linear regression model
linear_model = LinearRegression()
linear_model.fit(X_train, y_train)

# Make predictions
y_pred = linear_model.predict(X_test)

# Calculate and print metrics
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Mean Squared Error: {mse}")
print(f"R-squared: {r2}")



################## THIS SCRIPT IS EXECUTABLE - HOWEVER, IT'S STRUCTURE IN AN OBJECT-ORIENTED ENVIRONMENT MAY BE SUBJECT TO CHANGE #######################