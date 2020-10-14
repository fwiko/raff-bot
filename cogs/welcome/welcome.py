import discord, aiohttp, asyncio, time, json, datetime, random
from discord.ext import tasks, commands
from discord.ext.commands import guild_only

def load_data(file_name):
    f = open(file_name, )
    return json.load(f)

def write_data(data):
    with open('config.json', 'w') as file:
        json.dump(data, file, indent=2)

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.welcome_messages = [    
            "{member} just joined the server - glhf!",
            "{member} just joined. Everyone, look busy!",
            "{member} just joined. Can I get a heal?",
            "{member} joined your party.",
            "{member} joined. You must construct additional pylons.",
            "Ermagherd. {member} is here.",
            "Welcome, {member}. Stay awhile and listen.",
            "Welcome, {member}. We were expecting you ( ͡° ͜ʖ ͡°)",
            "Welcome, {member}. We hope you brought pizza.",
            "Welcome {member}. Leave your weapons by the door.",
            "A wild {member} appeared.",
            "Swoooosh. {member} just landed.",
            "Brace yourselves. {member} just joined the server.",
            "{member} just joined. Hide your bananas.",
            "{member} just arrived. Seems OP - please nerf.",
            "{member} just slid into the server.",
            "A {member} has spawned in the server.",
            "Big {member} showed up!",
            "Where’s {member}? In the server!",
            "{member} hopped into the server. Kangaroo!!",
            "{member} just showed up. Hold my beer.",
            "Challenger approaching - {member} has appeared!",
            "It's a bird! It's a plane! Nevermind, it's just {member}.",
            "It's {member}! Praise the sun! [T]/",
            "Never gonna give {member} up. Never gonna let {member} down.",
            "Ha! {member} has joined! You activated my trap card!",
            "Cheers, love! {member}'s here!",
            "Hey! Listen! {member} has joined!",
            "We've been expecting you {member}",
            "It's dangerous to go alone, take {member}!",
            "{member} has joined the server! It's super effective!",
            "Cheers, love! {member} is here!",
            "{member} is here, as the prophecy foretold.",
            "{member} has arrived. Party's over.",
            "Ready player {member}",
            "{member} is here to kick butt and chew bubblegum. And {member} is all out of gum.",
            "Hello. Is it {member} you're looking for?",
            "{member} has joined. Stay a while and listen!",
            "Roses are red, violets are blue, {member} joined this server with you",
        ]

    @commands.Cog.listener()
    async def on_member_join(self, member):
        config = load_data('config.json')
        if config['welcome']['welcome_message']:
            await member.guild.system_channel.send(self.welcome_messages[random.randint(0, len(self.welcome_messages)-1)].format(member=member.mention))
        if config['welcome']['welcome_dm']:
            embed = discord.Embed(
                title=config['welcome']['welcome_message_title'],
                description=config['welcome']['welcome_message_description'],
                color=config['bot']['embed_colour'],
                timestamp=datetime.datetime.utcnow()
            )
            embed.set_image(
                url=config['welcome']['welcome_message_image']
            )
            try:
                await member.send(embed=embed)
            except Exception as e:
                print(e)

    @commands.command()
    async def test(self, ctx):
        config = load_data('config.json')
        for i in config:
            await ctx.send(i)

def setup(bot):
    bot.add_cog(Welcome(bot))