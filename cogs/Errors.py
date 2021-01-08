#discord
from discord.ext import commands
from discord.utils import get
#secret
from cogs.secret import ADMIN_LOG

#Errors cog
class Errors(commands.Cog,name="Errors Cog"):
    def __init__(self,bot):
        self.bot=bot

    def channelObj(self,ctx,channel:str):
        obj=None
        for c in ctx.guild.channels:
            if str(c.id) == channel:
                obj=c
                break
        return obj

    @commands.Cog.listener()
    async def on_command_error(self,ctx, error):
        if isinstance(error, commands.errors.CheckFailure):
            await ctx.send(f'You do not have the required permission to use this command. Try contacting admins!')
        elif(isinstance(error, commands.errors.MissingRequiredArgument)):
            await ctx.send(f"{error}")
        else:
            log_channel=self.channelObj(ctx,ADMIN_LOG)
            await log_channel.send(f"{error}")

def setup(bot):
    bot.add_cog(Errors(bot))