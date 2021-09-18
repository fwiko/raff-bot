import discord
import datetime

from discord.ext import commands
from discord.utils import get

from settings import CONFIG


class Default(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content != "" and not message.author.bot:
            print(f"[{message.channel}] {message.author} ({message.author.id}) > {message.content}")


    @commands.Cog.listener()
    async def on_member_join(self, member):
        if CONFIG.welcome.enabled:
            await member.guild.system_channel.send(CONFIG.welcome.message.format(member=member.mention))


def setup(bot):
    bot.add_cog(Default(bot))
