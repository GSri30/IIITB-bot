import re
from discord.ext import commands
from discord.utils import get,find
from discord.channel import DMChannel
from __constants import CHECK_EMOJI,UNCHECK_EMOJI,CROSS_EMOJI,RIGHT_ARROW,REGEX,DOMAIN,NON_STUDENT_MAILS,ROLES
from Bcrypt import Bcrypt
from smtp import smtp

from Database import sqlite

from os import getenv,path
from dotenv import load_dotenv
load_dotenv()
AUTH_CHANNEL=getenv("AUTH")
FQ_CHANNEL=getenv("FEATUREREQ")
ASSIGN_CHANNEL=getenv("ASSIGN")


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
        db=sqlite.SQLite()
        if db.Connect() and db.AddStudent(ctx.author.name,ctx.author.id,mail,Hash):
            db.Close()
            return True
        return False

    @commands.command(name="register",help="Registers a user using their IIIT-B domain mail id.")
    async def register(self,ctx, mailID:str):
        mailID=mailID.lower()
        if not self.is_in_channel(ctx,AUTH_CHANNEL,False):
            await ctx.message.add_reaction(CROSS_EMOJI)
            return
        if not self.validMail(mailID.lower()):
            await ctx.author.send(f"Wrong email entered. Try again!\nNOTE : Use only college mail ID.")
            await ctx.message.add_reaction(CROSS_EMOJI)
            return
        if mailID in NON_STUDENT_MAILS:
            await ctx.author.send(f"You can only use a student mail ID!")
            await ctx.message.add_reaction(CROSS_EMOJI)
            return
        
        Key=Bcrypt.GeneratePassword()
        Hashed=Bcrypt.Hash(Key)

        if self.store_in_db(ctx,mailID,Hashed):
            ctx.message.add_reaction(CHECK_EMOJI)
            await ctx.author.send(f"{mailID} has been successfully mapped for you. Check your :email: to proceed further!")
            smtp.send_mail(mailID,Key)
            return
        await ctx.message.add_reaction(CROSS_EMOJI)
        
    @commands.command(name="verify",help="Verifies the user email using an associated auto generated key.")
    async def verify(self,ctx,key:str):
        if not self.is_in_channel(ctx,AUTH_CHANNEL,True):
            await ctx.message.add_reaction(CROSS_EMOJI)
            return
        db=sqlite.SQLite()
        if db.Connect() and db.VerifyUser(ctx.author.id,Bcrypt.Hash(key)):
            db.Close()
            await ctx.message.add_reaction(CHECK_EMOJI)
            await ctx.author.send(f"Yay!! You made it! Welcome to IIITB discord community!")
            await ctx.author.send(f"As a last step, assign yourself a suitable role @ <#{ASSIGN_CHANNEL}> to view all the channels! :smile:\n\n"
                                    f"{RIGHT_ARROW}: scholars\n\n"
                                    f"{RIGHT_ARROW}: imt2016\n\n"
                                    f"{RIGHT_ARROW}: imt2017\n\n"
                                    f"{RIGHT_ARROW}: imt2018\n\n"
                                    f"{RIGHT_ARROW}: mt2019\n\n"
                                    f"{RIGHT_ARROW}: dt2019\n\n"
                                    f"{RIGHT_ARROW}: imt2019\n\n"
                                    f"{RIGHT_ARROW}: mt2020\n\n"
                                    f"{RIGHT_ARROW}: dt2020\n\n"
                                    f"{RIGHT_ARROW}: imt2020\n\n"
                                    f"You can use !assign command for the same!\n"
                                    f"Example : !assign imt2020"
                                )
        else:
            await ctx.message.add_reaction(CROSS_EMOJI)
            await ctx.author.send(f"Sorry, couldn't verify.\nTry again!")


    @commands.command(name="assign",help="Helps you to assign a suitable role for yourself to view the channels.")
    async def assign(self,ctx,role:str):
        if isinstance(ctx.channel,DMChannel) or (str(ctx.message.channel.id) != str(ASSIGN_CHANNEL)):
            await ctx.message.add_reaction(CROSS_EMOJI)
            await ctx.author.send(f"Hey! not here! Head over to <#{ASSIGN_CHANNEL}>")
            return
        role=role.lower()
        roleObj=get(ctx.guild.roles,name=role)
        db=sqlite.SQLite()
        if (role in ROLES) and roleObj and db.Connect() and db.isVerified("dkkskfn2k5nk2nk"):
            await ctx.author.add_roles(roleObj)
            await ctx.message.add_reaction(CHECK_EMOJI)
            db.Close()
            return
        await ctx.message.add_reaction(CROSS_EMOJI)

    @commands.command(name="feature-request",help="Feature request.")
    async def request(self,ctx,*,feature:str):
        await get(self.bot.get_all_channels(),name=FQ_CHANNEL).send(f"Feature request by {ctx.user.name}.\n\"{feature}\"")
        await ctx.message.add_reaction(CHECK_EMOJI)

def setup(bot):
    bot.add_cog(General(bot))