#discord
from discord.ext import commands
from discord.channel import DMChannel
from discord.utils import get
import discord
#constants
from __constants import CHECK_EMOJI,UNCHECK_EMOJI,CROSS_EMOJI,MAIL_EMOJI,NON_STUDENT_MAILS,LIKE_EMOJI
#secret
from secret import ADMIN,REGISTRATION_CHANNEL,NEWBIE,RULES_CHANNEL
#mail
from smtp import smtp
#encryption
from Bcrypt import Bcrypt
#database
from Database import sql
#other
from datetime import datetime
#OAuth
import base64,pickle,requests
#Settings
from settings import OAUTH_URL,SUMMARY_PATH
# Excel Utils
import requests
import asyncio
import os

#Admin cog
class Admin(commands.Cog,name="Admin Cog"):
    def __init__(self,bot):
        self.bot=bot

    def is_in_channel(self,ctx,channel_id):
        return (channel_id and (str(ctx.message.channel.id) == str(channel_id)))

    def is_a_DM(self,ctx):
        return isinstance(ctx.channel,DMChannel)

    def is_a_newbie(self,ctx):
        ok=discord.utils.get(ctx.author.roles,name=NEWBIE)
        return ok is not None
       

    @commands.command(name="register-excel")
    @commands.has_role(ADMIN)
    async def register_excel(self,ctx,batch:str):
        if not self.is_in_channel(ctx,REGISTRATION_CHANNEL):
            await ctx.send("Please do this stuff in registration channel.")
            return

        if not get(ctx.guild.roles,name=batch):
            await ctx.send("Enter a valid batch role. (case-sensitive)")
            return

        await ctx.send(f"<@{ctx.author.id}> Upload the csv file within 60 sec. Enter 'n' (without quotes) to cancel.")

        def check(msg):
            if(msg.author==ctx.author and msg.channel==ctx.channel):
                if (msg.content.lower()=="n" or len(msg.attachments)>0):
                    return True
            return False 
        
        try:
            msg=await self.bot.wait_for('message',check=check,timeout=60)
            if(msg.content=="n"):
                await msg.add_reaction(LIKE_EMOJI)
                return
            attachment=msg.attachments[0]
            file=requests.get(attachment,stream=True)
            students=[]
            for line in file.iter_lines():
                students.append(line.decode('utf-8'))
            await msg.add_reaction(LIKE_EMOJI)
            await self.send_mails(ctx,batch,students)
        except asyncio.exceptions.TimeoutError:
            await ctx.send(f"<@{ctx.author.id}> Sorry, you didn't upload any csv file within 60sec. Aborted.")
            return

    async def send_mails(self,ctx,batch,students):
        async with ctx.typing():

            success=[]
            failed=[]
            registered=[]

            db=sql.SQL()
            db.Connect()
            
            smtp_object=smtp.SMTP()

            for mailID in students:
                mailID=mailID.lower()

                if (not smtp.SMTP.validMail(mailID.lower())) or (mailID in NON_STUDENT_MAILS):
                    failed.append(mailID)
                    continue
                    
                isPresent=db.isPresent(mailID)
                isVerified=db.isVerified(None,mailID)

                if isPresent and isVerified:
                    registered.append(mailID)
                    continue

                Key=Bcrypt.GeneratePassword()
                KeyHash=Bcrypt.Hash(Key)

                if isPresent and (not isVerified):
                    db.RemoveUser(mailID=mailID)
                
                db.AddUser(mailID,batch,str(datetime.now().year),KeyHash)

                stateObj={'emailID':mailID,'key':Key,'batch':batch}
                state=base64.urlsafe_b64encode(pickle.dumps(stateObj)).decode('utf-8');
                url=f"{OAUTH_URL}&state={state}"

                smtp_object.send_mail(mailID,Key,url)
                success.append(mailID)

            successLen=len(success)
            failedLen=len(failed)
            registeredLen=len(registered)

            with open(SUMMARY_PATH,'w') as f:
                f.write("Success,Failed,Already Registered\n")
                for i in range(max([successLen,failedLen,registeredLen])):
                    if i<successLen:
                        f.write(f"{success[i]},")
                    else:
                        f.write(',')
                    if i<failedLen:
                        f.write(f"{failed[i]},")
                    else:
                        f.write(',')
                    if i<registeredLen:
                        f.write(registered[i])
                    f.write('\n')

        smtp_object.quit()

        await ctx.message.add_reaction(CHECK_EMOJI)

        await ctx.send(file=discord.File(SUMMARY_PATH))

        os.remove(SUMMARY_PATH)

        db.Close()

    @commands.command(name="register",help="Registers a user using their IIIT-B domain mail id.")
    @commands.has_role(ADMIN)
    async def register(self,ctx,batch:str,*arguments):
        
        if not self.is_in_channel(ctx,REGISTRATION_CHANNEL):
            await ctx.message.add_reaction(CROSS_EMOJI)
            return

        if not get(ctx.guild.roles,name=batch):
            await ctx.send("Enter a valid batch role. (case-sensitive)")
            return

        async with ctx.typing():

            sentmails=0
            success=""
            failed=""
            summary=""
            registered=""

            db=sql.SQL()
            db.Connect()
            
            smtp_object=smtp.SMTP()

            for mailID in arguments:
                mailID=mailID.lower()

                if (not smtp.SMTP.validMail(mailID.lower())) or (mailID in NON_STUDENT_MAILS):
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
                    db.RemoveUser(mailID=mailID)
                
                db.AddUser(mailID,batch,str(datetime.now().year),KeyHash)

                stateObj={'emailID':mailID,'key':Key,'batch':batch}
                state=base64.urlsafe_b64encode(pickle.dumps(stateObj)).decode('utf-8');
                url=f"{OAUTH_URL}&state={state}"

                smtp_object.send_mail(mailID,Key,url)

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
        
        smtp_object.quit()

        await ctx.message.add_reaction(CHECK_EMOJI)

        await ctx.send(summary)

        db.Close()


    @commands.command(name="un-register",help="Un-registers a user using their IIIT-B domain mail id.")
    @commands.has_role(ADMIN)
    async def un_register(self,ctx,mailID:str):
        if not self.is_in_channel(ctx,REGISTRATION_CHANNEL):
            await ctx.message.add_reaction(CROSS_EMOJI)
            return

        async with ctx.typing():
            db=sql.SQL()
            db.Connect()
            db.RemoveUser(mailID=mailID)
            db.Close()
            await ctx.message.add_reaction(CHECK_EMOJI)


    #filter---> all users who have @newbie role

    @commands.command(name="filter-ban",help="Filters out the unauthorized users and bans them from the server.")
    @commands.has_role(ADMIN)
    async def filter_ban(self,ctx):
        
        summary="Successfully banned member(s) : \n"

        async with ctx.typing():
            for member in ctx.guild.members:
                ok=discord.utils.get(member.roles,name=NEWBIE)
                if ok:
                    await member.send(f"<@{member.id}> You have been banned from {ctx.guild.name}. Contact admins.")
                    summary+=f"{str(member)}\n"
                    await ctx.guild.ban(member,reason=f"{ctx.author} used filter ban.")

        await ctx.message.add_reaction(CHECK_EMOJI)
        await ctx.send(summary)


    @commands.command(name="filter-kick",help="Filters out the unauthorized users and kicks them out from the server.")
    @commands.has_role(ADMIN)
    async def filter_kick(self,ctx): 
        
        summary="Successfully kicked out member(s) : \n"

        async with ctx.typing():
            for member in ctx.guild.members:
                ok=discord.utils.get(member.roles,name=NEWBIE)
                if ok:
                    await member.send(f"<@{member.id}> You have been kicked out from {ctx.guild.name}. Contact admins.")
                    summary+=f"{str(member)}\n"
                    await ctx.guild.kick(member,reason=f"{ctx.author} used filter kick.")
            
        await ctx.message.add_reaction(CHECK_EMOJI)
        await ctx.send(summary)


    @commands.command(name="ban",help="Bans the specified user from the server.")
    @commands.has_role(ADMIN)
    async def ban(self,ctx,member:discord.User=None,reason=None):
       
        if member is None or member==ctx.message.author:
            await ctx.message.add_reaction(CROSS_EMOJI)
            await ctx.send("You cannot ban yourself.")
            return

        async with ctx.typing():
            await member.send(f"<@{member.id}> You have been banned from {ctx.guild.name}. Contact admins.")
            await ctx.guild.ban(member,reason=f"{ctx.author} used ban command.")
            
            db=sql.SQL()
            db.Connect()
            db.RemoveUser(memberID=member.id)
            db.Close()

        await ctx.message.add_reaction(CHECK_EMOJI)

    @commands.command(name="kick",help="Kicks out the specified user from the server.")
    @commands.has_role(ADMIN)
    async def kick(self,ctx,member:discord.User=None,reason=None):
        
        if member is None or member==ctx.message.author:
            await ctx.message.add_reaction(CROSS_EMOJI)
            await ctx.send("You cannot kick out yourself.")
            return

        async with ctx.typing():    
            await member.send(f"<@{member.id}> You have been kicked out from {ctx.guild.name}. Contact admins.")
            await ctx.guild.kick(member,reason=f"{ctx.author} used kick command.")

            db=sql.SQL()
            db.Connect()
            db.RemoveUser(memberID=member.id)
            db.Close()
        
        await ctx.message.add_reaction(CHECK_EMOJI)


    @commands.command(name="count-role",help="Returns the count of members of specified role in the server.")
    @commands.has_role(ADMIN)
    async def count_role(self,ctx,role:str):
        
        async with ctx.typing():
            ok=discord.utils.get(ctx.guild.roles,name=role)
        
        if not ok:
            await ctx.message.add_reaction(CROSS_EMOJI)
            await ctx.send("Enter a valid role.")
            return

        async with ctx.typing():
            count=0
            summary=f"Total count of {role} : "
            for member in ctx.guild.members:
                for r in member.roles:
                    if str(r.name) == role:
                        count+=1
                
            summary+=str(count)

        await ctx.message.add_reaction(CHECK_EMOJI)
        await ctx.send(summary)


    @commands.command(name="roles",help="Returns the list of server roles")
    @commands.has_role(ADMIN)
    async def roles(self,ctx):
        rls=""
        for role in ctx.guild.roles:
            rls+=f"{role.name}\n"
        await ctx.send(rls)


    @commands.command(name="list",help="Gives the database list in an excel sheet form.")
    @commands.has_role(ADMIN)
    async def ExcelForm(self,ctx):
        async with ctx.typing():
            db=sql.SQL()
            db.Connect()
            ok=db.GenerateCSV()

        if ok:
            await ctx.message.add_reaction(CHECK_EMOJI)
            await ctx.send(file=discord.File(sql.EXCEL_PATH))
            db.DeleteCSV()
            db.Close()
            return

        await ctx.message.add_reaction(CROSS_EMOJI)
        db.Close()


    @commands.command(name="update-roles",help="Assigns 'role 2' to all the members having 'role 1'.")
    @commands.has_role(ADMIN)
    async def UpdateRoles(self,ctx,Role1:str,Role2:str):
        if self.is_a_DM(ctx):
            await ctx.message.add_reaction(CROSS_EMOJI)
            return
        
        async with ctx.typing():
            obj1=discord.utils.get(ctx.guild.roles,name=Role1)
            obj2=discord.utils.get(ctx.guild.roles,name=Role2)

        if obj1 is None:
            await ctx.message.add_reaction(CROSS_EMOJI)
            await ctx.send("Enter a valid role 1.")
            return

        if obj2 is None:
            await ctx.message.add_reaction(CROSS_EMOJI)
            await ctx.send("Enter a valid role 2.")
            return

        async with ctx.typing():
            count=0
            for member in ctx.guild.members:
                ok=discord.utils.get(member.roles,name=Role1)
                if ok:
                    await member.add_roles(obj2)
                    count+=1
        
        # As a sub-process, we also remove old alumni of below CURRENT_YEAR-DELTA_YEAR seniority
        async with ctx.typing():
            count=0
            db=sql.SQL()
            db.Connect()
            results=db.filterOldAlumni(str(datetime.now().year))
            if results is not None:
                for alumniID in results:
                    alumni=discord.utils.get(ctx.guild.members,id=int(alumniID))
                    alumni.send("Will miss you! All the best from IIIT-B community!\n")
                    ctx.guild.kick(alumni,reason="Old Alumni")
                    count+=1
            db.Close()

        await ctx.message.add_reaction(CHECK_EMOJI)
        await ctx.send(f"Updated roles of {count} member(s) and removed {count} Old Alumni successfully!")


    @commands.command(name="sync-permissions",help="Helps to sync the most important permissions required for authentication functioning.")
    @commands.has_role(ADMIN)
    async def sync_permissions(self,ctx):
        await ctx.send(f"<@{ctx.author.id}> Okay. Will notify once I'm done.")
        newbie=get(ctx.guild.roles,name=NEWBIE)
        for channel in ctx.guild.channels:
            if int(channel.id)==int(RULES_CHANNEL):
                continue
            await channel.set_permissions(newbie,view_channel=False,attach_files=False,send_messages=False,send_tts_messages=False)
        
        await ctx.message.add_reaction(CHECK_EMOJI)
        await ctx.send(f"<@{ctx.author.id}> Done.")


def setup(bot):
    bot.add_cog(Admin(bot))