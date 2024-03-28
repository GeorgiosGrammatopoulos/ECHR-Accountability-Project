import pandas as pd
import random as rd
import odbc
from scipy import stats
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, classification_report, roc_auc_score
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

#Setting display options to max rows and columns

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


def initStats():


    applicants= odbc.exportData('Applicants')
    reasonings= odbc.exportData('Reasonings')
    cases = odbc.exportData('Cases')


    #Insert compensation calculation execution here
           
    winners = reasonings[reasonings['favor'] > reasonings['against']]
    askmat= winners[winners['material_ask'] > 0].count()
    asknon= winners[winners['non_material_ask'] > 0].count()
    print(f'Average material satisfaction awarded per case: \n{winners["material_award"].sum()/askmat}\n\n\n')
    print(f'Average non material satisfaction awarded per case: \n {winners["non_material_award"].sum()/asknon}\n\n\n')
    print('Voting patterns:\n\n\n', reasonings['favor'].value_counts(), end = '\n\n\n')
    print(reasonings['against'].value_counts(), end = '\n\n\n')
    print(applicants.describe())
    print(cases.describe())
    print(reasonings.describe())


    
def cleanerStats():

    reasonings= odbc.exportData('Reasonings')
    reasonings['recount'] = reasonings['favor'] + reasonings['against']
    corrupt = reasonings[reasonings['recount'] != 7]
    print(corrupt.head(200))
    print(corrupt.describe())





    #########################################################     LOGISTIC REGRESSION MODEL FOR WIN RATIO     ############################################################################

    def differntialRatio():
    
        # Assuming 'instance' and 'applicant' dataframes are ready
        # Merging instance data with applicant data on first and last names
        merged_df = pd.merge(reasonings, applicants, on=['firstname', 'lastname'])
        merged_df = pd.merge(merged_df, cases, on=['application_no'])


        print('Binomial logistic regression tests accounting for sensitivity to bias:', end= '\n\n\n')

        # Selecting relevant features for the model
        # For example: 'material_ask', 'non_material_ask', 'ce_ask', and some applicant features
        X = merged_df[[
            'female', 'natural', 'southeast_asian_nationality', 'asian_nationality', 
            'african_nationality', 'undocumented', 'religion_lack', 'religion_muslim', 
            'religion_other', 'sexuality_other', 'gender_other', 'radical_political', 
            'radical_social', 'criminal', 'felon', 'official', 'relevance'
        ]]  # Add other relevant features
        y = merged_df['favor'].astype(int)  # Convert boolean to int

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
        y = merged_df['favor'].astype(int)  # Convert boolean to int

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

    def winLossRatio():

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

initStats()