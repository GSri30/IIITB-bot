#discord
from discord.ext import commands,tasks
from discord.channel import DMChannel
from discord.utils import get
#embeds
from cogs.Embeds import Embeds
#constants
from __constants import CHECK_EMOJI,CROSS_EMOJI,CP_LOGOS,COLORS
#secret
from secret import DEVELOPERS_CHANNEL,GUILD,CP_CHANNEL,NEWBIE,CLIST_USERNAME,CLIST_KEY
#Other
import requests
import time
from urllib.parse import urlparse
import random


#CP cog
class CP(commands.Cog,name="Competitive Programming Cog"):
    def __init__(self,bot):
        self.bot=bot
        self.NextContest.start()

    def is_a_DM(self,ctx):
        return isinstance(ctx.channel,DMChannel)

    def is_a_newbie(self,ctx):
        ok=get(ctx.author.roles,name=NEWBIE)
        return ok is not None

    def sec_to_hour(self,sec:str):
        min,sec=divmod(sec,60)
        hour,min=divmod(min,60)
        return "%d:%02d:%02d"%(hour,min,sec)
    
    def decode_unix(self,unixformat:float):
        return time.ctime(unixformat)

    def iso_to_sec(self,isoformat:str):
        utc_dt=time.strptime(isoformat,'%Y-%m-%dT%H:%M:%S')
        return time.mktime(utc_dt)

    def decode_iso(self,isoformat:str):
        return self.decode_unix(self.iso_to_sec(isoformat))

    def hostname(self,url:str):
        return urlparse(url).hostname

    @commands.command(name="random-cf",help="Gives a random Codeforces question.")
    async def randomQ(self,ctx):
        if self.is_a_DM(ctx):
            await ctx.message.add_reaction(CROSS_EMOJI)
            await ctx.author.send(f"Sorry. You cannot DM me for this! :neutral_face:")
            return
        await ctx.message.add_reaction(CHECK_EMOJI)
        await ctx.send(f"Feature coming soon! :smile:")
    
    # freq : 1 day
    @tasks.loop(seconds=86400)
    async def NextContest(self):
        await self.bot.wait_until_ready()
        channel=get(get(self.bot.guilds,name=GUILD).channels,id=int(CP_CHANNEL))
        async with channel.typing():
            url=f"https://clist.by/api/v1/contest/?username={CLIST_USERNAME}&api_key={CLIST_KEY}&order_by=-start&limit=1000"
            r=requests.get(url=url)
            logos=CP_LOGOS
            colors=COLORS
            if str(r.status_code)=="200":
                contests=r.json()["objects"]
                for contest in contests:
                    if(self.iso_to_sec(contest["start"])-2*86400<=time.time() and time.time()<self.iso_to_sec(contest["start"])-86400) and (self.hostname(contest["href"]) in logos): 
                        summary=Embeds.NextContestEmbed("Contest",contest["event"],contest["href"],self.decode_iso(contest["start"]),self.sec_to_hour(contest["duration"]),logos[self.hostname(contest["href"])],random.choice(colors))
                        await get(get(self.bot.guilds,name=GUILD).channels,id=int(CP_CHANNEL)).send(embed=summary)
            else:
                await get(get(self.bot.guilds,name=GUILD).channels,name=DEVELOPERS_CHANNEL).send(f"Error in CP cog while fetching next contest details.\nStatus code : {r.status_code}")


def setup(bot):
    bot.add_cog(CP(bot))