from discord.ext import commands
from discord.channel import DMChannel
import discord
from __constants import CHECK_EMOJI,UNCHECK_EMOJI,CROSS_EMOJI

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

    @commands.command(name="filter",help="Filters out the unauthorized users.")
    @commands.has_role(ADMIN)
    async def filter(self,ctx):
        if not self.is_in_channel(ctx,SAC_CHANNEL,True):
            ctx.message.add_reaction(CROSS_EMOJI)
            return
        #Filter the DB and return the unverified users list
        await ctx.message.add_reaction(CHECK_EMOJI)

    @commands.command(name="filter-remove",help="Filters out the unauthorized users and removes them from the server.")
    @commands.has_role(ADMIN)
    async def filter_remove(self,ctx):
        if not self.is_in_channel(ctx,SAC_CHANNEL,False):
            ctx.message.add_reaction(CROSS_EMOJI)
            return
        #Remove the filtered users from DB.
        # Add them to the unauth
        await ctx.message.add_reaction(CHECK_EMOJI)

    @commands.command(name="ban",help="Bans the specified user from the server.")
    @commands.has_role(ADMIN)
    async def ban(self,ctx,member:discord.User=None,reason=None):
        if not self.is_in_channel(ctx,SAC_CHANNEL,False):
            ctx.message.add_reaction(CROSS_EMOJI)
            return
        if member==None or member==ctx.message.author:
            await ctx.send("You cannot ban yourself.")
            await ctx.message.add_reaction(UNCHECK_EMOJI)
            return
        await member.send(f"You have been banned from {ctx.guild.name}. Contact SAC.")
        await ctx.message.add_reaction(CHECK_EMOJI)
        return

    @commands.command(name="kick",help="Kicks out the specified user from the server.")
    @commands.has_role(ADMIN)
    async def kick(self,ctx,member:discord.User=None,reason=None):
        if not self.is_in_channel(ctx,SAC_CHANNEL,False):
            ctx.message.add_reaction(CROSS_EMOJI)
            return
        if member==None or member==ctx.message.author:
            await ctx.send("You cannot kick out yourself.")
            return
        await ctx.message.add_reaction(CHECK_EMOJI)
        await member.send(f"You have been kicked out from {ctx.guild.name}. Contact SAC.")


def setup(bot):
    bot.add_cog(Admin(bot))