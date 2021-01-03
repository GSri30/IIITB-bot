from discord.ext import commands

from os import getenv
from dotenv import load_dotenv
load_dotenv()

class CP(commands.Cog,name="Competitive Programming Cog"):
    def __init__(self,bot):
        self.bot=bot

    @commands.command(name="randomq",help="Gives a random codeforces question of moderate-difficulty level")
    async def randomQ(self,ctx):
        await ctx.send(f"Feature coming soon! :smile:")


def setup(bot):
    bot.add_cog(CP(bot))