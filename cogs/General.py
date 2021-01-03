from discord.ext import commands
from discord.utils import get
from __constants import UNCHECK_EMOJI
from bcrypt import bcrypt

from os import getenv
from dotenv import load_dotenv
load_dotenv()
AUTH_CHANNEL=getenv("AUTH")



class General(commands.Cog,name="General Cog"):
    def __init__(self,bot):
        self.bot=bot

    @commands.command(name="register",help="Registers a user using their IIIT-B domain mail id.")
    async def register(self,ctx, mailID:str):
        if(str(ctx.channel.id)!=AUTH_CHANNEL):
            await ctx.send(f"This command cannot be used from here.")
            return
        #send_mail(mailID,passgen())
        await ctx.message.add_reaction(UNCHECK_EMOJI)
        await ctx.send(f"{mailID} registered for user {ctx.author} with {ctx.author.id}")

    @commands.command(name="verify",help="Verifies the user email using an associated auto generated key.")
    async def verify(self,ctx,key:str):
        if bcrypt.match(key,usrhash):
            await ctx.author.send(f"You made it! Welcome to IIITB discord community!")
        else:
            await ctx.author.send(f"Sorry, you entered a wrong key. Try again!")

    @commands.command(name="fq",help="Send a feature requested by the user to the develpers.")
    async def request(self,ctx,*,feature:str):
        await get(self.bot.get_all_channels(),name=self.CHANNEL).send(f"Feature request by {ctx.user.name}.\n\"{feature}\"")


def setup(bot):
    bot.add_cog(General(bot))