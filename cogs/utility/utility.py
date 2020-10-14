import discord, json, asyncio, datetime
from discord.ext import commands
from discord.utils import get

def load_data(file_name):
    f = open(file_name, )
    return json.load(f)

def write_data(data):
    with open('config.json', 'w') as file:
        json.dump(data, file, indent=2)

class Utils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="membercount",aliases=["users"])
    @commands.cooldown(1, 30, commands.BucketType.user)
    @commands.guild_only()
    async def membercount(self, ctx):
        embed=discord.Embed(
            color=load_data('config.json')['bot']['embed_colour'],
            timestamp = datetime.datetime.utcnow()
        )
        embed.add_field(
            name="Server Members",
            value=f"{len(ctx.guild.members)}"
        )
        await ctx.send(embed=embed)

    @commands.command(usage="<member>", description="Gets a users avatar")
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def avatar(self, ctx, member: discord.Member = None):
        if member != None:
            embed = discord.Embed(
                color=load_data('config.json')['bot']['embed_colour']
            )
            embed.set_author(
                name=member,
                icon_url=member.avatar_url
            )
            embed.set_image(url=member.avatar_url)
        elif member == None:
            embed = discord.Embed(
                color=load_data('config.json')['bot']['embed_colour']
                )
            embed.set_author(
                name=ctx.author,
                icon_url=ctx.author.avatar_url
            )
            embed.set_image(url=ctx.message.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(usage="<member>", description="Gets information about a user")
    @commands.guild_only()
    async def user(self, ctx, member:discord.Member = None):
        roles = []
        if member == None:
            member = ctx.author

        embed=discord.Embed(
            color=load_data('config.json')['bot']['embed_colour'],
            timestamp=datetime.datetime.utcnow()
        )
        embed.set_author(
            name=f"Information about {member.name}",
            icon_url=member.avatar_url
        )
        embed.set_thumbnail(
            url=member.avatar_url
        )
        if member.joined_at is not None:
            embed.add_field(
                name="Joined Server",
                value=member.joined_at.strftime("%A, %B %d %Y @ %H:%M")
            )
        embed.add_field(
            name="Registered",
            value=member.created_at.strftime("%A, %B %d %Y @ %H:%M")
        )
        if member in ctx.guild.premium_subscribers:
            embed.add_field(
                name="Boosting Since",
                value=member.premium_since.strftime("%A, %B %d %Y @ %H:%M"),
                inline=False
            )
        for role in member.roles:
            if role != ctx.guild.default_role:
                roles.append(f"<@&{role.id}>")
            else:
                pass
        if roles != []:
            embed.add_field(
                name="Roles",
                value=", ".join(roles),
                inline=False   
            )
        await ctx.channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content != "":
            print(f" > {message.author} ({message.author.id}) - {message.content}")

def setup(bot):
    bot.add_cog(Utils(bot))
