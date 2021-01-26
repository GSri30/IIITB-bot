from discord import Embed

class Embeds:
    def __init__(self):
        pass

    def IntroEmbed(bot,UserName,MailID:str,DiscordID:str):
        embed=Embed(title="Welcome to IIITB discord community!",description="The following data is collected by SAC : ",color=0x00ff00)
        embed.add_field(name="User Name",value=UserName,inline=False)
        embed.add_field(name="Email ID",value=MailID,inline=False)
        embed.add_field(name="Discord ID",value=DiscordID,inline=False)
        embed.set_footer(text="Hope you will have a great time.\nSAC IIIT Bangalore.")
        embed.set_thumbnail(url=bot.user.avatar_url)
        return embed
    
    def NextContestEmbed(title:str,name:str,event_url:str,start:str,duration:str,logo_url:str,color:str):
        embed=Embed(title=title,description=f"[{name}]({event_url})",color=color)
        embed.add_field(name="Start time",value=start)
        embed.add_field(name="Duration",value=duration)
        embed.set_footer(text="All the best!")
        embed.set_thumbnail(url=logo_url)
        return embed