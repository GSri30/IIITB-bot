from discord.ext import commands
from discord.channel import DMChannel
from __constants import CHECK_EMOJI

from os import getenv
from dotenv import load_dotenv
load_dotenv()

class CP(commands.Cog,name="Competitive Programming Cog"):
    def __init__(self,bot):
        self.bot=bot

    def is_a_DM(self,ctx):
        return isinstance(ctx.channel,DMChannel)

    @commands.command(name="randomq",help="Gives a random codeforces question of moderate-difficulty level")
    async def randomQ(self,ctx):
        await ctx.message.add_reaction(CHECK_EMOJI)
        await ctx.send(f"Feature coming soon! :smile:\n")


def setup(bot):
    bot.add_cog(CP(bot))