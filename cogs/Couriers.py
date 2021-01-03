from discord.ext import commands

from os import getenv
from dotenv import load_dotenv
load_dotenv()

class Couriers(commands.Cog,name="Couriers Cog"):
    def __init__(self,bot):
        self.bot=bot
    
    @commands.command(name="couriers",help="Gives you your couriers list.(if any)")
    async def couriers(self,ctx):
        await ctx.send(f"Feature coming soon! :smile:")



def setup(bot):
    bot.add_cog(Couriers(bot))