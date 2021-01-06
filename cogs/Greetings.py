from discord.ext import commands
from discord.utils import get

from os import getenv
from dotenv import load_dotenv
load_dotenv()
NEWBIE=getenv("NEWBIE")
GUILD=getenv("GUILD")
AUTH=getenv("AUTH")
WELCOME_CHANNEL=getenv("WELCOME")

class Greetings(commands.Cog,name="Greetings Cog"):
    def __init__(self,bot):
        self.bot=bot
    
    @commands.Cog.listener()
    async def on_member_join(self,member):
        if not member.bot:
            await member.add_roles(get(get(self.bot.guilds,name=GUILD).roles,name=NEWBIE))
            await member.send(f"Hey hii! You need to register your IIITB mail id in order to get into the server! Get over to <#{AUTH}> for registration. :smile:")
            return

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.bot.user.name} has connected to Discord!')

def setup(bot):
    bot.add_cog(Greetings(bot))