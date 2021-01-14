#discord
from discord.ext import commands
from discord.utils import get
from discord.channel import DMChannel
#secret
from cogs.secret import ADMIN_LOG, GUILD,NEWBIE
#constants
from __constants import CROSS_EMOJI

#!work on this
#Use private msg only etc decorators
#refer exception-hierarchy

#Errors cog
class Errors(commands.Cog,name="Errors Cog"):
    def __init__(self,bot):
        self.bot=bot

    def is_a_DM(self,ctx):
        return isinstance(ctx.channel,DMChannel)

    @commands.Cog.listener()
    async def on_command_error(self,ctx, error):
        if isinstance(error, commands.errors.CheckFailure) or isinstance(error, commands.errors.UserInputError) or isinstance(error,commands.errors.CommandNotFound):
            await ctx.send(f"<@{ctx.author.id}> {error}")
        elif(isinstance(error,commands.errors.CommandOnCooldown)):
            await ctx.send(f"<@{ctx.author.id}> Hey stop spamming.\n{error}")
        else:
            await ctx.message.add_reaction(CROSS_EMOJI)
            log_channel=get(get(self.bot.guilds,name=GUILD).channels,id=int(ADMIN_LOG))
            summary=f"Error :\n{error}\nFor the message :\n{ctx.message.content}\nUsed by :\n{ctx.author}"
            await log_channel.send(summary)

def setup(bot):
    bot.add_cog(Errors(bot))