import discord
import datetime

from discord.ext import commands
from settings import CONFIG

class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="membercount",aliases=["users"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.guild_only()
    async def membercount(self, ctx):
        """Get membercount of current server"""
        embed=discord.Embed(color=CONFIG.bot.embed_colour, timestamp = datetime.datetime.utcnow())
        embed.add_field(name="Server Members", value=f"{len(ctx.guild.members)}")
        await ctx.send(embed=embed)


    @commands.command(usage="<member>", description="Gets a users avatar")
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.guild_only()
    async def avatar(self, ctx, member: discord.Member = None):
        """Get large avatar of specified user"""
        if member != None:
            embed = discord.Embed(color=CONFIG.bot.embed_colour)
            embed.set_author(name=member, icon_url=member.avatar)
            embed.set_image(url=member.avatar)
        elif member == None:
            embed = discord.Embed(color=CONFIG.bot.embed_colour)
            embed.set_author(name=ctx.author, icon_url=ctx.message.author.avatar)
            embed.set_image(url=ctx.message.author.avatar)
        await ctx.send(embed=embed)


    @commands.command(usage="<member>", description="Gets information about a user")
    @commands.guild_only()
    async def user(self, ctx, member:discord.Member = None):
        """Get information about specified user"""
        if member == None:
            member = ctx.author
        embed=discord.Embed(color=CONFIG.bot.embed_colour, timestamp=datetime.datetime.utcnow())
        embed.set_author(name=f"Information about {member.name}", icon_url=member.avatar)
        embed.set_thumbnail(url=member.avatar)
        if member.joined_at is not None:
            embed.add_field(name="Joined Server", value=member.joined_at.strftime("%A, %B %d %Y @ %H:%M"))
        embed.add_field(name="Registered", value=member.created_at.strftime("%A, %B %d %Y @ %H:%M"))
        if member in ctx.guild.premium_subscribers:
            embed.add_field(name="Boosting Since", value=member.premium_since.strftime("%A, %B %d %Y @ %H:%M"), inline=False)
        roles = [f"<@&{role.id}>" for role in member.roles if role != ctx.guild.default_role]
        if roles != []:
            embed.add_field(name="Roles",value=", ".join(roles),inline=False   )
        await ctx.channel.send(embed=embed)


def setup(bot):
    bot.add_cog(Utility(bot))
