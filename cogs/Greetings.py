from discord.ext import commands
from discord.utils import get

from os import getenv
from dotenv import load_dotenv
load_dotenv()
NEWBIE=getenv("NEWBIE")
GUILD=getenv("GUILD")

class Greetings(commands.Cog,name="Greetings Cog"):
    def __init__(self,bot):
        self.bot=bot
    
    @commands.Cog.listener()
    async def on_member_join(self,member):
        await member.add_roles(get(get(self.bot.guilds,name=GUILD).roles,name=NEWBIE))

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.bot.user.name} has connected to Discord!')


def setup(bot):
    bot.add_cog(Greetings(bot))