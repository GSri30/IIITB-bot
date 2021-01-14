#discord
from discord.ext import commands
from discord.utils import get
from discord.channel import DMChannel
#constants
from __constants import CHECK_EMOJI,CROSS_EMOJI
#secret
from cogs.secret import DEVELOPERS_CHANNEL


#General Cog
class General(commands.Cog,name="General Cog"):
    def __init__(self,bot):
        self.bot=bot
    
    def is_in_channel(self,ctx,channel_id):
        return (channel_id and (str(ctx.message.channel.id) == str(channel_id))) 
        
    def is_a_DM(self,ctx):
        return isinstance(ctx.channel,DMChannel)

    @commands.command(name="feature-request",help="Send a feature request to the admins. (non-anonymous request)")
    async def request(self,ctx,*,feature:str):
        if self.is_a_DM(ctx):
            await ctx.message.add_reaction(CROSS_EMOJI)
            await ctx.author.send(f"Sorry. You cannot DM me for this! :neutral_face:")
            return
            
        await ctx.message.add_reaction(CHECK_EMOJI)
        dev_channel=get(ctx.guild.channels,id=int(DEVELOPERS_CHANNEL))
        await dev_channel.send(f"Feature request by {ctx.message.author}.\n\"{feature}\"")

    @commands.command(name="flag",hidden=True)
    async def flag(self,ctx):
        await ctx.author.send(f"Too many CTFs ahh :joy: Nothing special here.")

def setup(bot):
    bot.add_cog(General(bot))