from random import choice

import discord
import aiohttp

from discord.ext import commands
from utils.classes import ColourCodes


_cooldown = commands.CooldownMapping.from_cooldown(
    4.0, 15.0, commands.BucketType.user)


class Misc(
    commands.Cog, command_attrs={"cooldown": _cooldown}
    ):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot


    @commands.command()
    @commands.guild_only()
    async def kiss(
        self, ctx: commands.Context, 
        *, member: discord.Member
        ) -> discord.Embed:
        """
        kisses another member

        Parameters
        ----------
        `member`: discord.Member
         the member to kiss
        
        Returns
        -------
        `discord.Embed`
         an embed saying that you kissed the member
        """

        if member == ctx.author:
            return await ctx.send("virgin spotted")

        embed = discord.Embed(
            colour=ColourCodes.theme_colour,
            description=f"{ctx.author.mention} **kisses** {member.mention} :kissing_heart:")
        await ctx.send(embed=embed)


    @commands.command()
    @commands.guild_only()
    async def fuck(
        self, ctx: commands.Context, 
        *, member: discord.Member
        ) -> discord.Embed:
        """
        fucks another member

        Parameters
        ----------
        `member`: discord.Member
         the member to fuck
        
        Returns
        -------
        `discord.Embed`
         an embed saying that you fucked the member
        """

        if member == ctx.author:
            return await ctx.send("virgin spotted")

        embed = discord.Embed(
            colour=ColourCodes.theme_colour,
            description=f"{ctx.author.mention} **fucks** {member.mention} :peach: :eggplant:")
        await ctx.send(embed=embed)


    @commands.command()
    @commands.guild_only()
    async def slap(
        self, ctx: commands.Context, 
        *, member: discord.Member
        ) -> discord.Embed:
        """
        slaps another member

        Parameters
        ----------
        `member`: discord.Member
         the member to slap
        
        Returns
        -------
        `discord.Embed`
         an embed saying that you slapped the member
        """

        if member == ctx.author:
            return await ctx.send("are u dumb")

        embed = discord.Embed(
            colour=ColourCodes.theme_colour,
            description=f"{ctx.author.mention} **slaps** {member.mention} :angry:")
        await ctx.send(embed=embed)


    @commands.command()
    @commands.guild_only()
    async def kill(
        self, ctx: commands.Context, 
        *, member: discord.Member
        ) -> discord.Embed:
        """
        kills another member

        Parameters
        ----------
        `member`: discord.Member
         the member to kill
        
        Returns
        -------
        `discord.Embed`
         an embed saying that you killed the member
        """

        if member == ctx.author:
            return await ctx.send("stfu depressed kid")

        embed = discord.Embed(
            colour=ColourCodes.theme_colour,
            description=f"{ctx.author.mention} **kills** {member.mention} :knife:")
        await ctx.send(embed=embed)


    @commands.command()
    @commands.guild_only()
    async def punch(
        self, ctx: commands.Context, 
        *, member: discord.Member
        ) -> discord.Embed:
        """
        punches another member

        Parameters
        ----------
        `member`: discord.Member
         the member to punch
        
        Returns
        -------
        `discord.Embed`
         an embed saying that you punched the member
        """

        if member == ctx.author:
            return await ctx.send("why are u punching yourself moron")

        embed = discord.Embed(
            colour=ColourCodes.theme_colour,
            description=f"{ctx.author.mention} **punches** {member.mention} :punch:")
        await ctx.send(embed=embed)


    @commands.command()
    @commands.guild_only()
    async def shoot(
        self, ctx: commands.Context,
        *, member: discord.Member
        ) -> discord.Embed:
        """
        shoots another member

        Parameters
        ----------
        `member`: discord.Member
         the member to shoot
        
        Returns
        -------
        `discord.Embed`
         an embed saying that you shot the member
        """

        if member == ctx.author:
            return await ctx.send("stfu depressed kid")

        embed = discord.Embed(
            colour=ColourCodes.theme_colour,
            description=f"{ctx.author.mention} **shoots** {member.mention} :gun:")
        await ctx.send(embed=embed)


    @commands.command()
    @commands.guild_only()
    async def hug(
        self, ctx: commands.Context, 
        *, member: discord.Member
        ) -> discord.Embed:
        """
        hugs another member

        Parameters
        ----------
        `member`: discord.Member
         the member to hug
        
        Returns
        -------
        `discord.Embed`
         an embed saying that you hugged the member
        """

        if member == ctx.author:
            return await ctx.send("stfu depressed kid")

        embed = discord.Embed(
            colour=ColourCodes.theme_colour,
            description=f"{ctx.author.mention} **hugs** {member.mention} :people_hugging:")
        await ctx.send(embed=embed)


    @commands.command()
    @commands.guild_only()
    async def gayrate(self, ctx: commands.Context) -> str:
        """
        to check how much of a fag you are

        Returns
        -------
        `str`
         a random rate
        """        

        variable_list: list[str] = [
        "0% gay", "10% gay", "20% gay", "30% gay",
        "40% gay", "50% gay", "60% gay","70% gay",
        "80% gay", "90% gay", "100% gay"]

        await ctx.send(f"{choice(variable_list)}")


    @commands.command()
    @commands.guild_only()
    async def pp(self, ctx: commands.Context) -> str:
        """
        how big is your pp

        Returns
        -------
        `str`
         a random pp size
        """        

        variable_list: list[str] = [
        "8================D (what did they feed you)", "8==========D",
        "8=========D", "8=======D", "8======D", "8=====D", "8===D",
        "8=D", "8D"]

        await ctx.send(f"{choice(variable_list)}")


    @commands.command()
    @commands.guild_only()
    async def cat(self, ctx: commands.Context) -> discord.Embed:
        """
        shows random cat pics

        Returns
        -------
        `discord.Embed`
         an embed with a random cat image
        """

        embed = discord.Embed(colour=ColourCodes.theme_colour)

        async with aiohttp.ClientSession() as client_session:
            async with client_session.get("http://aws.random.cat/meow") as response:
                res = await response.json()

                embed.set_image(url=res["file"])
                await ctx.send(embed=embed)


    @commands.command()
    @commands.guild_only()
    async def dog(self, ctx: commands.Context) -> discord.Embed:
        """
        shows random dog pics

        Returns
        -------
        `discord.Embed`
         an embed with a random dog image
        """

        embed = discord.Embed(colour=ColourCodes.theme_colour)

        async with aiohttp.ClientSession() as client_session:
            async with client_session.get("https://dog.ceo/api/breeds/image/random") as r:
                res = await r.json()

                embed.set_image(url=res["message"])
                await ctx.send(embed=embed)


    @commands.command()
    @commands.guild_only()
    async def panda(self, ctx: commands.Context) -> discord.Embed:
        """
        shows random panda images

        Returns
        -------
        `discord.Embed`
         an embed with a random panda image
        """

        embed = discord.Embed(colour=ColourCodes.theme_colour)

        async with aiohttp.ClientSession() as client_session:
            async with client_session.get("https://some-random-api.ml/animal/panda") as response:
                panda = await response.json()

                embed.set_image(url=panda["image"])
                await ctx.send(embed = embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Misc(bot))
