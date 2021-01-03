from discord.ext import commands

from os import getenv,path
from dotenv import load_dotenv
load_dotenv()

class Errors(commands.Cog,name="Errors Cog"):
    def __init__(self,bot):
        self.bot=bot

    @commands.Cog.listener()
    async def on_command_error(self,ctx, error):
        if isinstance(error, commands.errors.CheckFailure):
            await ctx.send(f'You do not have the required permission to use this command. Try contacting admins!')
        # elif(isinstance(error, commands.errors.MissingRequiredArgument)):
        #     await ctx.send(f"{error}")
        else:
            await ctx.send(f"{error}")

    #!NOT working
    @commands.Cog.listener()
    async def on_error(self,ctx,error):
        print("error\n\n")
        with open(path.dirname(__file__)+"/../err.log","a") as f:
            f.write(f"{error}\n")


def setup(bot):
    bot.add_cog(Errors(bot))