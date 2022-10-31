
'''
Encoding: UTF-8
Title: asthma_MART.py
Created: 2022-10-19 03:29:11
@author: samantix
'''

# * ----------------------------------------------------------
# * UPDATE:
# 2022-10-27 23:47:39.000-05:00
# + changed lists to tuples for less memory consumption & faster iteration
# + corrected preferred controller from budesonide-formoterol to any ICS-formoterol

# + all track functions working
# + all ICS functions working

# todo:
# @ create A&P algorithms
# @ figure out what to do w/ Rx variables
# @ finish the consolidated ICS function
# @ find the function you want to slice [:]

# * ----------------------------------------------------------

# import streamlit as st

# * ----------------------------------------------------------


def get_LD_ICS():
    '''
    O: all dict entries correlating to LD_ICS formulations
    '''
    # Time complexity: O(1) # Rx's have fixed qty & dose ranges
    return "\n".join([f"{k2} {v2[1][0][0]}{v2[2]} {v2[0]}" for k, v in ICS.items()
                      for k2, v2 in v.items()])


# return {char: uc_str[(uc_str.index(char) + shift) % 26] for char in uc_str} | {char: lc_str[(lc_str.index(char) + shift) % 26] for char in lc_str}
# * ----------------------------------------------------------


def get_MD_ICS():
    '''
    O: all dict entries correlating to MD_ICS formulations
    '''
    # Time complexity: O(1) # Rx's have fixed qty & dose ranges
    return "\n".join([f"{k2} {v2[1][1][0]}{v2[2]} {v2[0]}" for k, v in ICS.items()
                      for k2, v2 in v.items()])
# * ----------------------------------------------------------


def get_HD_ICS():
    '''
    O: all dict entries correlating to HD_ICS formulations
    '''
    # Time complexity: O(1) # Rx's have fixed qty & dose ranges
    return "\n".join([f"{k2} {v2[1][2][0]}{v2[2]} {v2[0]}" for k, v in ICS.items()
                      for k2, v2 in v.items()])
# * ----------------------------------------------------------

# todo: finish this consolidated function of the above three


def get_ICS(dose):
    '''
    I: int: correlating to dose index in ICS dict i.e., 0=low, 1=medium, 2=high
    O: all dict entries correlating to HD_ICS formulations

    argument is provided by other fxn TBD (get_track?)
    '''
    # Time complexity: O(1) # Rx's have fixed qty & dose ranges
    return "\n".join([f"{k2} {v2[1][dose][0]}{v2[2]} {v2[0]}" for k, v in ICS.items()
                      for k2, v2 in v.items()])


# * ----------------------------------------------------------


def get_track(track):
    '''
    I: int; of track number
    O: str; of GINA steps per respective track

    argument provided by fxn TBD
    use: informational; another fxn (TBD) will return exact step per track
    '''
    # Time complexity: O(1) # Rx's have fixed qty & dose ranges
    return "\n".join([f"{k1} {k2}: {' + '.join(v2[track-1])}" for k1, v1 in GINA_Tx_steps.items()
                      for k2, v2 in v1.items()])
# * ----------------------------------------------------------


def get_step(track):
    '''
    I: int; of track number
    O: str; of GINA steps per respective track

    argument provided by fxn TBD
    use: recommended Tx per Dx status
    '''
    # Time complexity: O(1) # Rx's have fixed qty & dose ranges
    return "\n".join([f"{k1} {k2}: {', '.join(v2[track-1])}" for k1, v1 in GINA_Tx_steps.items()
                      for k2, v2 in v1.items()])

# * ----------------------------------------------------------


BDP = "beclometasone dipropionate"
bud = "budesonide"
cic = "ciclesonide"
FP = "fluticasone propionate"
FF = "fluticasone furoate"
MF = "mometasone furoate"

DPI = ("dry powder inhaler", "DPI")
HFA = ("hydrofluoroalkane propellant", "HFA")
# ICS by pMDI should preferably be used with a spacer
pMDI = ("pressurized metered dose inhaler", "pMDI")
pMDI_snp = (pMDI[0] + "_standard (non-fine) particle", "pMDI_snp")
unit = "mcg"

# * ----------------------------------------------------------

# todo: replace these w/ literal substitutes
LD_ICS_formoterol = "LD-ICS-formoterol"
SABA = "SABA (albuterol, Levalbuterol, etc.)"

# * ----------------------------------------------------------

qD_controller_adherence_likely = None

LD_ICS = "LD-ICS"   # get_LD_ICS()
MD_ICS = "MD-ICS"   # get_MD_ICS()
HD_ICS = "HD-ICS"   # get_HD_ICS()

LD_ICS_LABA = "LD-ICS-LABA"
MD_ICS_formoterol = "MD-ICS-formoterol"
MHD_ICS_LABA = "Medium/High-dose ICS-LABA"
LAMA = "LAMA"


# ! ----------------------------------------------------------
# per minimum req for Sx ctrl
severity = {
    "severe": ("high-dose ICS-LABA"),
    "mild": ("PRN-ICS-formoterol", "low-dose ICS"),
    "moderate": ("medium-dose ICS-LABA")
}
# ! ----------------------------------------------------------
# * ----------------------------------------------------------

# Table shows metered doses
ICS = {
    0: {
        # Name
        BDP: (
            # Route
            "(pMDI_snp, HFA)",
            (
                # low-dose
                ("200-500",),
                # medium-dose
                ("500-1000",),
                # high-dose
                (">1000",)
            ),
            unit
        )
    },

    1: {
        # Name
        BDP:  (
            # Route
            "(DPI or pMDI, extrafine particle, HFA)",
            (
                # low-dose
                ("100-200",),
                # medium-dose
                ("200-400",),
                # high-dose
                (">400",)
            ),
            unit
        )
    },

    2: {
        # Name
        bud: (
            # Route
            "(DPI or pMDI_snp, HFA)",
            (
                # low-dose
                ("200-400",),
                # medium-dose
                ("400-800",),
                # high-dose
                (">800",)
            ),
            unit
        )
    },

    3: {
        # Name
        cic: (
            # Route
            "(pMDI, extrafine particle, HFA)",
            (
                # low-dose
                ("80-160",),
                # medium-dose
                ("160-320",),
                # high-dose
                (">320",)
            ),
            unit
        )
    },

    4: {
        # Name
        FF: (
            # Route
            "(DPI)",
            (
                # low-dose
                ("100",),
                # medium-dose
                ("100",),
                # high-dose
                ("200",)
            ),
            unit
        )
    },

    5: {
        # Name
        FP: (
            # Route
            "(DPI)",
            (
                # low-dose
                ("100-250",),
                # medium-dose
                ("250-500",),
                # high-dose
                (">500",)
            ),
            unit
        )
    },

    6: {
        # Name
        FP: (
            # Route
            "(pMDI_snp, HFA)",
            (
                # low-dose
                ("100-250",),
                # medium-dose
                ("250-500",),
                # high-dose
                (">500",)
            ),
            unit
        )
    },

    7: {
        # Name
        MF: (
            # Route
            "(DPI)",
            (
                # low-dose
                ("(device-dependent dosage)",),
                # medium-dose
                ("(device-dependent dosage)",),
                # high-dose
                ("(device-dependent dosage)",)
            ),
            ""
        )
    },

    8: {
        # Name
        MF: (
            # Route
            "(pMDI_snp}, HFA)",
            (
                # low-dose
                ("200-400",),
                # medium-dose
                ("200-400",),
                # high-dose
                ("400",)
            ),
            unit
        )
    }
}
# * ----------------------------------------------------------
# adults & adolescents

# pre_reqs

# ! 1. confirm Dx
# + 2. assess Sx_ctrl
# ! 3. assess modifiable_RF
# ! 4. assess comorbidities
# ! 5. assess inhaler_technique
# ! 6. assess inhaler_adherence
# ! 7. assess patient_prefs_goals
# ! 8. assess likelihood of daily controller adherence

# * ----------------------------------------------------------

GINA_Tx_steps = {
    "step-1": {
        "controller": (
            # Track 1
            ("None",),
            # Track 2
            ("None",)
        ),
        "reliever": (
            # Track 1
            (LD_ICS_formoterol,),
            # Track 2
            (SABA, LD_ICS,)
        )
    },
    "step-2": {
        "controller": (
            # Track 1
            ("None",),
            # Track 2
            (LD_ICS,)
        ),
        "reliever": (
            # Track 1
            (LD_ICS_formoterol,),
            # Track 2
            (SABA,)
        )
    },
    "step-3": {
        "controller": (
            # Track 1
            (LD_ICS_formoterol,),
            # Track 2
            (LD_ICS_LABA,)
        ),
        "reliever": (
            # Track 1
            (LD_ICS_formoterol,),
            # Track 2
            (SABA,)
        )

    },
    "step-4": {
        "controller": (
            # Track 1
            (MD_ICS_formoterol,),
            # Track 2
            (MHD_ICS_LABA,)
        ),
        "reliever": (
            # Track 1
            (LD_ICS_formoterol,),
            # Track 2
            (SABA,)
        )
    },
    "step-5": {
        "controller": (
            # Track 1
            (MD_ICS_formoterol, LAMA),
            # Track 2
            (MHD_ICS_LABA, LAMA)
        ),
        "reliever": (
            # Track 1
            (LD_ICS_formoterol,),
            # Track 2
            (SABA,)
        )
    },
}


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
print("")
print("--------------------")
print("     HD-ICS         ")
print("--------------------")
# ----------------------------------------------------------
dose = 2
print(get_ICS(dose))
# ----------------------------------------------------------
