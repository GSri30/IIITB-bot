from discord.ext import commands

from os import getenv
from dotenv import load_dotenv
load_dotenv()

class Greetings(commands.Cog,name="Greetings Cog"):
    def __init__(self,bot):
        self.bot=bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.bot.user.name} has connected to Discord!')



def setup(bot):
    bot.add_cog(Greetings(bot))