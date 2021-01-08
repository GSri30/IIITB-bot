#discord
from discord.ext import commands
from discord.channel import DMChannel
import discord
#constants
from __constants import CHECK_EMOJI,UNCHECK_EMOJI,CROSS_EMOJI,MAIL_EMOJI,NON_STUDENT_MAILS
#secret
from cogs.secret import ADMIN,SAC_CHANNEL,REGISTRATION_CHANNEL,NEWBIE
#mail
from smtp import smtp
#encryption
from Bcrypt import Bcrypt
#database
from Database import sqlite


#Admin cog
class Admin(commands.Cog,name="Admin Cog"):
    def __init__(self,bot):
        self.bot=bot

    def is_in_channel(self,ctx,channel_id):
        return (channel_id and (str(ctx.message.channel.id) == str(channel_id)))

    def is_a_DM(self,ctx):
        return isinstance(ctx.channel,DMChannel)

    @commands.command(name="register",help="Registers a user using their IIIT-B domain mail id.")
    async def register(self,ctx,*arguments):

        if (not self.is_in_channel(ctx,REGISTRATION_CHANNEL)) or self.is_a_DM(ctx):
            await ctx.message.add_reaction(CROSS_EMOJI)
            return

        await ctx.message.add_reaction(CHECK_EMOJI)

        sentmails=0
        success=""
        failed=""
        summary=""
        registered=""

        db=sqlite.SQLite()
        db.Connect()
        
        for mailID in arguments:
            mailID=mailID.lower()

            if (not smtp.validMail(mailID.lower())) or (mailID in NON_STUDENT_MAILS):
                failed+=f"{mailID}\n"
                continue
                
            isPresent=db.isPresent(mailID)
            isVerified=db.isVerified(None,mailID)

            if isPresent and isVerified:
                registered+=f"{mailID}\n"
                continue

            Key=Bcrypt.GeneratePassword()
            KeyHash=Bcrypt.Hash(Key)

            if isPresent and (not isVerified):
                db.RemoveUser(mailID)
            
            db.AddUser(mailID,KeyHash)
           
            smtp.send_mail(mailID,Key)

            success+=f"{mailID}\n"

            sentmails+=1
            
        summary+=f"{MAIL_EMOJI} Successfully sent {sentmails} mail(s).\n\n"

        if success:
            summary+=(
                    f"{CHECK_EMOJI} Successfully sent mails to : \n"
                    f"{success}\n"
                    )
        if failed:
            summary+=(
                    f"{CROSS_EMOJI} Failed sending mails to : \n"
                    f"{failed}\n"
                    )
        if registered:
            summary+=(
                    f"{UNCHECK_EMOJI} Found few already registered mails : (skipped them)\n"
                    f"{registered}\n"
                    )
        
        await ctx.send(summary)

        db.Close()




    #filter---> all users who have @newbie role

    @commands.command(name="filter-remove",help="Filters out the unauthorized users and removes them from the server.")
    @commands.has_role(ADMIN)
    async def filter_remove(self,ctx):
        if self.is_a_DM(ctx):
            ctx.message.add_reaction(CROSS_EMOJI)
            return     
        
        summary="Successfully kicked out member(s) : \n"

        for member in ctx.guild.members:
            for role in member.roles:
                if str(role.name) == str(NEWBIE):
                    await member.send(f"You have been kicked out from {ctx.guild.name}. Contact admins.")
                    summary+=f"{str(member)}\n"
                    await ctx.guild.kick(member)
            
        await ctx.message.add_reaction(CHECK_EMOJI)
        await ctx.send(summary)


    @commands.command(name="ban",help="Bans the specified user from the server.")
    @commands.has_role(ADMIN)
    async def ban(self,ctx,member:discord.User=None,reason=None):
        if self.is_a_DM(ctx):
            ctx.message.add_reaction(CROSS_EMOJI)
            return

        if member is None or member==ctx.message.author:
            await ctx.message.add_reaction(CROSS_EMOJI)
            await ctx.send("You cannot ban yourself.")
            return

        await ctx.message.add_reaction(CHECK_EMOJI)
        await member.send(f"You have been banned from {ctx.guild.name}. Contact admins.")
        await ctx.guild.ban(member)
        return

    @commands.command(name="kick",help="Kicks out the specified user from the server.")
    @commands.has_role(ADMIN)
    async def kick(self,ctx,member:discord.User=None,reason=None):
        if self.is_a_DM(ctx):
            ctx.message.add_reaction(CROSS_EMOJI)
            return

        if member is None or member==ctx.message.author:
            await ctx.message.add_reaction(CROSS_EMOJI)
            await ctx.send("You cannot kick out yourself.")
            return
        
        await ctx.message.add_reaction(CHECK_EMOJI)
        await member.send(f"You have been kicked out from {ctx.guild.name}. Contact admins.")
        await ctx.guild.kick(member)


    @commands.has_role(ADMIN)
    @commands.command(name="exceldb",help="Gives the database list in an excel sheet form.")
    async def ExcelForm(self,ctx):
        db=sqlite.SQLite()
        db.Connect()
        ok=db.GenerateCSV()

        if ok:
            await ctx.message.add_reaction(CHECK_EMOJI)
            await ctx.send(file=discord.File(sqlite.EXCEL_PATH))
            db.DeleteCSV()
            db.Close()
            return

        db.Close()
        await ctx.message.add_reaction(CROSS_EMOJI)


def setup(bot):
    bot.add_cog(Admin(bot))