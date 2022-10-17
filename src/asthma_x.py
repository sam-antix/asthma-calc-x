'''
Encoding: UTF-8
Title: asthma_Dx_Tx_3.py
Created: 2022-10-15 22:17:29
@author: samantix
'''


# ----------------------------------------------------------
# # * Asthma Assessment via GINA criteria
# ----------------------------------------------------------

# todo: format user input: strip white space, capitalize booleans, etc.

# +RECORD DATA+ ----------------------------------------------------------

def set_data():
    '''
    # * records asthma assessment
    # iterating through both dicts passed as tuple;
    # using 0th val indices as user prompts;
    # using 1st val indices to typcast 3rd val, via eval()
    '''

    # * control_factors v4 (type-casting keyword changed to string 2/2 problematic O/P)

    control_factors = {
        'A4': ['currently symptomatic (True/False)', "bool", None],
        'A5': ['daytime asthma Sx per week (integer)', "int", None],
        'A6': ['rescue inhaler uses per week (integer)', "int", None],
        'A7': ['asthmatic-awakening ≥1 per month (True/False)', "bool", None],
        'A8': ['asthma-limited physical activity (True/False)', "bool", None],
        'A9': ['≥1 annual exacerbation (True/False)', "bool", None],
        'A10': ['asthma triggers (True/False)', "bool", None],
        'A11': ['atopy (personal or FMH) (True/False)', "bool", None],
        'A12': ['characteristic musical wheezing on PE (True/False)', "bool", None],
        'A15': ['alternative Dx have been excluded (True/False)', "bool", None]
    }

    # * exacerbation_risk_factors v2

    exacerbation_risk_factors = {
        "A17": ["tobacco smoke exposure (True/False)", "bool", None],
        "A18": ["sensitized allergen exposure (True/False)", "bool", None],
        "A19": ["previous asthma-induced intubation or ICU admission (True/False)", "bool", None],
        "A20": ["low FEV1 (especially <60% predicted) (True/False)", "bool", None],
        "A21": ["obesity (True/False)", "bool", None],
        "A22": ["food allergy (True/False)", "bool", None],
        "A23": ["chronic rhinosinusitis (True/False)", "bool", None],
        "A24": ["poor adherence/inhaler technique (True/False)", "bool", None]
    }

    # ----------------------------------------------------------

    # pack both sets of questions into a tuple; AND
    #   map a single dict comprehension expression to both Q banks via lambda.

    Dx_criteria = control_factors, exacerbation_risk_factors

    return list(map(lambda n: {k: [v[0], v[1], eval(v[1])(input(f"{v[0]}: "))]
                               for k, v in n.items()}, Dx_criteria))


# +ANALYZE DATA+ ----------------------------------------------------------


def assess_data(data):
    '''
    I: patient-asthma data
    O: asthma Dx
    '''

    asthma_classification_dict = {
        "H4": "acute exacerbation",
        "H6": "intermittent asthma",
        "H8": "mild persistent asthma",
        "H10": "moderate persistent asthma",
        "H14": "severe persistent asthma"
    }

    exacerbation_RF = [v[2] for k, v in data[1].items()]

    severely_uncontrolled_asthma = [
        data[0]['A5'][2] > 2,
        data[0]['A6'][2] > 2,
        data[0]['A7'][2] == True,
        data[0]['A8'][2] == True
    ]

    # classification algorithm v2

    asthma_classification = None
    asthma_exacerbation = None
    severely_uncontrolled_asthma_count = 0

    if data[0]['A15'][2]:
        if data[0]['A4'][2]:
            asthma_exacerbation = f"with {asthma_classification_dict['H4']}"
        if data[0]['A5'][2] > 2 or data[0]['A6'][2] > 2:
            if data[0]['A5'][2] > 3 or data[0]['A6'][2] > 3 or data[0]['A7'][2] or any(exacerbation_RF):
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
        return "alternative diagnoses must be excluded"

# ! ----------------------------------------------------------


# todo: review implementation relevance

# asthma_exacerbation = {
#     "sx": [
#         "breathlessness",
#         "wheezing",
#         "cough",
#         "chest_tightness",
#         "worsened_exercise_intolerance"
#     ],
#     "severity": [
#         "provoked by exertion",
#         "present at rest",
#         "sx-related sleep disturbance"
#     ]
# }

# print(asthma_exacerbation)
# FEV1/FVC is normal if > 5th %ile (i.e., > z-score of -1.645)

# ! ----------------------------------------------------------

# @ --------------------------------------------- @
# @                   TESTING                     @
# @ --------------------------------------------- @

print("")
print(assess_data(set_data()))
