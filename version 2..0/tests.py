###Relational dataframes to populate

#Python packages that will be needed
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



class Tests:

    # Set option to display all columns (None means unlimited)
    pd.set_option('display.max_columns', None)

    # Optionally, you can also adjust the number of rows to display
    pd.set_option('display.max_rows', None)

    #establish a connection with the database





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

#################################################### UTILITY ###################################################################

    @staticmethod
    def mainTests():