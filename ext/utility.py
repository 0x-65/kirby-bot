from re import search
from requests import get
from arrow import utcnow
from typing import Optional
from textwrap import dedent
from datetime import datetime
from bs4 import BeautifulSoup
from secrets import token_urlsafe
from dateutil.relativedelta import relativedelta

import discord
import async_cse

from discord.ext import commands

from utils.classes import Emojis, ColourCodes, Config
from utils.embed_parser import to_object, embed_replacement


class Google(discord.ui.View):
    """ search result button for the google search """

    def __init__(self) -> None:
        super().__init__(timeout=90.0)


_cooldown = commands.CooldownMapping.from_cooldown(
    4.0, 15.0, commands.BucketType.user)


class Utility(
    commands.Cog, command_attrs={"cooldown": _cooldown}
    ):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.start_time = utcnow()
        self.btc_rate: float = 30135.30


    @commands.command(aliases=["av", "pfp"])
    @commands.guild_only()
    async def avatar(
        self, ctx: commands.Context, *, user: Optional[discord.User]
        ) -> discord.Asset:  
        """
        returns a user's avatar

        Parameters
        ----------
        `user`: Optional[discord.User]
         the user to get the avatar of (defaults to ctx.author)

        Returns
        -------
        `discord.Asset`
         the user's avatar asset
        """

        user = user or ctx.author
        user = await self.bot.fetch_user(user.id)

        av_embed = discord.Embed(
            title=f"{user}'s avatar",
            url=f"{user.avatar}",
            colour=ColourCodes.theme_colour)
        av_embed.set_image(url=user.avatar)

        await ctx.send(embed=av_embed)


    @commands.command(aliases=["ub", "userbanner"])
    @commands.guild_only()
    async def banner(
        self, ctx: commands.Context, *, user: Optional[discord.User]
        ) -> discord.Asset:
        """
        returns a user's banner

        Parameters
        ----------
        `user`: Optional[discord.User]
         the user to get the banner of (defaults to ctx.author)

        Returns
        -------
        `discord.Asset`
         the user's banner asset
        """        

        user = user or ctx.author
        user = await self.bot.fetch_user(user.id)

        if not user.banner:
            return await ctx.send(f"**{user}** does not have a banner set")

        bnr_embed = discord.Embed(
            title=f"{user}'s banner",
            url=user.banner,
            colour=ColourCodes.theme_colour)
        bnr_embed.set_image(url=user.banner)

        await ctx.send(embed=bnr_embed)


    @commands.command()
    @commands.guild_only()
    async def devices(
        self, ctx: commands.Context, *, member: Optional[discord.Member]
        ) -> discord.Status:
        """
        shows the device(s) a member is currently active on

        Parameters
        ----------
        `member`: Optional[discord.Member]
         the member to show the devices of (defaults to ctx.author)

        Returns
        -------
        `discord.Status`
         the member's status on every device
        """        

        member = member or ctx.author

        devices_embed = discord.Embed(
            colour=ColourCodes.theme_colour,
            description=dedent(f"""
            {Emojis.mobile} **mobile:** `{member.mobile_status}`
            {Emojis.desktop} **desktop**: `{member.desktop_status}`
            {Emojis.web} **web:** `{member.web_status}`
            """)
            )

        devices_embed.set_author(
            name=f"{member}'s devices",
            icon_url=member.avatar)

        await ctx.send(embed=devices_embed)


    @commands.command()
    @commands.guild_only()
    async def spotify(
        self, ctx: commands.Context, *, member: Optional[discord.Member]
        ) -> discord.Embed:
        """
        shows a member's spotify activity

        Parameters
        ----------
        `member`: Optional[discord.Member]
         the member to show the spotify activity of

        Returns
        -------
        `discord.Embed`
         an embed with info about the member's activity if there's any
        """        

        member = member or ctx.author
        spotify = discord.utils.find(
            lambda activity: isinstance(activity, discord.Spotify),
            member.activities
            )

        if spotify is None:
            embed = discord.Embed(
                colour=ColourCodes.theme_colour,
                description=f"{Emojis.warning} **couldn't** detect **{member.name}'s** spotify activity")
            return await ctx.send(embed=embed)

        embed = discord.Embed(
            colour=ColourCodes.spotify_colour,
            description=dedent(f"""
            `by` [{spotify.artist}]({spotify.album_cover_url})
            `on` [{spotify.album}]({spotify.album_cover_url})"""))

        embed.set_thumbnail(url=spotify.album_cover_url)
        embed.set_footer(text=f"requested by @{ctx.author.name}")
        embed.set_author(
            name=f"{spotify.title}",
            icon_url="https://cdn.discordapp.com/emojis/962638639781797911.webp")

        await ctx.send(embed=embed)


    @commands.command()
    @commands.guild_only()
    async def google(
        self, ctx: commands.Context, *, msg: Optional[str]
        ) -> discord.Embed:
        """
        shows images based on your google search

        Parameters
        ----------
        `msg`: Optional[str]
         the message to return images based on

        Returns
        -------
        `discord.Embed`
         an embed with images based on the google search
        """        

        google_client = async_cse.Search(Config.api_key)
        results = await google_client.search(msg, safesearch=True, image_search=True)

        if not msg:
            return await ctx.send("what do you wanna search for?")

        view = Google()
        view.add_item(discord.ui.Button(
            label="view search", 
            style=discord.ButtonStyle.link,
            url=f"{results[0].url}"))

        embed = discord.Embed(
            title=results[0].title, url=results[0].url,
            colour=ColourCodes.theme_colour)

        embed.set_footer(text=f"executed by @{ctx.author.name}")
        embed.set_image(url=results[0].image_url)

        await ctx.send(embed=embed, view=view)
        await google_client.close()


    @commands.command(aliases=["pass"])
    @commands.guild_only()
    async def password(self, ctx: commands.Context) -> str:
        """
        generates a random secure password

        Returns
        -------
        `str`
         a randomly generated password
        """

        password = token_urlsafe(24)

        await ctx.reply("done, check your dms", mention_author=False)
        await ctx.author.send(f"**your generated pass:** `{password}`")


    @commands.command(aliases=["checkbtc"])
    @commands.guild_only()
    async def checkhash(
        self, ctx: commands.Context, transaction_id: str
        ) -> discord.Embed:
        """
        checks the status of a bitcoin transaction

        Parameters
        ----------
        `transaction_id`: str
         the transaction ID to get the info of

        Returns
        -------
        `discord.Embed`
         an embed with info about the transaction
        """

        try:
            html = get(f"https://live.blockcypher.com/btc/tx/{transaction_id}/")
            found_confirmations = search('<strong>(.*?)</strong> confirmations.', html.text)
            confirmations = int(found_confirmations.group(1).replace('.','').replace(',',''))

            found_amount = search('(.*?) BTC', html.text)
            amount = (found_amount.group(1).strip())

            if found_confirmations is None:
                embed = discord.Embed(
                    title="view transaction",
                    url=f"https://live.blockcypher.com/btc/tx/{transaction_id}/",
                    colour=ColourCodes.theme_colour,
                    description=dedent(f"""
                    {Emojis.warning} status: `pending`
                    {Emojis.success} confirmations: `{str(confirmations)}`
                    {Emojis.btc} amount: `{amount} BTC` **({round(float(amount) * self.btc_rate, 2)} USD)**
                    """))
                
                embed.set_footer(text="will be marked as complete at 1 confirmation")
                return await ctx.send(embed=embed)

            if confirmations >= 1:
                embed = discord.Embed(
                    title="view transaction",
                    url=f"https://live.blockcypher.com/btc/tx/{transaction_id}/",
                    colour=ColourCodes.theme_colour,
                    description=dedent(f"""
                    {Emojis.success} status: `completed`
                    {Emojis.success} confirmations: `{str(confirmations)}`
                    {Emojis.btc} amount: `{amount} BTC` **({round(float(amount) * self.btc_rate, 2)} USD)**
                    """))

                await ctx.send(embed=embed)

            else:
                embed = discord.Embed(
                    title="view transaction",
                    url=f"https://live.blockcypher.com/btc/tx/{transaction_id}/",
                    colour=ColourCodes.theme_colour,
                    description=dedent(f"""
                    {Emojis.warning} status: `pending`
                    {Emojis.success} confirmations: `{str(confirmations)}`
                    {Emojis.btc} amount: `{amount} BTC` **({round(float(amount) * self.btc_rate, 2)} USD)**
                    """))
                embed.set_footer(text="will be marked as complete at 1 confirmation")
                await ctx.send(embed=embed)
        except:
            embed = discord.Embed(
                colour=ColourCodes.theme_colour,
                description=f"{Emojis.warning} **invalid** transaction ID, make sure to provide a **valid** one")
            await ctx.send(embed=embed)


    @commands.command(aliases=["ce"])
    @commands.guild_only()
    async def buildembed(
        self, ctx: commands.Context, *, code: str
        ) -> discord.Embed:
        """
        creates an embed

        Parameters
        ----------
        `code`: str
         the embed code

        Returns
        -------
        `discord.Embed`
         the created embed
        """

        converter = commands.PartialEmojiConverter()

        try:
            em = await to_object(await embed_replacement(ctx.author, code))
            msg = await ctx.send(
                content=em[0] if not em[5] else em[5],
                embed=em[1], view=em[2], file=em[4])

            if em[3]:
                if isinstance(em[3], str):
                    await msg.add_reaction(em[3].strip())
                else:
                    emoji = await converter.convert(ctx, em[3])
                    await msg.add_reaction(emoji)

        except Exception as e:
            error_embed = discord.Embed(
                description=f'{Emojis.error} {e}',
                color=ColourCodes.theme_colour)
            await ctx.send(embed=error_embed)


    @commands.command(aliases=["ping", "uptime", "latency"])
    @commands.guild_only()
    async def status(self, ctx: commands.Context) -> discord.Embed:
        """
        shows the bot's latency and how long it has been up for

        Returns
        -------
        `discord.Embed`
         an embed with info about the bot's latency and uptime
        """

        latency: float = round(self.bot.latency * 1000, 2)
        difference = relativedelta(self.start_time - utcnow())

        uptime: str = self.start_time.shift(
            seconds=-difference.seconds,
            minutes=-difference.minutes,
            hours=-difference.hours,
            days=-difference.days
        ).humanize()

        status_embed = discord.Embed(
            colour=ColourCodes.theme_colour,
            description=f"websocket latency: **{latency} ms**"
        )
        status_embed.set_footer(text=f"kirby started up {uptime}")

        await ctx.send(embed=status_embed)


    @commands.command(aliases=["msgs", "totalmessages", "totalmsgs"])
    @commands.guild_only()
    async def messages(
        self, ctx: commands.Context, 
        *, member: Optional[discord.Member]
        ) -> discord.Embed:
        """
        shows how many messages a member has sent in the guild

        Returns
        -------
        `discord.Embed`
         an embed with info about the member's message count
        """

        await ctx.typing()

        member = member or ctx.author
        count: int = 0

        for channel in ctx.guild.text_channels:
            async for msg in channel.history(limit=None):
                if msg.author == member:
                    count += 1

        embed = discord.Embed(
            colour=ColourCodes.theme_colour,
            description=f"{member.mention} has sent **{count} messages** in total"
        )

        await ctx.send(embed=embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Utility(bot))
