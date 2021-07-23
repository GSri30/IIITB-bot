from os import getenv
import os
from dotenv import load_dotenv

BASEDIR=os.path.abspath(os.path.dirname(__file__))

load_dotenv(os.path.join(BASEDIR,'.env'))

#Base Token
TOKEN=os.getenv("DISCORD_TOKEN")

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

# For production side purposes
PRODUCTION=os.getenv("PRODUCTION")

#channels
RULES_CHANNEL=getenv("RULES")
WELCOME_CHANNEL=getenv("WELCOME")

SAC_CHANNEL=getenv("SAC")
REGISTRATION_CHANNEL=getenv("REGISTRATION")

ADMIN_LOG=getenv("ADMIN_LOG")
DEVELOPERS_CHANNEL=getenv("DEVELOPERS")

CP_CHANNEL=getenv("CP")

#roles
ADMIN=getenv("ADMIN")
NEWBIE=getenv("NEWBIE")

#guild
GUILD=getenv("GUILD")
GUILD_ID=getenv("GUILD_ID")

#Clist API
CLIST_USERNAME=getenv("CLIST_USERNAME")
CLIST_KEY=getenv("CLIST_KEY")

# Discord Link
DISCORD_LINK=getenv("DISCORD_LINK")

#OAuth2
CLIENT_ID=getenv("CLIENT_ID")
CLIENT_SECRET=getenv("CLIENT_SECRET")

# OAuth2 Verification Webhook
URL=getenv("URL")