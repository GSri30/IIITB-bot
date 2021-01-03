import os
from dotenv import load_dotenv
import discord
from discord.ext import commands

from __constants import *
from sendmail import send_mail,SENDER_ID,SENDER_PASSWORD
from passwordgen import passgen,hash,match

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
ADMIN = os.getenv("ADMIN")
SAC_CHANNEL = os.getenv("SAC_CHANNEL")
AUTH_CHANNEL = os.getenv("AUTH_CHANNEL")


bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


#! Common commands

@bot.command(name="register",help="Registers a user using their IIIT-B domain mail id.")
async def register(ctx, mailID:str):
    if(str(ctx.channel.id)!=AUTH_CHANNEL):
        await ctx.send(f"This command cannot be used from here.")
        return
    #send_mail(mailID,passgen())
    await ctx.message.add_reaction(UNCHECK_EMOJI)
    await ctx.send(f"{mailID} registered for user {ctx.author} with {ctx.author.id}")

@bot.command(name="verify",help="Verifies the user email using an associated auto generated key.")
async def verify(ctx,key:str):
    if match(key,usrhash):
        await ctx.author.send(f"You made it! Welcome to IIITB discord community!")
    else:
        await ctx.author.send(f"Sorry, you entered a wrong key. Try again!")

@bot.command(name="couriers",help="Gives you your couriers list.(if any)")
async def couriers(ctx):
    await ctx.send(f"Feature coming soon! :smile:")



#! Admin commands 

@bot.command(name="filter",help="Filters out the unauthorized users.")
@commands.has_role(ADMIN)
async def filter(ctx):
    if(str(ctx.channel.id)!=SAC_CHANNEL):
        await ctx.send(f"This command cannot be used from here.")
        return
    await ctx.send("Filtered and returned the results!")

@bot.command(name="filter-remove",help="Filters out the unauthorized users and removes them from the server.")
@commands.has_role(ADMIN)
async def filter_remove(ctx):
    if(str(ctx.channel.id)!=SAC_CHANNEL):
        await ctx.send(f"This command cannot be used from here.")
        return
    await ctx.send(f"Removed the unauthorized users.\nStored their emails in the database successfully!")

@bot.command(name="ban",help="Bans the specified user from the server.")
@commands.has_role(ADMIN)
async def ban(ctx,member:discord.User=None,reason=None):
    if(str(ctx.channel.id)!=SAC_CHANNEL):
        await ctx.send(f"This command cannot be used from here.")
        return
    if member==None or member==ctx.message.author:
        await ctx.send("You cannot ban yourself.")
        return
    await member.send(f"You have been banned from {ctx.guild.name}. Contact SAC.")
    return

@bot.command(name="kick",help="Kicks out the specified user from the server.")
@commands.has_role(ADMIN)
async def kick(ctx,member:discord.User=None,reason=None):
    if(str(ctx.channel.id)!=SAC_CHANNEL):
        await ctx.send(f"This command cannot be used from here.")
        return
    if member==None or member==ctx.message.author:
        await ctx.send("You cannot kick out yourself.")
        return
    await member.send(f"You have been kicked out from {ctx.guild.name}. Contact SAC.")


#! Error handling

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send(f'You do not have the required permission to use this command. Try contacting SAC!')
    # elif(isinstance(error, commands.errors.MissingRequiredArgument)):
    #     await ctx.send(f"{error}")
    else:
        await ctx.send(f"{error}")


bot.run(TOKEN)