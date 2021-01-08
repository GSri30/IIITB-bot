#discord
from discord.ext import commands
from discord.utils import get
from discord.channel import DMChannel
#constants
from __constants import CHECK_EMOJI,CROSS_EMOJI,RIGHT_ARROW,ROLES
#database
from Database import sqlite
#secret
from cogs.secret import VERIFICATION_CHANNEL,ASSIGN_CHANNEL,WELCOME_CHANNEL,DEVELOPERS_CHANNEL,NEWBIE


#General Cog
class General(commands.Cog,name="General Cog"):
    def __init__(self,bot):
        self.bot=bot
    
    def is_in_channel(self,ctx,channel_id):
        return (channel_id and (str(ctx.message.channel.id) == str(channel_id))) 
        
    def is_a_DM(self,ctx):
        return isinstance(ctx.channel,DMChannel)

    def channelObj(self,ctx,channel:str):
        obj=None
        for c in ctx.guild.channels:
            if str(c.id) == channel:
                obj=c
                break
        return obj
        

    @commands.command(name="verify",help="Verifies the user email using an associated auto generated key.")
    async def verify(self,ctx,emailID:str,key:str):
        if (not self.is_in_channel(ctx,VERIFICATION_CHANNEL)) or self.is_a_DM(ctx):
            await ctx.message.add_reaction(CROSS_EMOJI)
            return
        
        db=sqlite.SQLite()
        db.Connect()
        
        await ctx.message.add_reaction(CHECK_EMOJI)

        isPresent=db.isPresent(emailID)
        isVerified=db.isVerified(None,emailID)

        if not isPresent:
            db.Close()
            await ctx.send(f"<@{ctx.message.author.id}> {emailID} is not registered. Contact admins.")
            return

        if isVerified:
            db.Close()
            await ctx.send(f"<@{ctx.message.author.id}> {emailID} is already verified successfully! You can directly proceed to <#{ASSIGN_CHANNEL}>. :smile: ")
            return

        ok=db.VerifyUser(str(ctx.message.author),ctx.message.author.id,emailID,key)
        
        if ok:
            db.Close()
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
        await ctx.send(f"<@{ctx.author.id}> Sorry, couldn't verify you.\nTry again.")


    @commands.command(name="assign",help="Helps you to assign a suitable role for yourself to view the channels.")
    async def assign(self,ctx,role:str):
        role=role.lower()

        if self.is_a_DM(ctx):
            await ctx.message.add_reaction(CROSS_EMOJI)
            await ctx.send(f"Hey not here! Headover to <#{ASSIGN_CHANNEL}> for that.")
            return

        if (not self.is_in_channel(ctx,ASSIGN_CHANNEL)) or not (role in ROLES):
            await ctx.message.add_reaction(CROSS_EMOJI)
            return

        roleObj=get(ctx.guild.roles,name=role)
        db=sqlite.SQLite()
        db.Connect()
        isVerified=db.isVerified(ctx.author.id,None)
        if isVerified:
            await ctx.message.add_reaction(CHECK_EMOJI)
            await ctx.author.add_roles(roleObj)
            await ctx.author.remove_roles(get(ctx.guild.roles,name=NEWBIE))
            await self.channelObj(ctx,WELCOME_CHANNEL).send(f"Welcome <@{ctx.author.id}>.")
            db.Close()
            return

        db.Close()
        await ctx.message.add_reaction(CROSS_EMOJI)

    @commands.command(name="feature-request",help="Send a feature request to the admins. (non-anonymous request)")
    async def request(self,ctx,*,feature:str):
        if self.is_a_DM(ctx):
            await ctx.message.add_reaction(CROSS_EMOJI)
            return
            
        await ctx.message.add_reaction(CHECK_EMOJI)
        await self.channelObj(ctx,DEVELOPERS_CHANNEL).send(f"Feature request by {ctx.message.author.name}.\n\"{feature}\"")
        


def setup(bot):
    bot.add_cog(General(bot))