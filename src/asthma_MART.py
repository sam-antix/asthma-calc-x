
'''
Encoding: UTF-8
Title: asthma_MART.py
Created: 2022-10-19 03:29:11
@author: samantix
'''

# * ----------------------------------------------------------
# * UPDATE:
# + all track functions working
# + all ICS functions working

# todo:
# @ create A&P algorithms
# @ figure out what to do w/ Rx variables

# * ----------------------------------------------------------


def get_LD_ICS():
    '''
    returns all dict entries correlating to LD_ICS formulations
    '''
    return "\n".join([f"{k2} {v2[1][0][0]}{v2[2]} {v2[0]}" for k, v in ICS.items() for k2, v2 in v.items()])

# * ----------------------------------------------------------


def get_MD_ICS():
    '''
    returns all dict entries correlating to MD_ICS formulations
    '''
    return "\n".join([f"{k2} {v2[1][1][0]}{v2[2]} {v2[0]}" for k, v in ICS.items() for k2, v2 in v.items()])
# * ----------------------------------------------------------


def get_HD_ICS():
    '''
    returns all dict entries correlating to HD_ICS formulations
    '''
    return "\n".join([f"{k2} {v2[1][2][0]}{v2[2]} {v2[0]}" for k, v in ICS.items() for k2, v2 in v.items()])
# * ----------------------------------------------------------


def get_track(track):
    '''
    I: int correlating to track number
    O: GINA steps to respective track
    '''
    return "\n".join([f"{k1} {k2}: {', '.join(v2[track-1])}" for k1, v1 in GINA_Tx_steps.items()
                      for k2, v2 in v1.items()])

# * ----------------------------------------------------------


BDP = ["beclometasone dipropionate", "BDP"]
DPI = ["dry powder inhaler", "DPI"]
HFA = ["hydrofluoroalkane propellant", "HFA"]
# ICS by pMDI should preferably be used with a spacer
pMDI = ["pressurized metered dose inhaler", "pMDI"]
pMDI_snp = [pMDI[0] + "_standard (non-fine) particle", "pMDI_snp"]
unit = "mcg"

# * ----------------------------------------------------------

# todo: replace these w/ literal substitutes
LD_ICS_FALABA = "budesonide-formoterol"
SABA = "SABA (albuterol, Levalbuterol, etc.)"

# * ----------------------------------------------------------

qD_controller_adherence_likely = None

LD_ICS = "LD_ICS"   # get_LD_ICS()
MD_ICS = "MD_ICS"   # get_MD_ICS()
HD_ICS = "HD_ICS"   # get_HD_ICS()

LD_ICS_LABA = "LD-ICS-LABA"
MD_ICS_formoterol = "MD-ICS-formoterol"
MHD_ICS_LABA = "Medium/High-dose ICS-LABA"
LAMA = "LAMA"

# * ----------------------------------------------------------

# Table shows metered doses
ICS = {
    0: {
        # Name
        "BDP": [
            # Route
            "(pMDI_snp, HFA)",
            [
                # low-dose
                ["200-500"],
                # medium-dose
                ["500-1000"],
                # high-dose
                [">1000"]
            ],
            unit
        ]
    },

    1: {
        # Name
        "BDP":  [
            # Route
            "(DPI or pMDI, extrafine particle, HFA)",
            [
                # low-dose
                ["100-200"],
                # medium-dose
                ["200-400"],
                # high-dose
                [">400"]
            ],
            unit
        ]
    },

    2: {
        # Name
        "Budesonide": [
            # Route
            "(DPI or pMDI_snp, HFA)",
            [
                # low-dose
                ["200-400"],
                # medium-dose
                ["400-800"],
                # high-dose
                [">800"]
            ],
            unit
        ]
    },

    3: {
        # Name
        "Ciclesonide": [
            # Route
            "(pMDI, extrafine particle, HFA)",
            [
                # low-dose
                ["80-160"],
                # medium-dose
                ["160-320"],
                # high-dose
                [">320"]
            ],
            unit
        ]
    },

    4: {
        # Name
        "Fluticasone furoate": [
            # Route
            "(DPI)",
            [
                # low-dose
                ["100"],
                # medium-dose
                ["100"],
                # high-dose
                ["200"]
            ],
            unit
        ]
    },

    5: {
        # Name
        "Fluticasone propionate": [
            # Route
            "(DPI)",
            [
                # low-dose
                ["100-250"],
                # medium-dose
                ["250-500"],
                # high-dose
                [">500"]
            ],
            unit
        ]
    },

    6: {
        # Name
        "Fluticasone propionate": [
            # Route
            "(pMDI_snp, HFA)",
            [
                # low-dose
                ["100-250"],
                # medium-dose
                ["250-500"],
                # high-dose
                [">500"]
            ],
            unit
        ]
    },

    7: {
        # Name
        "Mometasone furoate": [
            # Route
            "(DPI)",
            [
                # low-dose
                ["(device-dependent dosage)"],
                # medium-dose
                ["(device-dependent dosage)"],
                # high-dose
                ["(device-dependent dosage)"]
            ],
            ""
        ]
    },

    8: {
        # Name
        "Mometasone furoate": [
            # Route
            "(pMDI_snp}, HFA)",
            [
                # low-dose
                ["200-400"],
                # medium-dose
                ["200-400"],
                # high-dose
                ["400"]
            ],
            unit
        ]
    }
}
# * ----------------------------------------------------------
# adults & adolescents

# pre_reqs

# 1. confirm Dx
# 2. assess Sx_ctrl
# 3. assess modifiable_RF
# 4. assess comorbidities
# 5. assess inhaler_technique
# 6. assess inhaler_adherence
# 7. assess patient_prefs_goals

# 8. determine appropriate track via qD_"controller"_adherence_likelihood

# * ----------------------------------------------------------

GINA_Tx_steps = {
    "step_1": {
        "controller": [
            # Track 1
            ["None"],
            # Track 2
            ["None"]
        ],
        "reliever": [
            # Track 1
            [LD_ICS_FALABA],
            # Track 2
            [SABA, LD_ICS]
        ]
    },
    "step_2": {
        "controller": [
            # Track 1
            ["None"],
            # Track 2
            [LD_ICS]
        ],
        "reliever": [
            # Track 1
            [LD_ICS_FALABA],
            # Track 2
            [SABA]
        ]
    },
    "step_3": {
        "controller": [
            # Track 1
            [LD_ICS_FALABA],
            # Track 2
            [LD_ICS_LABA]
        ],
        "reliever": [
            # Track 1
            [LD_ICS_FALABA],
            # Track 2
            [SABA]
        ]

    },
    "step_4": {
        "controller": [
            # Track 1
            [MD_ICS_formoterol],
            # Track 2
            [MHD_ICS_LABA]
        ],
        "reliever": [
            # Track 1
            [LD_ICS_FALABA],
            # Track 2
            [SABA]
        ]
    },
    "step_5": {
        "controller": [
            # Track 1
            [MD_ICS_formoterol, LAMA],
            # Track 2
            [MHD_ICS_LABA, LAMA]
        ],
        "reliever": [
            # Track 1
            [LD_ICS_FALABA],
            # Track 2
            [SABA]
        ]
    },
}

# @ ----------------------------------------------------------

# @ todo: finish A&P algorithm

# if qD_controller_adherence_likely:
#     take_track_1
# else:
#     take_track_2

# ----------------------------------------------------------

# if not Tx_status:
#     if Sx < 2 qMo and not exacerbation_RF:
#         step_1
# else:
#     if asthma == well_controlled on current_step  # step_2
#     step_down(current_step)
#     else:
#         step_up(current_step)

# Tx_status = {
#     0: [“naive”, None],
#     1: [step_1], None,
#     2: [],
#     3: [],
#     4: [],
#     5: []
# }

# @ --------------------------------------------- @
# @                   TESTING                     @
# @ --------------------------------------------- @

# ----------------------------------------------------------
print("")
print("--------------------")
print("     Track 1        ")
print("--------------------")
# ----------------------------------------------------------
print(get_track(1))
# ----------------------------------------------------------
print("")
print("--------------------")
print("     Track 2        ")
print("--------------------")
# ----------------------------------------------------------
print(get_track(2))
# ----------------------------------------------------------
print("")
print("--------------------")
print("     LD-ICS         ")
print("--------------------")
# ----------------------------------------------------------
print(get_LD_ICS())
# ----------------------------------------------------------
print("")
print("--------------------")
print("     MD-ICS         ")
print("--------------------")
# ----------------------------------------------------------
print(get_MD_ICS())
# ----------------------------------------------------------
print("")
print("--------------------")
print("     HD-ICS         ")
print("--------------------")
# ----------------------------------------------------------
print(get_HD_ICS())
# ----------------------------------------------------------
