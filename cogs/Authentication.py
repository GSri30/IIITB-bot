#discord
from discord.ext import commands
from discord.utils import get
from discord.channel import DMChannel
#embeds
from cogs.Embeds import Embeds
#constants
from __constants import CHECK_EMOJI,GREETINGS,_GREETINGS
#database
from Database import sql
#secret
from secret import GUILD,WELCOME_CHANNEL,NEWBIE
#other
import random


class Authentication(commands.Cog,name="Authentication Cog"):
    def __init__(self,bot):
        self.bot=bot
    
    def is_in_channel(self,ctx,channel_id):
        return (channel_id and (str(ctx.message.channel.id) == str(channel_id))) 
        
    def is_a_DM(self,ctx):
        return isinstance(ctx.channel,DMChannel)

    def is_a_newbie(self,ctx):
        ok=get(ctx.author.roles,name=NEWBIE)
        return ok is not None

    @commands.cooldown(3,30,commands.BucketType.user)
    @commands.command(name="verify",help="Verifies the user email using an associated auto generated key.")
    @commands.dm_only()
    async def verify(self,ctx,emailID:str,key:str):
        
        async with ctx.typing():
            ok=get(get(get(self.bot.guilds,name=GUILD).members,id=int(ctx.author.id)).roles,name=NEWBIE)
       
        if not ok:
            await ctx.send(f"<@{ctx.author.id}> You are already verified and assigned once afaik. Contact admins if I'm wrong.")
            return

        async with ctx.typing():
            db=sql.SQL()
            db.Connect()

            isPresent=db.isPresent(emailID)
            isVerified=db.isVerified(None,emailID)

        await ctx.message.add_reaction(CHECK_EMOJI)

        if not isPresent:
            db.Close()
            await ctx.send(f"<@{ctx.message.author.id}> '{emailID}' is not registered. Contact admins.")
            return

        if isVerified:
            batch=db.getBatch(emailID)
            db.Close()
            
            guild=get(self.bot.guilds,name=GUILD)
            members=guild.members
            roles=guild.roles
            role_obj=get(roles,name=batch)
            user_obj=get(members,name=ctx.author.name)
            
            await ctx.send(f"<@{ctx.message.author.id}> '{emailID}' is already verified successfully! You have been given {batch} role again. Welcome back!. :smile: ")
            await user_obj.add_roles(role_obj)
            await user_obj.remove_roles(get(roles,name=NEWBIE))
            return

        async with ctx.typing():
            ok=db.VerifyUser(str(ctx.message.author),ctx.message.author.id,emailID,key)
        
        if ok:
            async with ctx.typing():
                batch=db.getBatch(emailID)
            db.Close()
            await ctx.send(f"<@{ctx.author.id}> Yay!! You have been verified successfully and given {batch} role!")
            intro=Embeds.IntroEmbed(self.bot,str(ctx.message.author),emailID,str(ctx.message.author.id))
            await ctx.author.send(embed=intro)

            guild=get(self.bot.guilds,name=GUILD)
            members=guild.members
            roles=guild.roles
            role_obj=get(roles,name=batch)
            user_obj=get(members,name=ctx.author.name)

            await user_obj.add_roles(role_obj)
            await user_obj.remove_roles(get(roles,name=NEWBIE))

            greeting=random.choice(GREETINGS).replace(_GREETINGS, f"<@{ctx.author.id}>")
            await get(guild.channels,id=int(WELCOME_CHANNEL)).send(greeting)

            return

        db.Close()
        await ctx.send(f"<@{ctx.author.id}> Sorry, couldn't verify you.\nTry again.")


    # Modify command to assign to a club

    # @commands.cooldown(3,30,commands.BucketType.user)
    # @commands.command(name="assign",help="Helps you to assign a suitable role for yourself to view the channels.")
    # @commands.dm_only()
    # async def assign(self,ctx,role:str):
    
    #     async with ctx.typing():
    #         ok=get(get(get(self.bot.guilds,name=GUILD).members,id=int(ctx.author.id)).roles,name=NEWBIE)
       
    #     if not ok:
    #         await ctx.send(f"<@{ctx.author.id}> You are already verified and assigned once afaik. Contact admins if I'm wrong.")
    #         return

    #     async with ctx.typing():
    #         guild=get(self.bot.guilds,name=GUILD)
    #         members=guild.members
    #         roles=guild.roles
    #         role_obj=get(roles,name=role)
    #         user_obj=get(members,name=ctx.author.name)

    #     await ctx.message.add_reaction(CHECK_EMOJI)

    #     if (not role_obj) or (not (role in ROLES)):
    #         await ctx.send(f"<@{ctx.author.id}> Enter a valid role.")
    #         return
        
    #     #Can omit this line as discord itself handles this case while using a bot
    #     if not user_obj:
    #         await ctx.send(f"<@{ctx.author.id}> Cannot find you on the server. Re-check if you have joined.")
    #         return

    #     async with ctx.typing():
    #         db=sql.SQL()
    #         db.Connect()
    #         isVerified=db.isVerified(ctx.author.id,None)

    #     if isVerified:
    #         await ctx.author.send("Rock on!")

    #         await user_obj.add_roles(role_obj)
    #         await user_obj.remove_roles(get(roles,name=NEWBIE))

    #         greeting=random.choice(GREETINGS).replace(_GREETINGS, f"<@{ctx.author.id}>")
    #         await get(guild.channels,id=int(WELCOME_CHANNEL)).send(greeting)
            
    #         db.Close()
    #         return

    #     db.Close()
    #     await ctx.send(f"<@{ctx.author.id}> :joy: Don't trick me. Verify first.")
    #     async with ctx.typing():
    #         await asyncio.sleep(1.5)
    #     await ctx.send(f"<@{ctx.author.id}> Wait! Think you are already verified? Re-check using !verify command. :confused:\nTip : You can only use the same discord account from which you verified your Mail ID.")

    @commands.command(name="leave",help="Removes you from server and also from the mapping")
    @commands.dm_only()
    async def leave(self,ctx):
        async with ctx.typing():
            db=sql.SQL()
            db.Connect()
            db.RemoveUser(memberID=ctx.author.id)
            db.Close()

        await ctx.send("Hope you had a great time with us. Hope to see you again in the server. Bye! :smile:")

        await get(self.bot.guilds,name=GUILD).kick(ctx.author,reason=f"{ctx.author} used leave command.")


def setup(bot):
    bot.add_cog(Authentication(bot))