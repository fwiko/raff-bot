import discord, asyncio, json, re, os
from discord import utils, Embed
from discord.ext import commands
from discord.utils import get

def load_data():
    f = open("config.json", )
    return json.load(f)

def write_data(file_name, data):
    with open(file_name, 'w') as file:
        json.dump(data, file, indent=2)

config = load_data()

intents = discord.Intents.default()
intents.members = True

bot = commands.AutoShardedBot(command_prefix=commands.when_mentioned_or(config['bot']['prefix']), owner_id=264375928468013058, intents=intents)
extensions = config['bot']['extensions']
bot.remove_command('help')

if __name__ == '__main__':
    for extension in extensions:
        try:
            bot.load_extension(f"cogs.{extension}.{extension}")
        except Exception as error:
            print(f"{extension} cannot be loaded. [{error}]")
        else:
            print(f"> Loaded {extension}")
    
"""async def status_task():
    data = read_json('config')
    while True:
        for x in data['other']['playing_status']:
            await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=x))
            await asyncio.sleep(10)
            data = read_json('config')
"""
@bot.event
async def on_ready():
	print(f"> Logged in...")
	await bot.change_presence(activity=discord.Game(name=config['bot']["status"]))

@bot.command()
@commands.is_owner()
async def load(ctx, extension):
    """Load a module"""
    await ctx.message.delete()
    try:
        if extension == "modules":
            await ctx.send(":x: You cannot load this module.")
        else:
            bot.load_extension(f"cogs.{extension}.{extension}")
            await ctx.send(f":white_check_mark: Loaded `{extension}`")
            config['bot']['extensions'].append(extension)
            write_data('config.json', config)
    except Exception as error:
        c = discord.Embed(description=f"{extension} cannot be loaded.\n`{error}`", colour=0x2f3136)
        await ctx.send(embed=c)

@bot.command()
@commands.is_owner()
async def unload(ctx, extension):
    """Unload a module"""
    await ctx.message.delete()
    try:
        if extension == "modules":
            await ctx.send(":x: You cannot unload this module.")
        else:
            bot.unload_extension(f"cogs.{extension}.{extension}")
            await ctx.send(f":white_check_mark: Unloaded `{extension}`")
            config['bot']['extensions'].remove(extension)
            write_data('config.json', config)
    except Exception as error:
        c = discord.Embed(description=f"{extension} cannot be unloaded.\n`{error}`", colour=0x2f3136)
        await ctx.send(embed=c)

@bot.command()
@commands.is_owner()
async def reload(ctx, extension):
    """Reload a module"""
    await ctx.message.delete()
    try:
        if extension == "modules":
            await ctx.send(":x: You cannot reload this module.")
        else:
            try:
                bot.load_extension(f"cogs.{extension}.{extension}")
            except:
                pass
            bot.unload_extension(f"cogs.{extension}.{extension}")
            bot.load_extension(f"cogs.{extension}.{extension}")
            c = discord.Embed(description=f":white_check_mark: Reloaded Extension `{extension}`", colour=0x2f3136)
            await ctx.send(embed=c)
    except Exception as error:
        c = discord.Embed(description=f"{extension} cannot be reloaded.\n`{error}`", colour=0x2f3136)
        await ctx.send(embed=c)

@bot.command()
@commands.is_owner()
async def shutdown(ctx):
    await bot.logout()


#bot.loop.create_task(status_task())
bot.run(config['bot']['token'])