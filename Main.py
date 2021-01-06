import os
from discord.ext import commands
from discord import Intents
from dotenv import load_dotenv
from settings import COGS

#Database
from Database import sqlite

#enable priviliged intents

load_dotenv()
TOKEN=os.getenv("DISCORD_TOKEN")

def main():
    #for version >1.5.0 of discord py
    intents=Intents.default()
    intents.members=True
    
    bot=commands.Bot(command_prefix="!",intents=intents)
    for PATH in COGS:
        bot.load_extension(PATH)
    db=sqlite.SQLite()
    db.init()
    bot.run(TOKEN)

if __name__ == "__main__":
    main()