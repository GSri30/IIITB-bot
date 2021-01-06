from cogs.Greetings import NEWBIE
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
WELCOME_CHANNEL=getenv("WELCOME")


class General(commands.Cog,name="General Cog"):
    def __init__(self,bot):
        self.bot=bot
    
    def is_in_channel(self,ctx,channel_id):
        return (channel_id and (str(ctx.message.channel.id) == str(channel_id))) 
        
    def is_a_DM(self,ctx):
        return isinstance(ctx.channel,DMChannel)

    def store_in_db(self,ctx,mail:str,Hash:str):
        db=sqlite.SQLite()
        if db.Connect() and db.AddStudent(ctx.author.name,ctx.author.id,mail,Hash):
            db.Close()
            return True
        return False

    @commands.command(name="register",help="Registers a user using their IIIT-B domain mail id.")
    async def register(self,ctx, mailID:str):
        mailID=mailID.lower()
        if (not self.is_in_channel(ctx,AUTH_CHANNEL)) or self.is_a_DM(ctx):
            await ctx.message.add_reaction(CROSS_EMOJI)
            return
        if not smtp.validMail(mailID.lower()):
            await ctx.message.add_reaction(CROSS_EMOJI)
            await ctx.author.send(f"Wrong email entered. Try again!\nNOTE : Use only college mail ID.")
            return
        if mailID in NON_STUDENT_MAILS:
            await ctx.message.add_reaction(CROSS_EMOJI)
            await ctx.author.send(f"You can only use a student mail ID!")
            return
        
        db=sqlite.SQLite()
        db.Connect()
        if db.isVerified(ctx.author.id,mailID):
            await ctx.message.add_reaction(CHECK_EMOJI)
            await ctx.send(f"<@{ctx.message.author.id}> Welcome back to the server again! You can directly proceed to <#{ASSIGN_CHANNEL}>. :smile:")
            #await ctx.author.remove_roles(get(ctx.guild.roles,name=NEWBIE))
            db.Close()
            return

        Key=Bcrypt.GeneratePassword()
        KeyHash=Bcrypt.Hash(Key)

        if db.isPresentUnverified(ctx.author.id,mailID):
            db.RemoveUser(ctx.author.id,mailID)
        
        db.AddUser(ctx.author.name,ctx.author.id,mailID,KeyHash)
        db.Close()
        await ctx.message.add_reaction(CHECK_EMOJI)
        await ctx.send(f"{mailID} has been successfully mapped to <@{ctx.message.author.id}>. Check your :email: to proceed further!")
        smtp.send_mail(mailID,Key)
        

    @commands.command(name="verify",help="Verifies the user email using an associated auto generated key.")
    async def verify(self,ctx,key:str):
        if (not self.is_in_channel(ctx,AUTH_CHANNEL)) or self.is_a_DM(ctx):
            await ctx.message.add_reaction(CROSS_EMOJI)
            return
        db=sqlite.SQLite()
        db.Connect()
        if db.VerifyUser(ctx.author.id,key):
            #await ctx.author.remove_roles(get(ctx.guild.roles,name=NEWBIE))
            db.Close()
            await ctx.message.add_reaction(CHECK_EMOJI)
            await ctx.send(f"<@{ctx.author.id}> You have been verified successfully! Check my DM.")
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
            return

        db.Close()
        await ctx.message.add_reaction(CROSS_EMOJI)
        await ctx.send(f"<@{ctx.author.id}> Sorry, couldn't verify you.\nTry again.")


    @commands.command(name="assign",help="Helps you to assign a suitable role for yourself to view the channels.")
    async def assign(self,ctx,role:str):
        if (not self.is_in_channel(ctx,ASSIGN_CHANNEL)) or self.is_a_DM(ctx):
            await ctx.message.add_reaction(CROSS_EMOJI)
            return
        role=role.lower()
        roleObj=get(ctx.guild.roles,name=role)
        db=sqlite.SQLite()
        db.Connect()
        if (role in ROLES) and roleObj and db.isVerified(ctx.author.id):
            await ctx.message.add_reaction(CHECK_EMOJI)
            await ctx.author.add_roles(roleObj)
            await ctx.author.remove_roles(get(ctx.guild.roles,name=NEWBIE))
            await get(ctx.guild.channels,name=WELCOME_CHANNEL).send(f"Welcome <@{ctx.author.id}>.")
            db.Close()
            return
        db.Close()
        await ctx.message.add_reaction(CROSS_EMOJI)

    @commands.command(name="feature-request",help="Send a feature request to the admins. (non-anonymous request)")
    async def request(self,ctx,*,feature:str):
        await get(self.bot.get_all_channels(),name=FQ_CHANNEL).send(f"Feature request by {ctx.user.name}.\n\"{feature}\"")
        await ctx.message.add_reaction(CHECK_EMOJI)

def setup(bot):
    bot.add_cog(General(bot))