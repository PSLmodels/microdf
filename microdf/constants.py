# Constants for share of each benefit that is cash.
HOUSING_CASH_SHARE = 0.0
MCAID_CASH_SHARE = 0.0
MCARE_CASH_SHARE = 0.0
# https://github.com/open-source-economics/taxdata/issues/148
# https://docs.google.com/spreadsheets/d/1g_YdFd5idgLL764G0pZBiBnIlnCBGyxBmapXCOZ1OV4
OTHER_CASH_SHARE = 0.35
SNAP_CASH_SHARE = 0.0
SSI_CASH_SHARE = 1.0
TANF_CASH_SHARE = 0.25
# https://github.com/open-source-economics/C-TAM/issues/62.
VET_CASH_SHARE = 0.48
WIC_CASH_SHARE = 0.0

# Columns to remove from expanded_income to approximate TPC's Expanded Cash
# Income.
ECI_REMOVE_COLS = [
    "wic_ben",
    "housing_ben",
    "vet_ben",
    "mcare_ben",
    "mcaid_ben",
]

# Benefits.
BENS = [
    "housing_ben",
    "mcaid_ben",
    "mcare_ben",
    "vet_ben",
    "other_ben",
    "snap_ben",
    "ssi_ben",
    "tanf_ben",
    "wic_ben",
    "e02400",  # Social Security (OASDI).
    "e02300",  # Unemployment insurance.
]

MED_BENS = ["mcaid_ben", "mcare_ben", "vet_ben"]
