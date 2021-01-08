#discord
from discord.ext import commands
from discord.channel import DMChannel
#constants
from __constants import CHECK_EMOJI


#Couriers Cog
class Couriers(commands.Cog,name="Couriers Cog"):
    def __init__(self,bot):
        self.bot=bot
    
    def is_a_DM(self,ctx):
        return isinstance(ctx.channel,DMChannel)

    @commands.command(name="couriers",help="Gives you your couriers list.(if any)")
    async def couriers(self,ctx,mobile:str):
        await ctx.message.add_reaction(CHECK_EMOJI)
        await ctx.send(f"Feature coming soon! :smile:")



def setup(bot):
    bot.add_cog(Couriers(bot))