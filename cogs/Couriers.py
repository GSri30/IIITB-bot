#discord
from discord.ext import commands
from discord.channel import DMChannel
from discord.utils import get
#constants
from __constants import CHECK_EMOJI,CROSS_EMOJI
#secret
from cogs.secret import NEWBIE


#Couriers Cog
class Couriers(commands.Cog,name="Couriers Cog"):
    def __init__(self,bot):
        self.bot=bot
    
    def is_a_DM(self,ctx):
        return isinstance(ctx.channel,DMChannel)

    def is_a_newbie(self,ctx):
        ok=get(ctx.author.roles,name=NEWBIE)
        return ok is not None

    @commands.command(name="couriers")
    async def couriers(self,ctx,mobile:str=None):
        if self.is_a_DM(ctx):
            await ctx.message.add_reaction(CROSS_EMOJI)
            await ctx.author.send(f"Sorry. You cannot DM me for this! :neutral_face:")
            return
            
        await ctx.message.add_reaction(CHECK_EMOJI)
        await ctx.send(f"Feature coming soon! :smile:")



def setup(bot):
    bot.add_cog(Couriers(bot))