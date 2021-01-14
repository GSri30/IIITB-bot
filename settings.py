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


#! Add the respective help commands

HELP={
    "Admin Cog": {
                "register":"Registers a user using their IIIT-B domain mail id.",
                "filter-ban":"Filters out the unauthorized users and bans them from the server.",
                "filter-kick":"Filters out the unauthorized users and kicks them out from the server.",
                "ban":"Bans the specified user from the server.",
                "kick":"Kicks out the specified user from the server.",
                "count-role":"Returns the count of members of specified role in the server.",
                "list":"Gives the database list in an excel sheet form.",
                "update-roles":"Updates the roles from 'role1' to 'role2'.",
            },
    "Authentication Cog": {
                        "verify":"Verifies the user email using an associated auto generated key.",
                        "assign":"Helps you to assign a suitable role for yourself to view the channels.",
                        "enter":"Helps you to enter into the server.",
                        },
    "Base Cog": {
                "help":"Shows this message.",
            },
    "Couriers Cog": {
                    "couriers":"Gives you your couriers list.(if any)",
                },
    "Competitive Programming Cog": {
                                    "random-cf":"Gives a random Codeforces question."
                                },
    "General Cog": {
                    "feature-request":"Send a feature request to the admins. (non-anonymous request)",
                },
}


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