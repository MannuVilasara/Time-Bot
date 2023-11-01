import requests
from discord.ext import commands
import discord
from bot.utils.utils import mongo


class Timezones(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="time", description="know user's time")
    async def time(self, ctx: commands.Context, member: discord.Member = None):
        msg = await ctx.send("stalking user to see time...")
        if member is None:
            member = ctx.author
        db = mongo()
        user = db.find_one({"_id": int(member.id)})
        if "timezone" in user:
            timezone = user["timezone"]
            a = requests.get(
                f"https://www.timeapi.io/api/Time/current/zone?timeZone={timezone}"
            ).json()
            time = a["time"]
            date = a["date"]
            colour = discord.Colour.green()
            embed = discord.Embed(
                title=f"Time for {member.display_name}",
                description=f"Date: {date} \n Time: {time} \n  <a:anime_zerotwohypedfast:1120375721819377715> ",
                color=colour,
            )
            embed.set_thumbnail(url=member.display_avatar)
            await msg.edit(content="here it is", embed=embed)
            return
        else:
            if ctx.author.id == member.id:
                await msg.edit(content="Please set your timezone")
            else:
                await msg.edit(
                    content=f"Please tell {member.display_name} to set their time"
                )

    @commands.hybrid_command(
        name="set-timezone", description="set user timezone to get time information"
    )
    async def set(self, ctx: commands.Context, timezone: str = None):
        if timezone is None:
            await ctx.send("Please enter your timezone")
            return
        a = requests.get(
            f"https://www.timeapi.io/api/Time/current/zone?timeZone={timezone}"
        ).json()
        if "Invalid Timezone" in a:
            await ctx.send("Please Enter A Valid Timezone")
            return
        else:
            db = mongo()
            user = db.find_one({"_id": int(ctx.author.id)})
            if "timezone" not in user:
                question = discord.Embed(
                    title=f"Are You Sure want to Set {timezone} as your timezone"
                )
                message = await ctx.send(embed=question)
                await message.add_reaction("✔")
                await message.add_reaction("❌")  # Add reaction options

                def check(react, users):
                    return users == ctx.author and str(react.emoji) in ["✔", "❌"]

                try:
                    reaction, _ = await self.bot.wait_for(
                        "reaction_add", timeout=60.0, check=check
                    )
                except TimeoutError:
                    await ctx.send("Timed Out")
                else:
                    if reaction.emoji == "✔":
                        db.delete_one(user)
                        user["timezone"] = timezone
                        db.insert_one(user)
                        await ctx.send("Success")
                    elif reaction.emoji == "❌":
                        await ctx.send("Canceled")
            else:
                db.delete_one(user)
                del user["timezone"]
                user["timezone"] = timezone
                db.insert_one(user)
                await ctx.send(f"`Updated your timezone to {timezone}`")

    @commands.hybrid_command(name="remove-timezone", description="remove user timezone")
    async def remove(self, ctx: commands.Context):
        db = mongo()
        user = db.find_one({"_id": int(ctx.author.id)})
        if "timezone" in user:
            db.delete_one(user)
            del user["timezone"]
            db.insert_one(user)
            await ctx.send("Removed your timezone")
        else:
            await ctx.send("You don't have timezone set")


async def setup(bot):
    await bot.add_cog(Timezones(bot))
    print("Timezone is loaded")
