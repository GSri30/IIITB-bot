from pathlib import Path
import os

# Turn 'ON' if you want to use production DB instead of a mysql db
# Else 'OFF' to use mysql db

DEVELOPMENT="ON"

BASE_DIR = Path(__file__).resolve().parent

DATABASE_NAME = "MainDatabase.db"
DATABASE_PATH = os.path.join(BASE_DIR,"Database",DATABASE_NAME)
EXCEL_NAME = "MainDatabaseExcel.csv"
EXCEL_PATH = os.path.join(BASE_DIR,"Database",EXCEL_NAME)


#! For any new feature, exclude newbies from using them and also disable DM
#! There shouldn't be any DM commands. If present, exclude newbies from using them.

#! Add any newly created COGS here

COGS=[
    "cogs.Base",
    "cogs.Admin",
    "cogs.Authentication",
    "cogs.General",
    "cogs.Errors",
    "cogs.Couriers",
    "cogs.CP",
]