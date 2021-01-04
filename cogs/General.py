import re
from discord.ext import commands
from discord.utils import get
from discord.channel import DMChannel
from __constants import CHECK_EMOJI,UNCHECK_EMOJI,CROSS_EMOJI,LIKE_EMOJI,REGEX,DOMAIN,NON_STUDENT_MAILS
from Bcrypt import Bcrypt
from smtp import smtp

from os import getenv,path
from dotenv import load_dotenv
load_dotenv()
AUTH_CHANNEL=getenv("AUTH")
FQ_CHANNEL=getenv("FEATUREREQ")



class General(commands.Cog,name="General Cog"):
    def __init__(self,bot):
        self.bot=bot

    def validMail(self,mailID:str):
        if re.match(REGEX,mailID)==None or mailID.split("@")[1]!=DOMAIN:
            return False
        return True
    
    def is_in_channel(self,ctx,channel_id,dm_allowed:bool):
        return (channel_id and (str(ctx.message.channel.id) == str(channel_id))) or (dm_allowed and isinstance(ctx.channel,DMChannel))
        
    def store_in_db(self,ctx,mail:str,Hash:str):
        #store into the db
        return

    def get_hash(self,ctx):
        #if not-found return None
        return
    def verify_user(self,ctx,key:str):
        ExistingHash=self.get_hash(ctx)
        if ExistingHash==None:
            return False
        if bcrypt.Match(key,ExistingHash):
            #verify the user in DB
            return True
        return False

    @commands.command(name="register",help="Registers a user using their IIIT-B domain mail id.")
    async def register(self,ctx, mailID:str):
        if not self.is_in_channel(ctx,AUTH_CHANNEL,False):
            await ctx.message.add_reaction(CROSS_EMOJI)
            return
        if not self.validMail(mailID.lower()):
            await ctx.author.send(f"Wrong email entered. Try again!\nNOTE : Use only college mail ID.")
            await ctx.message.add_reaction(UNCHECK_EMOJI)
            return
        if any(str(mailID) == mail.lower() for mail in NON_STUDENT_MAILS):
            await ctx.author.send(f"You can only use a student mail ID!")
            await ctx.message.add_reaction(CROSS_EMOJI)
            return
        
        Key=Bcrypt.GeneratePassword()
        Hashed=Bcrypt.Hash(Key)
        smtp.send_mail(mailID,Key)
        
        await ctx.message.add_reaction(CHECK_EMOJI)
        self.store_in_db(ctx,mailID,Hashed)
        await ctx.author.send(f"{mailID} has been successfully mapped for you. Check your :email: to proceed further!")
        
    @commands.command(name="verify",help="Verifies the user email using an associated auto generated key.")
    async def verify(self,ctx,key:str):
        if not self.is_in_channel(ctx,AUTH_CHANNEL,True):
            await ctx.message.add_reaction(CROSS_EMOJI)
            return
        if self.verify_user(ctx,key):
            await ctx.message.add_reaction(CHECK_EMOJI)
            await ctx.author.send(f"Yay!! You made it! Welcome to IIITB discord community!")
        else:
            await ctx.message.add_reaction(CROSS_EMOJI)
            await ctx.author.send(f"Sorry, couldn't verify.\nTry again!")
            

    @commands.command(name="feature-request",help="Feature request.")
    async def request(self,ctx,*,feature:str):
        await get(self.bot.get_all_channels(),name=FQ_CHANNEL).send(f"Feature request by {ctx.user.name}.\n\"{feature}\"")
        await ctx.message.add_reaction(CHECK_EMOJI)

def setup(bot):
    bot.add_cog(General(bot))