import os
from discord.ext import commands
from discord import Intents
from dotenv import load_dotenv
from settings import COGS

#Database
from Database import sqlite

#enable priviliged intents
#https://stackoverflow.com/questions/46020703/smtp-authentication-error-with-django-on-heroku
#solve the authentication problem that would arrive while using heroku and smtp gmail


#While using iiitb mail for bot, use smtp-mail.outlook.com

#For now, the bot cannot be made as a general college bot hosted on somewhere, though its possible.
#The entire code can be made more abstract by inheritance,decorators,base classes etc

load_dotenv()
TOKEN=os.getenv("DISCORD_TOKEN")

def main():
    #for version >1.5.0 of discord py
    intents=Intents.default()
    intents.members=True
    
    #Don't change '!'
    bot=commands.Bot(command_prefix="!",intents=intents)
    
    for PATH in COGS:
        bot.load_extension(PATH)
    db=sqlite.SQLite()
    db.init()
    bot.run(TOKEN)


if __name__ == "__main__":
    main()