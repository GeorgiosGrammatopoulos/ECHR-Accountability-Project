import odbc
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import curvefit as cf
from sklearn.metrics import mean_squared_error, r2_score

def initStats():


    applicants= odbc.exportData('Applicants')
    reasonings= odbc.exportData('Reasonings')
    cases = odbc.exportData('Cases')


    #Insert compensation calculation execution here
           
    winners = reasonings[reasonings['favor'] > reasonings['against']]
    losers = reasonings[reasonings['favor'] < reasonings['against']]
    reasonings['votediffs'] = abs(reasonings['favor'] - reasonings['against'])
    askmat= winners[winners['material_ask'] > 0].count()
    asknon= winners[winners['non_material_ask'] > 0].count()
    print(f'Average material satisfaction awarded per case: \n{winners["material_award"].sum()/askmat}\n\n\n')
    print(f'Average non material satisfaction awarded per case: \n {winners["non_material_award"].sum()/asknon}\n\n\n')
    print(applicants.describe())
    print(cases.describe())
    print(reasonings.describe())
    reasons = reasonings['favor'].value_counts()
    reasons = reasons.sort_index()
    reasons.plot.bar(color='purple')
    plt.xlabel('Number of Favor Votes')
    plt.ylabel('Frequency')
    plt.title('Distribution of Favor Votes in a Seven-Member Caucus')
    plt.show()


    print(reasonings['votediffs'].value_counts())
    print(winners['favor'].value_counts())
    print(losers['against'].value_counts())

    wholed = reasonings['votediffs'].value_counts().todict
    wind = winners['favor'].value_counts().to_dict()
    losed = losers['against'].value_counts().to_dict()


    print(f'\n\n\nTest output for synthetic data (random):\n')
    testdict = reasonings['votediffs'].value_counts().to_dict()
    a_fit, b_fit, predicted, covariance = cf.exponentRun(testdict)

    # Extract actual and predicted values