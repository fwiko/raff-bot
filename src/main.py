import discord
import json
import datetime

from discord.ext import commands
from collections import namedtuple
from settings import CONFIG

INTENTS = discord.Intents.default()
INTENTS.members = True

def load_extensions() -> None:
    """Load each extension listed in the config"""
    for extension in CONFIG.bot.extensions:
        try:
            bot.load_extension(f"extensions.{extension}.{extension}")
        except Exception as error:
            print(f"{extension} cannot be loaded. [{error}]")
        else:
            print(f"> Loaded {extension}")


if __name__ == '__main__':
    bot = commands.AutoShardedBot(command_prefix=commands.when_mentioned_or(CONFIG.bot.prefix), owner_id=264375928468013058, intents=INTENTS)


    @bot.command()
    @commands.is_owner()
    async def shutdown(ctx):
        """Shutdown the bot"""
        await bot.logout()


    @bot.event
    async def on_ready():
        print(f"""
            Logged in...\n
            Name: {bot.user.name}
            ID: {bot.user.id}
            Author: Rafferty
            Version: 0.0
            Date: {(datetime.datetime.now()).strftime("%d-%m-%Y @ %H:%M:%S")}
        """)
        await bot.change_presence(activity=discord.Game(name=CONFIG.bot.status))


    @bot.command()
    @commands.is_owner()
    async def load(ctx, extension):
        """Load an extension"""
        try:
            bot.load_extension(f"extensions.{extension}.{extension}")
            res = discord.Embed(description=f":white_check_mark: Loaded Extension `{extension}`", colour=CONFIG.bot.embed_colour)
        except Exception as error:
            res = discord.Embed(description=f"{extension} cannot be reloaded.\n`{error}`", colour=CONFIG.bot.embed_colour)
        finally:
            await ctx.send(embed=res)


    @bot.command()
    @commands.is_owner()
    async def unload(ctx, extension):
        """Unload an extension"""
        try:
            if extension in CONFIG.bot.blacklisted:
                res = discord.Embed(description=f":x: You cannot unload this module. `{extension}`", colour=CONFIG.bot.embed_colour)
            else:
                bot.unload_extension(f"extensions.{extension}.{extension}")
                res = discord.Embed(description=f":white_check_mark: Unloaded Extension `{extension}`", colour=CONFIG.bot.embed_colour)
        except Exception as error:
            res = discord.Embed(description=f"{extension} cannot be reloaded.\n`{error}`", colour=CONFIG.bot.embed_colour)
        finally:
            await ctx.send(embed=res)


    @bot.command()
    @commands.is_owner()
    async def reload(ctx, extension):
        """Reload a extension"""
        try:
            bot.unload_extension(f"extensions.{extension}.{extension}")
            bot.load_extension(f"extensions.{extension}.{extension}")
            res = discord.Embed(description=f":white_check_mark: Reloaded Extension `{extension}`", colour=CONFIG.bot.embed_colour)
        except Exception as error:
            res = discord.Embed(description=f"{extension} cannot be reloaded.\n`{error}`", colour=CONFIG.bot.embed_colour)
        finally:
            await ctx.send(embed=res)


    bot.remove_command("help")
    load_extensions()

    bot.run(CONFIG.bot.token)
