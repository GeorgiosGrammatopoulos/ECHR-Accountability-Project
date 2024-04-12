import datetime
import random
import string
import base64
import io
import sys
import os
import pandas as pd
import seaborn as sns
from io import BytesIO
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import statsmodels.api as sm





def random_name(length=6): #Name randomizer for simulations
    
    return ''.join(random.choice(string.ascii_letters) for _ in range(length))
    
    

def dateInput(commstring, preset = None): #date input function which enables proper checks
    
    while True:
        if preset == None:
            date = input(f'{commstring}')
        else:
            date = preset
            
        chars = list(date)
        
        try:
            year = int(date[0:4])
        except:
            pass
            
        try:
            month = int(date[5:7])
        except:
            pass
        try:
            day = int(date[8:])
        except:
            pass
        
        if len(date) != 10:
            
            print ('Invalid date! Please try again')
            preset = None
            continue
            
        elif (chars[4] != '-') or (chars[7] != '-'):
            
            print ('Invalid date! Please try again')
            preset = None
            continue
            
        elif year not in range(1954, datetime.now().year+1):
            
            print ('Invalid year! Please try again!')
            preset = None
            continue
            
        elif month not in range (1, 13):
            
            print ('Invalid month! Please try again!')
            preset = None
            continue
        
        elif day not in range (1, 32):
            
            print ('Invalid day! Please try again!')
            preset = None
            continue
            
        elif (day in range (30, 32)) and month == 2:
            
            print ('Invalid date! Please try again!')
            preset = None
            continue
        
        else:
            
            break
            
    return date



#randomizer for dates, for the purposes of simulation
def randomDate():
    start_date = datetime.date(1954, 1, 1)
    
    end_date = datetime.date.today()

    delta = end_date - start_date

    random_days = random.randint(0, delta.days)

    random_date = start_date + datetime.timedelta(days=random_days)

    return random_date



def firstLetter(inputstring):
    if not inputstring:  # Check if the string is empty
        return inputstring
    return inputstring[0].lower() + inputstring[1:]



def exportHTML(file_path, element_tag, content):
    content_type = firstLetter(element_tag)
    # Construct HTML content with line breaks after each text statement
    html_content = f'<{element_tag} type="{content_type}">{content}<br></{element_tag}>\n'
    # Check if the file exists
    if os.path.exists(file_path):
        # Read the existing HTML content
        with open(file_path, 'r') as f:
            existing_content = f.read()
        # Append the new HTML content
        new_content = existing_content + html_content
        # Prettify the HTML content
        soup = BeautifulSoup(new_content, 'html.parser')
        prettified_html = soup.prettify()
        # Write the prettified HTML content back to the file
        with open(file_path, 'w') as f:
            f.write(prettified_html)
    else:
        # Write the new HTML content to the file
        with open(file_path, 'w') as f:
            f.write(f'<Content>\n')
            f.write(f'{html_content}')
            f.write(f'</Content>\n')
 
           

import os
import matplotlib.pyplot as plt

def integratePlot(filepath, fig):
    # Determine the base filename without extension
    base_filename = os.path.splitext(filepath)[0]
    # Find the highest version number
    version_numbers = []
    stringnos = list(str(i) for i in range(30))
    stringdict = {}
    for i in range(0, len(stringnos)):
        stringdict[stringnos[i]] = i
    for filename in os.listdir():
        if filename.startswith(base_filename) and filename.endswith('.png'):
            version_num = filename[len(base_filename) + 1:-4]
            if version_num in stringnos:
                version_numbers.append(stringdict[version_num])
    if version_numbers:
        next_version = max(version_numbers) + 1
    else:
        next_version = 1
    # Construct the new plot image filename
    plot_image_path = f"{base_filename}_{next_version}.png"
    # Save the plot image with the new filename
    fig.savefig(plot_image_path, format='png')
    # Close the figure to free memory
    plt.close(fig)
    # Generate HTML with image tag referencing the saved image and a line break
    html_content = f'<img src="{plot_image_path}" alt="Plot"><br>\n'
    # Export the HTML content to the specified file
    with open(filepath, 'a') as f:
        f.write(html_content)


def beautifySummary(target, arguments):       # to amend after weight testing

    poisson_model = sm.GLM(target, arguments, family=sm.families.Poisson()).fit()
    return poisson_model.suumary()



def visuals(data, relation, *args):

    try:

        #then, visualize:
        exportHTML('Law_fact report.html', 'Text', f'Visualization of the dataset voting pattern, using{args}')
        colors = ['red', 'green', 'blue', 'purple', 'orange']
        for i in range(len(args)):
            sns.scatterplot(x = relation, y = args[i], data = data, color=colors[i])
        plt.title('Distribution of material awards in relation with their controversy')
        plt.legend()
        fig = plt.gcf()
        integratePlot('Law_fact report.html', fig)

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


    import pandas as pd

def vc_dataframe(function):
    """
    Creates a DataFrame from a list of value_counts objects.
    
    Parameters:
    - value_counts_list: list of pd.Series, each Series is a value_counts from a trial.
    
    Returns:
    - pd.DataFrame with trials as rows, categories as columns, and counts as values.
    """

    # Combine all unique indexes (categories) from the value_counts objects
    all_categories = set().union(*(vc.index for vc in value_counts_list))
    
    # Initialize a DataFrame with all categories as columns
    df = pd.DataFrame(columns=all_categories)
    
    # Fill in the DataFrame with counts for each trial
    for i, vc in enumerate(value_counts_list):
        # For each value_counts, set the trial row by reindexing with all_categories
        # Fill missing categories with 0
        df.loc[i] = vc.reindex(all_categories, fill_value=0)
    
    return df

# Example usage:
# Assuming you have a list of pd.Series objects that are the result of value_counts()
# value_counts_list = [series1.value_counts(), series2.value_counts(), ...]
# dataframe = create_dataframe_from_value_counts(value_counts_list)
