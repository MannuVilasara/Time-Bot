from discord.ext import commands
import discord
import requests


class Fetch(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="spotify", description="get user now playing")
    async def spotify(self, ctx: commands.Context, member: discord.Member = None):
        if member is None:
            member = ctx.author
        spotify_activity = None
        for activity in member.activities:
            if isinstance(activity, discord.Spotify):
                spotify_activity = activity
                break

        if spotify_activity is not None:
            song_name = spotify_activity.title
            artist_name = spotify_activity.artist
            album_name = spotify_activity.album
            thumbnail = spotify_activity.album_cover_url
            duration = spotify_activity.duration

            embed = discord.Embed(
                title="Spotify",
                description=f"""
                                  **Song**\n{song_name}\n\n**Artist(s)**\n{artist_name}\n\n**Album**\n{album_name}\n
                                  \n**Duration**\n{duration}""",
                color=discord.Colour.green(),
            )
            embed.set_thumbnail(url=thumbnail)
            embed.set_footer(
                text=f"Spotify of {member.display_name}", icon_url=member.display_avatar
            )
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title="Spotify",
                description=f"Not Listening",
                color=discord.Colour.red(),
            )
            embed.set_footer(
                text=f"Spotify of {member.display_name}", icon_url=member.display_avatar
            )
            await ctx.send(embed=embed)

    @commands.hybrid_command()
    async def gh(self, ctx: commands.Context, username):
        url = f"https://api.github.com/users/{username}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            avatar = data.get("avatar_url")
            name = data.get("name")
            bio = data.get("bio")
            followers = data.get("followers")
            following = data.get("following")
            public_repos = data.get("public_repos")
            url = data.get("html_url")

            embed = discord.Embed(title=f"GitHub Profile - {username}", url=url)
            embed.set_thumbnail(url=avatar)
            if name:
                embed.add_field(name="Name", value=name, inline=False)
            if bio:
                embed.add_field(name="Bio", value=bio, inline=False)
            if followers:
                embed.add_field(name="Followers", value=followers, inline=True)
            if following:
                embed.add_field(name="Following", value=following, inline=True)
            if public_repos:
                embed.add_field(
                    name="Public Repositories", value=public_repos, inline=True
                )

            await ctx.send(embed=embed)
        else:
            await ctx.send("GitHub profile not found.")


async def setup(bot):
    await bot.add_cog(Fetch(bot))
    print("Fetch is loaded")
