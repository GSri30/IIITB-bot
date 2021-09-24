from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent

DATABASE_NAME = "MainDatabase.db"
DATABASE_PATH = os.path.join(BASE_DIR,"Database",DATABASE_NAME)
EXCEL_NAME = "MainDatabaseExcel.csv"
EXCEL_PATH = os.path.join(BASE_DIR,"Database",EXCEL_NAME)
SUMMARY_NAME = "Summary.csv"
SUMMARY_PATH = os.path.join(BASE_DIR,"Database",SUMMARY_NAME)

# Used to remove old alumini of specified year difference
DELTA_YEAR=20

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

REDIRECT_URI='http://127.0.0.1:5000/verify'

OAUTH_URL="https://discord.com/api/oauth2/authorize?client_id=891043842030190613&redirect_uri=http%3A%2F%2F127.0.0.1%3A5000%2Fverify&response_type=code&scope=identify%20guilds.join"