
'''
Encoding: UTF-8
Title: asthma-calc-x-web.py
Created: 2022-10-17 02:24:01
@author: samantix
'''

# + Description: This program assesses asthma severity per 2020 GINA criteria

# ----------------------------------------------------------

# * Import libraries

#import pandas as pd
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
## Classifies asthma severity per 2022 GINA criteria
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
        "A15": ["Pre-established asthma diagnosis", "st.sidebar.radio(v[0],[True,False],index=1,horizontal=True)"],
        "A4": ["Currently symptomatic", "st.sidebar.radio(v[0],[True,False],index=1,horizontal=True)"],
        "A5": ["Daytime asthma Sx per week", "st.sidebar.number_input(v[0],0,7)"],
        "A6": ["Rescue inhaler uses per week", "st.sidebar.number_input(v[0],0,7)"],
        "A7": ["Asthmatic-awakening >0 per month", "st.sidebar.radio(v[0],[True,False],index=1,horizontal=True)"],
        "A8": ["Asthma-limited physical activity", "st.sidebar.radio(v[0],[True,False],index=1,horizontal=True)"]

        # @ not 2022 GINA criteria
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

    return [{k: [v[0], eval(v[1])] for k, v in n.items()} for n in Dx_criteria]
# ----------------------------------------------------------


def assess_user_data(data):
    '''
    I: patient-asthma data
    O: asthma Dx per 2020 GINA criteria
    '''

    asthma_class = {
        "H4": "acute exacerbation",
        # The 4 classes below describe severity;
        # which is assessed retrospectively (post ??? 2 months of Tx)
        # via Tx-level required to control Sx & exacerbations
        # Thus, newly diagnosed asthma cannot have a severity
        "H6": "intermittent asthma",
        "H8": "mild persistent asthma",
        "H10": "moderate persistent asthma",
        "H14": "severe persistent asthma"
    }

    exacerbation_RF = [v[1] for k, v in data[1].items()]

    severe_un_ctrl = [
        data[0]['A5'][1] > 2,
        data[0]['A6'][1] > 2,
        data[0]['A7'][1] == True,
        data[0]['A8'][1] == True
    ]

    # classification algorithm v2

    asthma_Dx = None
    asthma_exacerbation = None
    # severe_count = 0
    # asthma diagnosis must be confirmed prior to initiating assessment thereof
    if data[0]['A15'][1]:
        if data[0]['A4'][1]:
            asthma_exacerbation = f"with {asthma_class['H4']}"
        if data[0]['A5'][1] > 2 or data[0]['A6'][1] > 2:
            if data[0]['A5'][1] > 3 or data[0]['A6'][1] > 3 or data[0]['A7'][1] or data[0]['A8'][1] or any(exacerbation_RF):
                severe_count = 0
                if [severe_count := severe_count + 1 for i in severe_un_ctrl if i][-1] > 2:
                    asthma_Dx = asthma_class["H14"]
                else:
                    asthma_Dx = asthma_class["H10"]
            else:
                asthma_Dx = asthma_class["H8"]
        else:
            asthma_Dx = asthma_class["H6"]
        return " ".join([i for i in [asthma_Dx, asthma_exacerbation] if i])
    else:
        return "Asthma diagnosis must be confirmed prior to initiating assessment thereof."

# ----------------------------------------------------------

# * Store user input into a variable


user_data = get_user_data()

# ----------------------------------------------------------

# # * Set a subheader and display users input


# ! displaying user input as raw code;
# todo: convert to pandas dataframe

# st.subheader('User Input')
# st.write(user_data)

# ----------------------------------------------------------

# * Set a subheader and display result

st.subheader('Result:')
st.write(assess_user_data(user_data))
