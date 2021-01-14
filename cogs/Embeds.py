from discord import Embed

class Embeds:
    def __init__(self):
        pass

    def IntroEmbed(bot,UserName,MailID:str,DiscordID:str):
        embed=Embed(title="Welcome to IIITB discord community!",description="The following data is collected by SAC : ",color=0x00ff00)
        embed.add_field(name="User Name",value=UserName,inline=False)
        embed.add_field(name="Email ID",value=MailID,inline=False)
        embed.add_field(name="Discord ID",value=DiscordID,inline=False)
        embed.set_footer(text="Hope you obey with all the rules.\nSAC IIIT Bangalore.")
        embed.set_thumbnail(url=bot.user.avatar_url)
        return embed