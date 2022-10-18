
'''
Encoding: UTF-8
Title: asthma-calc-x-web.py
Created: 2022-10-17 02:24:01
@author: samantix
'''

# + Description: This program classifies asthma severity per 2020 GINA criteria

# ----------------------------------------------------------

# * Import libraries

import pandas as pd
from PIL import Image
import streamlit as st

# ----------------------------------------------------------

# * Set streamlit configuration

st.set_page_config(
    page_title=None,
    page_icon=None,
    layout="wide",
    initial_sidebar_state="auto"
)

# ----------------------------------------------------------

# * Create title & sub-title

st.write("""
# Asthma Calc-X
## Classifies asthma severity per 2020 GINA criteria
""")

# ----------------------------------------------------------

# * Open image

image = Image.open(
    "/Users/samantix/iam/_developing_/samantix/apps/Archive/Science/Applied/Medicine/Diagnostics/rithm-x/web_app/asthma-x/res/DiabetesRiskCalc.png")

# * Display image

st.image(image, caption='SamantiX', use_column_width=True)


# ----------------------------------------------------------


def get_user_data():
    '''
    I: int and boolean values via web interface
    O: list of nested dictionaries populated w/ user input to prompts
    '''

    # * control_factors v4 (type-casting keyword changed to string 2/2 problematic O/P)

    control_factors = {
        'A15': ['Alternative Dx have been excluded', "st.sidebar.radio(v[0],[True,False],index=1,horizontal=True)"],
        'A4': ['Currently symptomatic', "st.sidebar.radio(v[0],[True,False],index=1,horizontal=True)"],
        'A5': ['Daytime asthma Sx per week', "st.sidebar.number_input(v[0],0,7)"],
        'A6': ['Rescue inhaler uses per week', "st.sidebar.number_input(v[0],0,7)"],
        'A7': ['Asthmatic-awakening >0 per month', "st.sidebar.radio(v[0],[True,False],index=1,horizontal=True)"],
        'A8': ['Asthma-limited physical activity', "st.sidebar.radio(v[0],[True,False],index=1,horizontal=True)"],

        # @ not 2020 GINA criteria
        # 'A10': ['asthma triggers', "st.sidebar.radio(v[0],[True,False],index=1,horizontal=True)"],
        # 'A11': ['atopy (personal or FMH)', "st.sidebar.radio(v[0],[True,False],index=1,horizontal=True)"],
        # 'A12': ['characteristic musical wheezing on PE', "st.sidebar.radio(v[0],[True,False],index=1,horizontal=True)"],
    }

    # * exacerbation_risk_factors v2

    exacerbation_risk_factors = {
        "A17": ["Current tobacco smoke exposure", "st.sidebar.radio(v[0],[True,False],index=1,horizontal=True)"],
        "A18": ["Sensitized-allergen exposure", "st.sidebar.radio(v[0],[True,False],index=1,horizontal=True)"],
        "A19": ["Previous asthma-induced intubation or ICU admission", "st.sidebar.radio(v[0],[True,False],index=1,horizontal=True)"],
        "A20": ["Low FEV1 (especially <60% predicted)", "st.sidebar.radio(v[0],[True,False],index=1,horizontal=True)"],
        "A21": ["Obesity", "st.sidebar.radio(v[0],[True,False],index=1,horizontal=True)"],
        "A22": ["Food allergy", "st.sidebar.radio(v[0],[True,False],index=1,horizontal=True)"],
        "A23": ["Chronic rhinosinusitis", "st.sidebar.radio(v[0],[True,False],index=1,horizontal=True)"],
        "A24": ["Poor adherence/inhaler technique", "st.sidebar.radio(v[0],[True,False],index=1,horizontal=True)"]
    }

    Dx_criteria = control_factors, exacerbation_risk_factors

    return list(map(lambda n: {k: [v[0], eval(v[1])]
                               for k, v in n.items()}, Dx_criteria))


# ----------------------------------------------------------


def assess_user_data(data):
    '''
    I: patient-asthma data
    O: asthma Dx per 2020 GINA criteria
    '''

    asthma_classification_dict = {
        "H4": "acute exacerbation",
        "H6": "intermittent asthma",
        "H8": "mild persistent asthma",
        "H10": "moderate persistent asthma",
        "H14": "severe persistent asthma"
    }

    exacerbation_RF = [v[1] for k, v in data[1].items()]

    severely_uncontrolled_asthma = [
        data[0]['A5'][1] > 2,
        data[0]['A6'][1] > 2,
        data[0]['A7'][1] == True,
        data[0]['A8'][1] == True
    ]

    # classification algorithm v2

    asthma_classification = None
    asthma_exacerbation = None
    severely_uncontrolled_asthma_count = 0

    if data[0]['A15'][1]:
        if data[0]['A4'][1]:
            asthma_exacerbation = f"with {asthma_classification_dict['H4']}"
        if data[0]['A5'][1] > 2 or data[0]['A6'][1] > 2:
            if data[0]['A5'][1] > 3 or data[0]['A6'][1] > 3 or data[0]['A7'][1] or any(exacerbation_RF):
                for i in severely_uncontrolled_asthma:
                    if i:
                        severely_uncontrolled_asthma_count += 1
                if severely_uncontrolled_asthma_count > 2:
                    asthma_classification = asthma_classification_dict["H14"]
                else:
                    asthma_classification = asthma_classification_dict["H10"]
            else:
                asthma_classification = asthma_classification_dict["H8"]
        else:
            asthma_classification = asthma_classification_dict["H6"]
        return " ".join([i for i in [asthma_classification, asthma_exacerbation] if i])
    else:
        return "Alternative diagnoses must be excluded prior to assessment of asthma severity"


# * Store user input into a variable

user_data = get_user_data()
# ----------------------------------------------------------

# # * Set a subheader and display users input


# ! displaying user input as raw code;
# todo: convert to pandas dataframe

# st.subheader('User Input')
# st.write(user_data)

# ----------------------------------------------------------

# # * Create and train model

# RandomForestClassifier = RandomForestClassifier()
# RandomForestClassifier.fit(X_train, Y_train)

# ----------------------------------------------------------

# # * Show model's test accuracy score

# st.subheader('Model Test Accuracy Score:')
# st.write(str(accuracy_score(Y_test, RandomForestClassifier.predict(X_test)) * 100) + '%')

# ----------------------------------------------------------

# # * Store model's predictions in a variable

# prediction = RandomForestClassifier.predict(user_input)

# ----------------------------------------------------------


# * Set a subheader and display result

st.subheader('Result:')
st.write(assess_user_data(user_data))
