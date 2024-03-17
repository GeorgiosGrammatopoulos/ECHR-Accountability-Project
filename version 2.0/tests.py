import pandas as pd
import string
import random as rd
import pyodbc
import utility
import judge
import caucus
import subcaucus
import odbc
import filler
from scipy.special import comb
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, classification_report, roc_auc_score
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

#Setting display options to max rows and columns

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


#First: testing the connectivity of the database before pipelining anything
def odbcTests():

    createDatabase()
    importData('Cases', application_no = '1313432')
    df = exportData('Countries', 'Judges', 'Cases', 'Reasonings', 'Applicants')
    print(df.head(49))

#Second: testing the judge simulation, if necessary (only relevant for the first part, and for white-box testing, God willing)
def judgeTests():


    for i in range(1000):

        example = Judge(startterm = '2014-03-17', endterm = '2019-03-17')
        example.judgeAppointment()

    df = odbc.exportData('Judges', 'Countries')
    print(df.head(150))


#Third: testing the caucus simulation, if necessary (again, plenty of nature forces will have to conspire to do white box testing)
def caucusTests():

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

#Dataset descriptions. Relevant for case parsing
def initStats():


    applicants= odbc.exportData('Applicants')
    judges= odbc.exportData('Judges')
    reasonings= odbc.exportData('Reasonings')
    cases = odbc.exportData('Cases')

    print(
        applicants.head(30), 
        applicants.describe(), 
        reasonings.head(30), 
        reasonings.describe(), 
        cases.head(30), 
        cases.describe(), sep= '\n\n\n')


    add = 0

    for i in range (0, 1000):

        add += reasonings['favor'].mean()

    print ('\n\n\n\n\n', add/1000, '\n\n\n\n\n\')


    for i, row in cases.iterrows():
        application_row = row['application_no']
        reasoning_row = reasonings[reasonings['application_no'] == application_row].iloc[0]

        win = reasoning_row['favor'] >= 4
        cases.at[i, 'win'] = win
           
           
           

#Insert compensation calculation execution here
           

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

#################################################### EXECUTE BRACKET ###################################################################

