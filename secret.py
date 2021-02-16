from os import getenv
import os
from dotenv import load_dotenv

BASEDIR=os.path.abspath(os.path.dirname(__file__))

load_dotenv(os.path.join(BASEDIR,'.env'))

#SMTP
SENDER_ID=os.getenv("SENDER_ID")
SENDER_PASSWORD=os.getenv("SENDER_PASSWORD")

# Database

# Root
MYSQL_ROOT_USER=os.getenv("MYSQL_ROOT_USER")
MYSQL_ROOT_PASSWORD=os.getenv("MYSQL_ROOT_PASSWORD")

# Normal User
MYSQL_USER=os.getenv("MYSQL_USER")
MYSQL_PASSWORD=os.getenv("MYSQL_PASSWORD")

# Other specs
MYSQL_HOST=os.getenv("MYSQL_HOST")
MYSQL_DATABASE=os.getenv("MYSQL_DATABASE")

# Just for safe side, even if settings are changed, will use production mode (In production)
# Will always be true in production server
PRODUCTION=os.getenv("PRODUCTION")

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