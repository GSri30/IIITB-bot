from discord.ext import commands
from discord.channel import DMChannel
import discord
from __constants import CHECK_EMOJI,UNCHECK_EMOJI,CROSS_EMOJI

from Database import sqlite

from os import getenv
from dotenv import load_dotenv
load_dotenv()
ADMIN=getenv("ADMIN")
SAC_CHANNEL=getenv("SAC")


class Admin(commands.Cog,name="Admin Cog"):
    def __init__(self,bot):
        self.bot=bot

    def is_in_channel(self,ctx,channel_id,dm_allowed):
        return (channel_id and (str(ctx.message.channel.id) == str(channel_id)) or (dm_allowed and isinstance(ctx.channel,DMChannel)))

    def is_a_DM(self,ctx):
        return isinstance(ctx.channel,DMChannel)

    # @commands.command(name="filter",help="Filters out the unauthorized users.")
    # @commands.has_role(ADMIN)
    # async def filter(self,ctx):
    #     if not self.is_in_channel(ctx,SAC_CHANNEL,True):
    #         db=sqlite.SQLite()
    #         if(db.Connect() and db.UnverifiedUsers()):
    #             await ctx.message.add_reaction(CHECK_EMOJI)
    #             await ctx.send(file=discord.File(sqlite.EXCEL_PATH))
    #             db.DeleteCSV()
    #             db.Close()
    #             return
    #     await ctx.message.add_reaction(UNCHECK_EMOJI)

    # @commands.command(name="filter",help="Filters out the unauthorized users and tags them.")
    # @commands.has_role(ADMIN)
    # async def filter(self,ctx):
    #     if not self.is_in_channel(ctx,SAC_CHANNEL,False):
    #         ctx.message.add_reaction(CROSS_EMOJI)
    #         return
    #     await ctx.message.add_reaction(CHECK_EMOJI)
    #     db=sqlite.SQLite()
    #     db.Connect()
    #     set1=set(db.verified())
    #     print(set1)
    #     set2=set([str(member.id) for member in ctx.message.guild.members])
    #     print(set2)
    #     db.Close()
    #     diff=set2.difference(set1)
    #     if(len(diff)):
    #         message=""
    #         for s in diff:
    #             message+=f"<@{s}>"
    #         await ctx.send(message)
    #         return
    #     await ctx.send("No unverified users in the server!:smile:")


    #filter---> all users who have @newbie role

    @commands.command(name="filter-remove",help="Filters out the unauthorized users and removes them from the server.")
    @commands.has_role(ADMIN)
    async def filter_remove(self,ctx):
        if self.is_a_DM(ctx):
            ctx.message.add_reaction(CROSS_EMOJI)
            return
        db=sqlite.SQLite()
        if(db.Connect()):
            unverifiedlist=db.RemoveUnverified()            
            if unverifiedlist is not None:
                for unverifieduser in unverifiedlist:
                    UserObj = await ctx.guild.fetch_member(unverifieduser[0])
                    await UserObj.send(f"You have been kicked out from {ctx.guild.name}. Contact admins.")
                    await ctx.guild.kick(UserObj)
                await ctx.message.add_reaction(CHECK_EMOJI)
                db.Close()
                return
        await ctx.message.add_reaction(CROSS_EMOJI)

    @commands.command(name="ban",help="Bans the specified user from the server.")
    @commands.has_role(ADMIN)
    async def ban(self,ctx,member:discord.User=None,reason=None):
        if self.is_a_DM(ctx):
            ctx.message.add_reaction(CROSS_EMOJI)
            return
        if member is None or member==ctx.message.author:
            await ctx.send("You cannot ban yourself.")
            await ctx.message.add_reaction(CROSS_EMOJI)
            return
        await member.send(f"You have been banned from {ctx.guild.name}. Contact admins.")
        await ctx.guild.ban(member)
        await ctx.message.add_reaction(CHECK_EMOJI)
        return

    @commands.command(name="kick",help="Kicks out the specified user from the server.")
    @commands.has_role(ADMIN)
    async def kick(self,ctx,member:discord.User=None,reason=None):
        if self.is_a_DM(ctx):
            ctx.message.add_reaction(CROSS_EMOJI)
            return
        if member is None or member==ctx.message.author:
            await ctx.send("You cannot kick out yourself.")
            return
        
        await member.send(f"You have been kicked out from {ctx.guild.name}. Contact admins.")
        await ctx.guild.kick(member)
        await ctx.message.add_reaction(CHECK_EMOJI)

    @commands.has_role(ADMIN)
    @commands.command(name="exceldb",help="Gives the database list in an excel sheet form.")
    async def ExcelForm(self,ctx):
        db=sqlite.SQLite()
        if(db.Connect() and db.GenerateCSV()):
            await ctx.message.add_reaction(CHECK_EMOJI)
            await ctx.send(file=discord.File(sqlite.EXCEL_PATH))
            db.DeleteCSV()
            db.Close()
            return
        await ctx.message.add_reaction(CROSS_EMOJI)

def setup(bot):
    bot.add_cog(Admin(bot))