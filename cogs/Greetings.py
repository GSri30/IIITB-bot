#discord
from discord.ext import commands
from discord.utils import get
#secret
from cogs.secret import NEWBIE,GUILD,VERIFICATION_CHANNEL,WELCOME_CHANNEL

#Greetings Cog
class Greetings(commands.Cog,name="Greetings Cog"):
    def __init__(self,bot):
        self.bot=bot
    
    @commands.Cog.listener()
    async def on_member_join(self,member):
        if not member.bot:
            await member.add_roles(get(get(self.bot.guilds,name=GUILD).roles,name=NEWBIE))
            await member.send((f"Hey Hii! You need to verify your IIITB mail id in order to get into the server! "
                                f"Get over to <#{VERIFICATION_CHANNEL}> for verification. :smile:"
                                ))
            return

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.bot.user.name} has connected to Discord!')

def setup(bot):
    bot.add_cog(Greetings(bot))