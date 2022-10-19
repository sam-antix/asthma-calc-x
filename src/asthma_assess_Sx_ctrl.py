
'''
Encoding: UTF-8
Title: Sx_ctrl_assessment.py
Created: 2022-10-19 03:59:45
@author: samantix
'''

# * UPDATE
# + Sx control assessment function working

# todo
# @ impliment streamlit functionality

# ----------------------------------------------------------


def Sx_ctrl_assessment():
    '''
    A. Assessment of symptom control
    '''

    # * catalog queries

    Sx_ctrl_factors = {
        # over the last 4 weeks…
        0: ["Daytime symptoms more than twice/week?", None],
        1: ["Any night waking due to asthma?", None],
        2: ["SABA reliever needed more than twice/week?", None],
        3: ["Any activity limitation due to asthma?", None]
    }

    # ----------------------------------------------------------
    # * catalog classifications w/ descriptions & criteria thereof

    Sx_ctrl_classification = {
        0: ["well-controlled", [0]],
        1: ["partially-controlled", [1, 2]],
        2: ["uncontrolled", [3, 4]]
    }

    # ----------------------------------------------------------
    # * generate summative score from query responses

    Sx_ctrl_score = sum([v[1] for k, v in Sx_ctrl_factors.items() if v[1]])

    # ----------------------------------------------------------
    # * assess score per classification criteria

    return [v[0] for k, v in Sx_ctrl_classification.items() if Sx_ctrl_score in v[1]][0]

# ----------------------------------------------------------

# @ --------------------------------------------- @
# @                   TESTING                     @
# @ --------------------------------------------- @


print(Sx_ctrl_assessment())
