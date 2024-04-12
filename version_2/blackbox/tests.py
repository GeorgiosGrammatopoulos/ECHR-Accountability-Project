import pandas as pd
import odbc
import compcourt as cp
import utility as ut
import seaborn as sns
import matplotlib.pyplot as plt
import initstats as init
from scipy.optimize import curve_fit
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report, roc_auc_score, accuracy_score, mean_squared_error, mean_absolute_error, r2_score 
from sklearn.metrics import ConfusionMatrixDisplay
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier # For classification
from sklearn.ensemble import RandomForestRegressor # For regression  s5ss


#Plan:
#Establish weights by running primary regression models
#Build random forests based on the outcomes of the regression models
#Verify with building linear and logistic regressions correlating judges with individual variables, and using the score bands as predictors


#Setting display options to max rows and columns

plt.figure(figsize=(8, 6))
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

    

init.initStats()
cp.courtCurve()




#############################################################     DRAFTS    ################################################################################################################


#############################################################     TESTING THE IMPACT OF LAW AND FACT          ###########################################################################

#Assessing the impact of law and fact on the decisions
def lawFactTest():

    print('Testing the impact of law and fact on the decision-making process')

    #First, establish the relevant datasets, when they may be legally controversial
    reasonings = odbc.exportData('Reasonings')
    applicants = odbc.exportData('Applicants')
    cases = odbc.exportData('Cases')
    merged = pd.merge(reasonings, applicants, on = ['application_no'])
    merged = pd.merge(merged, cases, on=['application_no'])
    merged['result'] = False
    for index, row in merged.iterrows():
        if row['favor'] > 3:
            merged.at[index, 'result'] = True
    merged['dissent_val'] = 0
    for index, row in merged.iterrows():
        if type(row['dissent']) == str:
            merged.at[index, 'dissent_val'] = 1
    applicant_set = merged[merged['result']]
    respondent_set = merged[~merged['result']]
    applicant_lawset = applicant_set[applicant_set['favor'] > 4]        #turn into highly controversial
    respondent_lawset = respondent_set[respondent_set['favor'] < 3]
    sets = {'full': merged,
            'favoring applicant': applicant_set, 
            'favoring respondent': respondent_set,
            'circumstances favoring applicant': applicant_lawset, 
            'circumstances favoring respondent': respondent_lawset}
    

    try:
        for k, i in sets.items():
        #then, run the tests:
            ut.exportHTML('Law_fact report.html', 'Text', f'Analysis for the dataset "{k}"')
            visuals(i,'favor', 'non_material_award', 'non_material_diff')
            test1(i, 'favor', 'contest_law', 'contest_fact', 'contest_lawres', 'contest_factres')
            test2(i, 'non_material_diff', 'contest_law', 'contest_fact', 'contest_lawres', 'contest_factres')
            test3(i, 'favor', 'contest_law', 'contest_lawres')
            test4(i, 'non_material_diff', 'contest_law', 'contest_lawres')
            test5(i, 'favor', 'contest_fact', 'contest_factres')
            test6(i, 'non_material_diff', 'contest_fact')
            tests7(i, 'dissent_val', 'contest_law')
            tests7(i, 'dissent_val', 'contest_factres')
            tests7(i, 'dissent_val', 'contest_lawres')
    except Exception as e:
        print(f"{e}\nReport failed, check individual failures")



def visuals(data, relation, *args):

    try:

        #then, visualize:
        ut.exportHTML('Law_fact report.html', 'Text', f'Visualization of the dataset voting pattern, using{args}')
        colors = ['red', 'green', 'blue', 'purple', 'orange']
        for i in range(len(args)):
            sns.scatterplot(x = relation, y = args[i], data = data, color=colors[i])
        plt.title('Distribution of material awards in relation with their controversy')
        plt.legend()
        fig = plt.gcf()
        ut.integratePlot('Law_fact report.html', fig)

    except Exception as e:
        print(f"{e}\nVisualization failed")

    #Test 1: check how much controversy in general matters
    #Test 1.1: Logistic regression on win/loss
    #Expected result: significant impact, not dominant

def test1(frame1, target, *args):
    try:
        ut.exportHTML('Law_fact report.html', 'Text', f'Poisson regression model demontrating how voting patterns are impacted by contests in law and fact, using{args}')
        columns = list(args)
        a = frame1[columns]  # Features
        b = frame1[target]  # Target variable
        a_train, a_test, b_train, b_test = train_test_split(a, b, test_size=0.2, random_state=42)
        model1 = LogisticRegression()
        model1.fit(a_train, b_train)
        predictions = model1.predict(a_test)
        accuracy = accuracy_score(b_test, predictions)
        cm = confusion_matrix(b_test, predictions, labels=model1.classes_)
        disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=model1.classes_)
        fig, ax = plt.subplots()
        summary = ut.beautifySummary(b, a)
        ut.exportHTML('Law_fact report.html', 'Text', summary)
        ut.exportHTML('Law_fact report.html', 'Text', f'Accuracy: {accuracy}')
        disp.plot(ax=ax)
        ax.set_title('Confusion Matrix')
        plt.tight_layout()
        ut.integratePlot('Law_fact report.html', fig)
    except Exception as e:
        print(f"{e}\nModel 1 failed")


    #Test 1.2: Linear regression on amount
    #Expected result: significant impact, dominant
def test2(frame2, target, *args):
    try:
        ut.exportHTML('Law_fact report.html', 'Text', f'Linear regression on compensation data to assess significance of law and fact, using {args}')
        args= list(args)
        frame2 = frame2[(frame2['non_material_diff'] != 0) | (frame2['non_material_award'] == 0)]
        c = frame2[args]
        d = frame2[target]
        c_train, c_test, d_train, d_test = train_test_split(c, d, test_size=0.2, random_state=42)
        model2 = LinearRegression()
        model2.fit(c_train, d_train)
        predictions = model2.predict(c_test)
        mae = mean_absolute_error(d_test, predictions)
        mse = mean_squared_error(d_test, predictions)
        r2 = r2_score(d_test, predictions)
        ut.exportHTML('Law_fact report.html', 'Text', f'Mean Absolute Error (MAE): {mae}')
        ut.exportHTML('Law_fact report.html', 'Text', f'Mean Squared Error (MSE): {mse}')
        ut.exportHTML('Law_fact report.html', 'Text', f'R-squared (R²): {r2}')
    except Exception as e:
        print(f"{e}\nModel 2 failed")


    #Test 1.3: Logistic regression on win/loss
    #Expected result: significant impact, not dominant
def test3(frame3, target, *args):
    try:
        ut.exportHTML('Law_fact report.html', 'Text', f'Poisson regression model demontrating how voting patterns are impacted by contests in law{args}')
        args = list(args)
        e = frame3[args]  # Features
        f = frame3[target]  # Target variable
        e_train, e_test, f_train, f_test = train_test_split(e, f, test_size=0.2, random_state=42)
        model3 = LogisticRegression()
        model3.fit(e_train, f_train)
        predictions = model3.predict(e_test)
        accuracy = accuracy_score(f_test, predictions)
        cm = confusion_matrix(f_test, predictions, labels=model3.classes_)
        disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=model3.classes_)
        fig, ax = plt.subplots()
        summary = ut.beautifySummary(poisson_model)
        ut.exportHTML('Law_fact report.html', 'Text', summary)
        ut.exportHTML('Law_fact report.html', 'Text', f'Accuracy: {accuracy}')
        disp.plot(ax=ax)
        ax.set_title('Confusion Matrix')
        plt.tight_layout()
        ut.integratePlot('Law_fact report.html', fig)
    except Exception as e:
        print(f"{e}\nModel 3 failed")

    #Test 1.4: Linear regression on amount
    #Expected result: significant impact, dominant
def test4(frame4, target, *args):
    try:
        ut.exportHTML('Law_fact report.html', 'Text', f'Linear regression on compensation data to assess significance of law, using {args}')
        args = list(args)
        frame4 = frame4[(frame4['non_material_diff'] != 0) | (frame4['non_material_award'] == 0)]
        g = frame4[args]  # Predictor variables
        h = frame4[target]  # Target variable (the amount of compensation)
        g_train, g_test, h_train, h_test = train_test_split(g, h, test_size=0.2, random_state=42)
        model4 = LinearRegression()
        model4.fit(g_train, h_train)
        predictions = model4.predict(g_test)
        mae = mean_absolute_error(h_test, predictions)
        mse = mean_squared_error(h_test, predictions)
        r2 = r2_score(h_test, predictions)
        ut.exportHTML('Law_fact report.html', 'Text', f'Mean Absolute Error (MAE): {mae}')
        ut.exportHTML('Law_fact report.html', 'Text', f'Mean Squared Error (MSE): {mse}')
        ut.exportHTML('Law_fact report.html', 'Text', f'R-squared (R²): {r2}')
    except Exception as e:
        print(f"{e}\nModel 4 failed")

    #Test 1.5: Logistic regression on win/loss
    #Expected result: significant impact, not dominant
def test5(frame5, target, *args):
    try:
        ut.exportHTML('Law_fact report.html', 'Text', f'Confusion matrices demontrating how voting patterns are impacted by contests in fact, using {args}')
        args = list(args)
        j = frame5[args]  # Features
        k = frame5[target]  # Target variable
        poisson_model = sm.GLM(k, j, family=sm.families.Poisson()).fit()
        j_train, j_test, k_train, k_test = train_test_split(j, k, test_size=0.2, random_state=42)
        model5 = LogisticRegression()
        model5.fit(j_train, k_train)
        predictions = model5.predict(j_test)
        accuracy = accuracy_score(k_test, predictions)
        cm = confusion_matrix(k_test, predictions, labels=model5.classes_)
        disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=model5.classes_)
        fig, ax = plt.subplots()
        disp.plot(ax=ax)
        summary = ut.beautifySummary(poisson_model)
        ut.exportHTML('Law_fact report.html', 'Text', summary)
        ut.exportHTML('Law_fact report.html', 'Text', f'Accuracy: {accuracy}')
        disp.plot(ax=ax)
        ax.set_title('Confusion Matrix')
        plt.tight_layout()
        ut.integratePlot('Law_fact report.html', fig)
    except Exception as e:
        print(f"{e}\nModel 5 failed")


    #Test 1.6: Linear regression on amount
    #Expected result: significant impact, dominant
def test6(frame6, target, *args):
    try:
        ut.exportHTML('Law_fact report.html', 'Text', f'Linear regression on compensation data to assess significance of fact, using {args}')
        args = list(args)
        frame6 = frame6[(frame6['non_material_diff'] != 0) | (frame6['non_material_award'] == 0)]
        l = frame6[args]  # Predictor variables
        m = frame6[target]  # Target variable (the amount of compensation)
        l_train, l_test, m_train, m_test = train_test_split(l, m, test_size=0.2, random_state=42)
        model6 = LinearRegression()
        model6.fit(l_train, m_train)
        predictions = model6.predict(l_test)
        mae = mean_absolute_error(m_test, predictions)
        mse = mean_squared_error(m_test, predictions)
        r2 = r2_score(m_test, predictions)
        ut.exportHTML('Law_fact report.html', 'Text', f'Mean Absolute Error (MAE): {mae}')
        ut.exportHTML('Law_fact report.html', 'Text', f'Mean Squared Error (MSE): {mse}')
        ut.exportHTML('Law_fact report.html', 'Text', f'R-squared (R²): {r2}')
        ut.exportHTML('Law_fact report.html', 'Text', '\n\n\n\n\n\n')
    except Exception as e:
        print(f"{e}\nModel 6 failed")


def tests7(frame7, target, *args):
    ut.exportHTML('Law_fact report.html', 'Text', f'Logistic regression denoting the relatinship between dissenting and separate and vote tally, using {args}')
    try:
        args = list(args)
        for arg in args:
            for index, row in frame7.iterrows():
                if row[arg] == True:
                    frame7.at[index, arg] = 1
                else:
                    frame7.at[index, arg] = 0
        X = frame7[args]
        y = frame7[target]
        model = LogisticRegression(solver='liblinear', random_state=42)  # Using liblinear solver for binary classification
        model.fit(X, y)
        frame7['predicted_probability'] = model.predict_proba(X)[:, 1]  # Get the probability of class 1
        frame7['predicted_outcome'] = model.predict(X)
        ut.exportHTML('Law_fact report.html', 'Text', "Classification Report:")
        report = classification_report(y, frame7['predicted_outcome'], output_dict=True)
        report_str = ""
        for label, metrics in report.items():
            report_str += f'{label.title()}\n'
            # Check if metrics is a dictionary
            if isinstance(metrics, dict):
                for key, value in metrics.items():
                    report_str += f'    {key.title()}: {value:.2f}\n'  # Formatting value as float
            else:  # If metrics is not a dictionary, it's the overall accuracy
                report_str += f'    Accuracy: {metrics:.2f}\n'  # Assuming metrics is the accuracy float value here
        ut.exportHTML('Law_fact report.html', 'Text', report_str)
        ut.exportHTML('Law_fact report.html', 'Text',"Confusion Matrix:")
        cm = confusion_matrix(y, frame7['predicted_outcome'])
        cm_str = "Confusion Matrix:\n"
        labels = ['True Negative', 'False Positive', 'False Negative', 'True Positive']
        values = cm.flatten()
        for label, value in zip(labels, values):
            cm_str += f"{label}: {value}\n"
        ut.exportHTML('Law_fact report.html', 'Text', cm_str)
        if 'column_name' in frame7:
            frame7['column_name'] = pd.to_numeric(frame7['column_name'], errors='coerce').fillna(0)
            avg = sum(frame7['column_name'].tolist()) / len(frame7['column_name'].tolist())
            ut.exportHTML('Law_fact report.html', 'Text', f'Logistic regression predictive capability: {avg * 100}%')
    except Exception as e:
        ut.exportHTML('Law_fact report.html', 'Text',f"{e}\nModel 7 failed")




#############################################################     TESTING THE IMPACT OF PRIORITIES            ###########################################################################

def priorityTest():

    #Weight of items in the simulation:
    #firstname : 19
    #lastname: 18
    #female: 17
    #natural: 16
    #southeast_asian_nationality: 15
    #asian_nationality: 14
    #african_nationality: 13
    #undocumented: 12
    #religion_lack: 11
    #religion_muslim: 10
    #religion_other: 9
    #sexuality_other: 8
    #gender_other: 7
    #radical_political: 6 
    #radical_social: 5
    #criminal: 4
    #felon: 3
    #official: 2
    #relevance: 1
    
    #First, establish the relevant datasets. Also, build a column which will add truth values to establish a controversy score
    reasonings = odbc.exportData('Reasonings')
    applicants = odbc.exportData('Applicants')
    print(applicants.head())
    cases = odbc.exportData('Cases')
    merged = pd.merge(reasonings, applicants, on = ['application_no'])
    merged = pd.merge(merged, cases, on=['application_no'])
    collist = applicants.columns.tolist()
    collist = collist[4:]
    print(collist)
    merged['controversy_score']= 0
    for col in collist:
        merged['controversy_score'] += merged[f'{col}'].astype(int)
    winner_set = merged[merged['favor'] > 3]
    non_cont_set = merged[~(merged['contest_law'] | merged['contest_fact'])]
    iteration = 0
    sets = [merged, winner_set, non_cont_set]

    for i in sets:
        
        iteration += 1
        print(f'Analysis for the dataset No. {iteration}\n\n\n')

    #then, visualize:

        sns.scatterplot(x = 'controversy_score', y ='non_material_ask', data = i, color='red')
        plt.title('Distribution of material asks in relation with their controversy')
        plt.legend()
        plt.show()
        sns.scatterplot(x = 'controversy_score', y ='non_material_award', data = i, color='green')
        plt.title('Distribution of material awards in relation with their controversy')
        plt.legend()
        plt.show()


        #Test 1: check how much controversy in general matters
        #Test 1.1: Logistic regression on win/loss
        #Expected result: significant impact, not dominant
        if i.shape[0] != winner_set.shape[0]:
            print('Logistic regression on win/loss data to assess whether controversy is significant')
            i['result'] = i['favor'] > 3
            X = i[['controversy_score']]  # Features
            y = i['result']  # Target variable
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            model1 = LogisticRegression()
            model1.fit(X_train, y_train)
            predictions = model1.predict(X_test)
            accuracy = accuracy_score(y_test, predictions)
            print(f'Accuracy: {accuracy}')
            probabilities = model1.predict_proba(X_test)[:, 1]  # Probabilities of the positive class
            auc_roc = roc_auc_score(y_test, probabilities)
            print(f'AUC-ROC: {auc_roc}')
            print('\n\n\n\n\n\n')

        #Test 1.2: Linear regression on amount
        #Expected result: significant impact, dominant

        print('Linear regression on compensation data to assess whether controversy is significant')
        X = i[['controversy_score']]  # Predictor variables
        y = i['non_material_diff']  # Target variable (the amount of compensation)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        model2 = LinearRegression()
        model2.fit(X_train, y_train)
        predictions = model2.predict(X_test)
        mae = mean_absolute_error(y_test, predictions)
        mse = mean_squared_error(y_test, predictions)
        r2 = r2_score(y_test, predictions)
        print(f'Mean Absolute Error (MAE): {mae}')
        print(f'Mean Squared Error (MSE): {mse}')
        print(f'R-squared (R²): {r2}')


        #Test 1: treat unrelated variables as one single one, and check individual columns - PCA/LDA
        


        #Test 2: t-SnA for win/loss with individual columns



        #Test 3: UMAP for win/loss with individual columns




#########################################################     LOGISTIC REGRESSION MODEL FOR WIN RATIO     ############################################################################

def differntialRatio():
    
    # Assuming 'instance' and 'applicant' dataframes are ready
    # Merging instance data with applicant data on first and last names
    reasonings = odbc.exportData('Reasonings')
    print(reasonings.columns.tolist())
    applicants = odbc.exportData('Applicants')
    print(applicants.columns.tolist())
    cases = odbc.exportData('Cases')
    print(cases.columns.tolist())
    merged = pd.merge(reasonings, cases, on=['application_no'])
    merged = pd.merge(merged, applicants, on = ['application_no'])



    print('Binomial logistic regression tests accounting for sensitivity to bias:', end= '\n\n\n')

    # Selecting relevant features for the model
    # For example: 'material_ask', 'non_material_ask', 'ce_ask', and some applicant features
    X = merged[[
        'female', 'natural', 'southeast_asian_nationality', 'asian_nationality', 
        'african_nationality', 'undocumented', 'religion_lack', 'religion_muslim', 
        'religion_other', 'sexuality_other', 'gender_other', 'radical_political', 
        'radical_social', 'criminal', 'felon', 'official', 'relevance'
    ]]  # Add other relevant features
    y = merged['favor'].astype(int)  # Convert boolean to int

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
    X = merged[['national_judge']]  # Add other relevant features
    y = merged['favor'].astype(int)  # Convert boolean to int

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

    reasonings = odbc.exportData('Reasonings')
    applicants = odbc.exportData('Applicants')
    merged = pd.merge(reasonings, applicants, on = ['firstname', 'lastname'])


    # Define your features (independent variables) and target (dependent variable)

    print("\n\n\n\nLinear regression model for the differentials between material damage claims and awards for sensitivity groups\n\n")


    X = merged[[
        'female', 'natural', 'southeast_asian_nationality', 'asian_nationality', 
        'african_nationality', 'undocumented', 'religion_lack', 'religion_muslim', 
        'religion_other', 'sexuality_other', 'gender_other', 'radical_political', 
        'radical_social', 'criminal', 'felon', 'official', 'relevance'
    ]]
    y = merged['material_diff']

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

    y = merged['non_material_diff']

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

    y = merged['ce_diff']

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


    X = merged[[
    'national_judge'
    ]]
    y = merged['material_diff']

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

    y = merged['non_material_diff']

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

    y = merged['ce_diff']

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

#############################################################     RANDOM FOREST                               ###########################################################################


#Classification of variables
def forest():

    print('Testing the impact of law and fact on the decision-making process')

    #First, establish the relevant datasets, when they may be legally controversial
    reasonings = odbc.exportData('Reasonings')
    applicants = odbc.exportData('Applicants')
    cases = odbc.exportData('Cases')
    merged = pd.merge(reasonings, applicants, on = ['application_no'])
    merged = pd.merge(merged, cases, on=['application_no'])
    winner_set = merged[merged['favor'] > 3]
    applicant_set = merged[merged['contest_lawres'] | merged['contest_factres']]
    respondent_set = merged[~(merged['contest_lawres'] | merged['contest_factres'])]
    applicant_lawset = merged[merged['contest_lawres']]
    respondent_lawset = merged[~merged['contest_lawres']]
    applicant_factset = merged[merged['contest_factres']]
    respondent_factset = merged[~merged['contest_factres']]
    sets = {'full': merged,
            'favoring applicant': applicant_set, 
            #'favoring respondent': respondent_set, 
            #'law favoring applicant': applicant_lawset, 
            'law favoring respondent': respondent_lawset, 
            #'facts favoring applicant': applicant_factset, 
            'facts favoring respondent': respondent_factset}

    for k, i in sets.items():

        listing = applicants.columns.tolist()
        listing = listing[4:]

        X = i[['contest_law', 'contest_fact', 'contest_lawres', 'contest_factres']]
        y = i['favor']  # Target variable

        # Split dataset into training set and test set
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)  # 80% training, 20% test
        # Create a Gaussian Classifier
        clf = RandomForestClassifier(n_estimators=100)  # n_estimators is the number of trees

# Train the model using the training sets
        clf.fit(X_train, y_train)

# Predict the response for the test dataset
        y_pred = clf.predict(X_test)

        # Create a regressor
        reg = RandomForestRegressor(n_estimators=100)  # n_estimators is the number of trees

    # Train the model using the training sets
        reg.fit(X_train, y_train)

    # Predict the response for the test dataset
        y_pred = reg.predict(X_test)

        # Model Accuracy, how often is the classifier correct?
        print("Accuracy:", accuracy_score(y_test, y_pred))

        # Calculate the Mean Squared Error
        print("Mean Squared Error:", mean_squared_error(y_test, y_pred))

        feature_imp = pd.Series(clf.feature_importances_, index=X.columns).sort_values(ascending=False)
        print(feature_imp)


########################################################################################################################################
        
def heteroedasticity(np):

    # set the seed
    np.random.seed(561)

    # generate a single feature randomly
    X0 = np.random.rand(100)

    # actual interception and slope of linear regression
    intercept = 2
    slope = 5

    # generate random observation noise (error)
    # noise variance is a function of the feature (heteroscedastic noise)
    noise = 3*np.abs(X0)*np.random.randn(X0.shape[0])

    # generate the response variable
    y = slope*X0 + intercept + noise

    # generate the augmented feature matrix (bias + feature)
    X = np.c_[np.ones(X0.shape[0]),X0]

    # solution of linear regression
    w_lr = np.linalg.inv(X.T @ X) @ X.T @ y

    # calculate residuals
    res = y - X @ w_lr

    # estimate the covariance matrix
    C = np.diag(res**2)

    # solution of weighted linear regression
    w_wlr = np.linalg.inv(X.T @ np.linalg.inv(C) @ X) @ (X.T @ np.linalg.inv(C) @ y)

    # generate the feature set for plotting
    X_p = np.c_[np.ones(2), np.linspace(X0.min(), X0.max(), 2)]

    # plot the results
    plt.plot(X0, y, 'b.', label='Observations')
    plt.plot(X_p[:,1], X_p @ w_lr, 'r-', label='Linear Regression')
    plt.plot(X_p[:,1], X_p @ w_wlr, 'g-', label='Weighted Linear Regression')
    plt.plot(X_p[:,1], X_p @ [intercept, slope], 'm--', label='Actual Regression')
    plt.grid(linestyle=':')
    plt.ylabel('Response')
    plt.xlabel('Feature')
    plt.legend()