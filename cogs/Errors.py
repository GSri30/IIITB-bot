from discord.ext import commands
from discord.utils import get

from os import getenv,path
from dotenv import load_dotenv
load_dotenv()
ADMIN_LOG=getenv("ADMIN_LOG")

class Errors(commands.Cog,name="Errors Cog"):
    def __init__(self,bot):
        self.bot=bot

    @commands.Cog.listener()
    async def on_command_error(self,ctx, error):
        if isinstance(error, commands.errors.CheckFailure):
            await ctx.send(f'You do not have the required permission to use this command. Try contacting admins!')
        elif(isinstance(error, commands.errors.MissingRequiredArgument)):
            await ctx.send(f"{error}")
        else:
            log_channel=get(ctx.guild.channels,name=ADMIN_LOG)
            await log_channel.send(f"{error}")

def setup(bot):
    bot.add_cog(Errors(bot))