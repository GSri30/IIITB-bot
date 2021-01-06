from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent

DATABASE_NAME = "MainDatabase.db"
DATABASE_PATH = os.path.join(BASE_DIR,"Database",DATABASE_NAME)
EXCEL_NAME = "MainDatabaseExcel.csv"
EXCEL_PATH = os.path.join(BASE_DIR,"Database",EXCEL_NAME)



#! Add any newly created COGS here

COGS=[
    "cogs.Greetings",
    "cogs.Admin",
    "cogs.General",
    "cogs.Errors",
    "cogs.Couriers",
    "cogs.CP",
]