from pickle import NONE
import discord
from discord.ext import commands
from bot.utils.constants import TOKEN, PREFIX
import os
from bot.utils.utils import mongo
import dns.resolver


class timeBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=PREFIX, intents=discord.Intents.all())

    async def on_ready(self):
        await load()
        print(f"Logged in as {self.user}")


bot = timeBot()

bot.remove_command("help")


async def load():
    for fn in os.listdir("cogs"):
        if fn.endswith(".py"):
            await bot.load_extension(f"cogs.{fn[:-3]}")


@bot.event
async def on_message(message):
    dns.resolver.default_resolver = dns.resolver.Resolver(configure=False)
    dns.resolver.default_resolver.nameservers = ["8.8.8.8"]
    if message.author.bot:
        return
    if isinstance(message.channel, discord.DMChannel):
        return
    await bot.process_commands(message)
    data = mongo()
    create_user = data.find_one({"_id": int(message.author.id)})
    if message.author == bot.user:
        return
    try:
        if isinstance(message.channel, discord.DMChannel):
            return
        if create_user is None:
            user = {"_id": int(message.author.id), "name": str(message.author.name)}
            data.insert_one(user)
            print(f"Added {str(message.author.name)} to db")
    except Exception as e:
        print(e)
    if message.author == bot.user:
        return


@bot.command()
async def sync(ctx: commands.Context):
    await ctx.send("Syncing Slash Commands")
    synced = await bot.tree.sync()
    if len(synced) > 0:
        for cmd in synced:
            await ctx.send(f"Synced {cmd}")
        await ctx.send(f"Synced {len(synced)} Commands Globally!")
    else:
        await ctx.send("No Slash Commands to Register.")


@bot.command(name="sleep")
async def sleep(ctx: commands.Context):
    if str(ctx.author.id) != "786926252811485186":
        return
    await ctx.send("Going to sleep")
    await bot.close()


if __name__ == "__main__":
    bot.run(token=TOKEN)
