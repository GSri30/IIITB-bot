#discord
import discord
from discord.ext import commands
from discord.utils import get
from discord import Activity,ActivityType
#secret
from secret import ADMIN, ADMIN_LOG, NEWBIE,GUILD,RULES_CHANNEL, WELCOME_CHANNEL
#constants
from __constants import _GREETINGS,GREETINGS
#other
import random

#Base Cog
class Base(commands.Cog,name="Base Cog"):
    def __init__(self,bot):
        self.bot=bot
    

    async def set_permissions(self):
        guild=get(self.bot.guilds,name=GUILD)
        channels=guild.channels
        newbie=get(guild.roles,name=NEWBIE)

        for channel in channels:
            if int(channel.id)==int(RULES_CHANNEL):
                continue
            await channel.set_permissions(newbie,view_channel=False,attach_files=False,send_messages=False,send_tts_messages=False)


    @commands.Cog.listener()
    async def on_member_join(self,member):
        if not member.bot:
            await member.add_roles(get(get(self.bot.guilds,name=GUILD).roles,name=NEWBIE))
            await member.send((f"<@{member.id}> Hey Hii!\nYou need to verify your IIITB mail id in order to get into the server!\n"
                                f"If you don't have any key, contact admins.\n"
                                f"If you have a key, head over to <#{RULES_CHANNEL}> and come back! I will be waiting. :smile:"
                                ))
            return
        
        greeting=random.choice(GREETINGS).replace(_GREETINGS, f"<@{member.id}>")
        await get(get(self.bot.guilds,name=GUILD).channels,name=WELCOME_CHANNEL).send(greeting)


    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.change_presence(activity=Activity(type=ActivityType.listening, name="!help"))
        print(f'{self.bot.user.name} has connected to Discord!')

    @commands.Cog.listener()
    async def on_guild_channel_create(self,channel):
        await self.bot.wait_until_ready()
        
        guild=get(self.bot.guilds,name=GUILD)
        newbie=get(guild.roles,name=NEWBIE)
        await channel.set_permissions(newbie,view_channel=False,attach_files=False,send_messages=False,send_tts_messages=False)
        

    @commands.Cog.listener()
    async def on_guild_channel_update(self,before,after):
        guild=get(self.bot.guilds,name=GUILD)
        newbie=get(guild.roles,name=NEWBIE)
        everyone=get(guild.roles,name="@everyone")

        async for log in guild.audit_logs(limit=1):
            user=log.user

        if user.bot or after.id==int(RULES_CHANNEL):
            return

        if (before.overwrites_for(newbie)!=after.overwrites_for(newbie)):
            log_channel=get(guild.channels,id=int(ADMIN_LOG))
            await log_channel.send(f"{user} changed 'newbie' role settings for <#{after.id}>. Might be risky! (I have reset the important ones :smile:) Get to 'audit-log' to get complete details.")
            await log_channel.set_permissions(newbie,view_channel=False,attach_files=False,send_messages=False,send_tts_messages=False)

        if (before.overwrites_for(everyone)!=after.overwrites_for(everyone)):
            log_channel=get(guild.channels,id=int(ADMIN_LOG))
            await log_channel.send(f"{user} changed '@everyone' role settings for <#{after.id}>. Might be risky! Get to 'audit-log' to get complete details.")



    @commands.Cog.listener()
    async def on_member_update(self,before,after):
        guild=get(self.bot.guilds,name=GUILD)
        async for log in guild.audit_logs(limit=1):
            user=log.user

        if user.bot:
            return
        
        ok=False
        for role in after.roles:
            if role.name==NEWBIE:
                ok=True
                break

        if (ok and len(after.roles)>2) or (len(after.roles)==1):
            await get(get(self.bot.guilds,name=GUILD).channels,id=int(ADMIN_LOG)).send(f"Something fishy! {user} updated {after} (newbie) role which might give him/her message access. Get to 'audit log' to get complete details.")
        

def setup(bot):
    bot.add_cog(Base(bot))