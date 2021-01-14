#discord
from discord.ext import commands
from discord.utils import get
from discord import Activity,ActivityType
#secret
from cogs.secret import NEWBIE,GUILD,RULES_CHANNEL, WELCOME_CHANNEL
#settings
from settings import HELP
#constants
from __constants import _GREETINGS,GREETINGS
#other
import random

#Base Cog
class Base(commands.Cog,name="Base Cog"):
    def __init__(self,bot):
        self.bot=bot
    
    @commands.Cog.listener()
    async def on_member_join(self,member):
        if not member.bot:
            await member.add_roles(get(get(self.bot.guilds,name=GUILD).roles,name=NEWBIE))
            await member.send((f"<@{member.id}> Hey Hii!\nYou need to verify your IIITB mail id in order to get into the server!\n"
                                f"If you don't have any key, contact admins.\n"
                                f"If you have a key, head over to <#{RULES_CHANNEL}> and come back! I will be waiting. :smile:"
                                ))
            return
        
        greeting=random.choice(GREETINGS).replace(_GREETINGS, f"<@{member.id}>")
        get(get(self.bot.guilds,name=GUILD).channels,name=WELCOME_CHANNEL).send(greeting)


    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.change_presence(activity=Activity(type=ActivityType.listening, name="!help"))
        print(f'{self.bot.user.name} has connected to Discord!')

    # @commands.command(name="help")
    # async def help(self,ctx):
    #     pass
    

def setup(bot):
    bot.add_cog(Base(bot))