from discord.ext import commands
import discord

from os import getenv
from dotenv import load_dotenv
load_dotenv()
ADMIN=getenv("ADMIN")
SAC_CHANNEL=getenv("SAC")


class Admin(commands.Cog,name="Admin Cog"):
    def __init__(self,bot):
        self.bot=bot

    @commands.command(name="filter",help="Filters out the unauthorized users.")
    @commands.has_role(ADMIN)
    async def filter(self,ctx):
        if(str(ctx.channel.id)!=SAC_CHANNEL):
            await ctx.send(f"This command cannot be used from here.")
            return
        await ctx.send("Filtered and returned the results!")

    @commands.command(name="filter-remove",help="Filters out the unauthorized users and removes them from the server.")
    @commands.has_role(ADMIN)
    async def filter_remove(self,ctx):
        if(str(ctx.channel.id)!=SAC_CHANNEL):
            await ctx.send(f"This command cannot be used from here.")
            return
        await ctx.send(f"Removed the unauthorized users.\nStored their emails in the database successfully!")

    @commands.command(name="ban",help="Bans the specified user from the server.")
    @commands.has_role(ADMIN)
    async def ban(self,ctx,member:discord.User=None,reason=None):
        if(str(ctx.channel.id)!=SAC_CHANNEL):
            await ctx.send(f"This command cannot be used from here.")
            return
        if member==None or member==ctx.message.author:
            await ctx.send("You cannot ban yourself.")
            return
        await member.send(f"You have been banned from {ctx.guild.name}. Contact SAC.")
        return

    @commands.command(name="kick",help="Kicks out the specified user from the server.")
    @commands.has_role(ADMIN)
    async def kick(self,ctx,member:discord.User=None,reason=None):
        if(str(ctx.channel.id)!=SAC_CHANNEL):
            await ctx.send(f"This command cannot be used from here.")
            return
        if member==None or member==ctx.message.author:
            await ctx.send("You cannot kick out yourself.")
            return
        await member.send(f"You have been kicked out from {ctx.guild.name}. Contact SAC.")


def setup(bot):
    bot.add_cog(Admin(bot))