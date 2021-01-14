from pathlib import Path
import os

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


# f"{RIGHT_ARROW}: scholars\n\n"
# f"{RIGHT_ARROW}: imt2016\n\n"
# f"{RIGHT_ARROW}: imt2017\n\n"
# f"{RIGHT_ARROW}: imt2018\n\n"
# f"{RIGHT_ARROW}: mt2019\n\n"
# f"{RIGHT_ARROW}: dt2019\n\n"
# f"{RIGHT_ARROW}: imt2019\n\n"
# f"{RIGHT_ARROW}: mt2020\n\n"
# f"{RIGHT_ARROW}: dt2020\n\n"
# f"{RIGHT_ARROW}: imt2020\n\n"
# f"You can use !assign command for the same!\n"
# f"Example : !assign imt2020"