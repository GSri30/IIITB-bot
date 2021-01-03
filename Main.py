import os
from discord.ext import commands
from dotenv import load_dotenv
from settings import COGS

load_dotenv()
TOKEN=os.getenv("DISCORD_TOKEN")

def main():
    bot=commands.Bot(command_prefix="!")
    for PATH in COGS:
        bot.load_extension(PATH)
    bot.run(TOKEN)


if __name__ == "__main__":
    main()