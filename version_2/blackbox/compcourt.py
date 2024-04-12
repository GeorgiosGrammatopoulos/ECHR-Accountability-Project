import curvefit as cf
import odbc
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error, r2_score

def courtCurve():      #This function is an easy-to-call quick fit of the vote curve
    #These metrics were extracted on 09/04/2024 and may be revised.
    #Cases contain, on individual judgements, multiple rulings, whose voting patterns may vary.
    #From a sample of 20506 judgements:
    whole = {7: 12338, 5: 841, 3: 432, 1: 264}
    #From a sample of 15854 violation judgements:
    violations = {7: 9817, 5: 657, 3: 281, 1: 176}
    #From a sample of 3727 non-violation judgements:
    nonviolations = {7: 2646, 5: 347, 3: 205, 1: 134}

    fits = {'whole dataset': whole, "violations dataset": violations, "non-violations dataset": nonviolations}

    for key, value in fits.items():
        print(f'Test output for the {key}:\n')

        a_fit, b_fit, predicted, covariance = cf.exponentRun(value)
        
        # Here, you would interpret the covariance matrix, especially focusing on
        # the relationship between a and b, and how confident you are in their estimates.
        

courtCurve()

#Ktistakis track (129 cases):
#15+8+10 = 33 non-unanimous, 10 times not with the majority
#Ktistakis not voting with the majority:
#CASE OF BAKIRDZI AND E.C. v. HUNGARY - Protection of minorities - 6/1
#CASE OF WOJCZUK v. POLAND - Protection of the freedom of expression - 5/2
#CASE OF SEMENYA v. SWITZERLAND - Judgement that would effectively extend the court's jurisdiction - 4/3
#CASE OF JUSZCZYSZYN v. POLAND - In favor of acknowledging the loss of income - 4/3
#CASE OF BUDIMIR v. CROATIA - Admissibility - 4/3
#CASE OF SHIPS WASTE OIL COLLECTOR B.V. v. THE NETHERLANDS - Protection of corporate information - 4/3
#CASE OF JANSSEN DE JONG GROEP B.V. AND OTHERS v. THE NETHERLANDS - '' - 4/3
#CASE OF BURANDO HOLDING B.V. AND PORT INVEST v. THE NETHERLANDS - '' - 4/3
#CASE OF MALAGIĆ v. CROATIA - Women's rights - 4/3
#CASE OF ALTIUS INSURANCE LTD v. CYPRUS - Pecuniary damages - 4/3

#Maybe
#CASE OF PODCHASOV v. RUSSIA - 5/2
#CASE OF BRYAN AND OTHERS v. RUSSIA - 5/2

