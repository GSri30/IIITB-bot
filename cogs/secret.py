from os import getenv
from dotenv import load_dotenv

load_dotenv()


#channels
REGISTRATION_CHANNEL=getenv("REGISTRATION")
VERIFICATION_CHANNEL=getenv("VERIFICATION")
RULES_CHANNEL=getenv("RULES")
ASSIGN_CHANNEL=getenv("ASSIGN")
ADMIN_LOG=getenv("ADMIN_LOG")
SAC_CHANNEL=getenv("SAC")
DEVELOPERS_CHANNEL=getenv("DEVELOPERS")
WELCOME_CHANNEL=getenv("WELCOME")
CP_CHANNEL=getenv("CP")

#roles
ADMIN=getenv("ADMIN")
NEWBIE=getenv("NEWBIE")

#guild
GUILD=getenv("GUILD")

#database
DATABASE_URL=getenv("DATABASE_URL")

#Clist API
CLIST_USERNAME=getenv("CLIST_USERNAME")
CLIST_KEY=getenv("CLIST_KEY")