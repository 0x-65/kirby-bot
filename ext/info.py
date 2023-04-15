import os
import datetime

from textwrap import dedent
from typing import Optional
from psutil import cpu_percent, virtual_memory
from dateutil.relativedelta import relativedelta

import discord

from arrow import utcnow
from discord.ext import commands

from utils.classes import ColourCodes, Emojis
from utils.functions import line_count, better_numbers


class ChannelInfo(discord.ui.View):
    """ link to jump to the requested channel"""

    def __init__(self) -> None:
        super().__init__(timeout=90)


_cooldown = commands.CooldownMapping.from_cooldown(
    4.0, 15.0, commands.BucketType.user)


class Info(
    commands.Cog, command_attrs={"cooldown": _cooldown}
    ):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.start_time = utcnow()


    @commands.command(aliases=["whois", "ui", "wi", "uinfo"])
    @commands.guild_only()
    async def userinfo(
        self, ctx: commands.Context, *, member: Optional[discord.Member]
        ) -> discord.Embed:
        """
        shows info about a member

        Parameters
        ----------
        `member`: Optional[discord.Member]
         the member to get the info of (defaults to ctx.author)

        Returns
        -------
        `discord.Embed`
         an embed with info about the member
        """

        member = member or ctx.author
        joined_r_format = discord.utils.format_dt(member.joined_at, style="R")
        joined_d_format = discord.utils.format_dt(member.joined_at, style="D")
        created_r_format = discord.utils.format_dt(member.created_at, style="R")
        created_d_format = discord.utils.format_dt(member.created_at, style="D")

        embed = discord.Embed(
            title=f"{member.name}'s info",
            colour=ColourCodes.theme_colour,
            timestamp=datetime.datetime.now())

        embed.add_field(
            name="info",
            value=dedent(f"""
            **display name:** `{member.display_name}`
            **username:** `{member}`
            **ID:** `{member.id}`"""),
            inline=False)

        embed.add_field(
            name="dates",
            value=dedent(f"""
            **created:** {created_d_format} | {created_r_format}
            **joined:** {joined_d_format} | {joined_r_format}"""),
            inline=False)

        embed.add_field(
            name="platform",
            value=dedent(f"""
            {Emojis.mobile} **mobile:** `{member.mobile_status}`
            {Emojis.desktop} **desktop**: `{member.desktop_status}`
            {Emojis.web} **web:** `{member.web_status}`"""),
            inline=False)

        embed.set_footer(text=f"{len(member.mutual_guilds)} guild(s)")
        embed.set_thumbnail(url=member.display_avatar)

        await ctx.send(embed=embed)


    @commands.command(aliases=["sinfo", "guildinfo"])
    @commands.guild_only()
    async def serverinfo(
        self, ctx: commands.Context, 
        *, guild: Optional[discord.Guild]
        ) -> discord.Embed:
        """
        shows info about a guild

        Parameters
        ----------
        `guild`: Optional[discord.Guild]
         the guild to get the info of (defaults to ctx.guild)

        Returns
        -------
        `discord.Embed`
         an embed with info about the guild
        """

        guild = ctx.guild or guild

        created_r_format = discord.utils.format_dt(guild.created_at, style="R")
        created_d_format = discord.utils.format_dt(guild.created_at, style="D")

        boost_count: int = guild.premium_subscription_count
        boost_level: int = guild.premium_tier


        embed = discord.Embed(
            colour=ColourCodes.theme_colour,
            description=f"**created on** {created_d_format} ({created_r_format})",
            timestamp=datetime.datetime.now())

        embed.add_field(
            name="info",
            value=dedent(f"""
            **owner:** `{guild.owner}`
            **member count:** `{better_numbers(guild.member_count)}`
            """),
            )

        embed.add_field(
            name="levels",
            value=dedent(f"""
            **nsfw:** `{guild.nsfw_level.name}`
            **verification:** `{guild.verification_level}`
            """),
            )

        embed.add_field(
            name="boost",
            value=dedent(f"""
            **boost count:** `{boost_count}`
            **boost level:** `{boost_level}/3`
            """),
            )

        embed.add_field(
            name="count",
            value=dedent(f"""
            **roles:** `{len(guild.roles)}`
            **emojis**: `{len(guild.emojis)}`
            """),
            )

        embed.set_thumbnail(url=guild.icon)
        embed.set_footer(text=f"ID: {guild.id}")
        embed.set_author(name=f"{guild.name}'s info", icon_url=guild.icon)

        try:
            await ctx.send(embed=embed)
        except discord.errors.NotFound:
            await ctx.send("invalid server ID")


    @commands.command(aliases=["binfo"])
    @commands.guild_only()
    async def boostinfo(self, ctx: commands.Context) -> discord.Embed:
        """
        shows statistics about the guild"s boosts

        Returns
        -------
        `discord.Embed`
         an embed with statistics about the guild"s boosts
        """

        boosters: int = len(ctx.guild.premium_subscribers)
        boost_count: int = ctx.guild.premium_subscription_count
        booost_level: int = ctx.guild.premium_tier

        embed = discord.Embed(
            colour=ColourCodes.booster_colour,
            description=dedent(f"""
            `+` **boosters:** `{boosters}`
            `+` **boost count:** `{boost_count}`
            `+` **boost level:** `{booost_level}`"""))

        embed.set_author(
            name="boost info",
            icon_url="https://cdn.discordapp.com/emojis/906895528023949372.webp")

        embed.set_thumbnail(url=ctx.guild.icon)
        embed.set_footer(text=f"executed by @{ctx.author.name}")
        await ctx.send(embed=embed)


    @commands.command(aliases=["cinfo"])
    async def channelinfo(
        self, ctx: commands.Context, *,
        channel: Optional[discord.abc.GuildChannel]
        ) -> discord.Embed:
        """
        shows info about a channel

        Parameters
        ----------
        `channel`: Optional[discord.abc.GuildChannel]
         the channel to get the info of

        Returns
        -------
        `discord.Embed`
         an embed with info about the channel
        """

        view = ChannelInfo()
        channel = channel or ctx.channel

        view.add_item(discord.ui.Button(
            label='go to channel',
            style=discord.ButtonStyle.link,
            url=channel.jump_url))

        embed = discord.Embed(
            title=f"{channel.name} info",
            colour=ColourCodes.theme_colour)

        embed.set_footer(text=f"ID: {channel.id}")

        embed.add_field(
            name="Info",
            value=dedent(f"""
            **name:** `{channel.name}`
            **created:** {discord.utils.format_dt(channel.created_at, "R")}
            **type:** `{channel.type}`"""),
            inline=True)

        embed.add_field(
            name="Misc",
            value=dedent(f"""
            **topic:** `{channel.topic if channel.topic else "none"}`
            **position:** `{channel.position}/{len(ctx.guild.text_channels)}`
            **category:** `{channel.category.name}`"""),
            inline=True)

        await ctx.send(embed=embed, view=view)


    @commands.command(aliases=["rinfo"])
    async def roleinfo(
        self, ctx: commands.Context, *,
        role: Optional[discord.Role]
        ) -> discord.Embed:
        """
        shows info about a role

        Parameters
        ----------
        `role`: Optiona[discord.Role]
         the role to get the info of (defaults to the author's top role)

        Returns
        -------
        `discord.Embed`
         an embed with info about the role
        """

        role = role or ctx.author.top_role

        embed = discord.Embed(
            title=f"{role.name} info",
            colour=role.colour or ColourCodes.theme_colour)

        embed.set_footer(text=f"ID: {role.id} | {len(role.members)} members")

        #fix
        if role.display_icon:
            embed.set_thumbnail(url=role.display_icon.url)

        embed.add_field(
            name="Info",
            value=dedent(f"""
            **name:** `{role.name}`
            **created:** {discord.utils.format_dt(role.created_at, "R")}
            **colour:** `#{hex(role.colour.value)[2:].zfill(6)}`"""),
            inline=True)

        embed.add_field(
            name="Misc",
            value=dedent(f"""
            **position:** `{len(ctx.guild.roles) - role.position}/{len(ctx.guild.roles)}`
            **is hoisted:** `{'true' if role.hoist else 'false'}`
            **is mentionable:** `{'true' if role.mentionable else 'false'}`
            """),
            inline=True)

        await ctx.send(embed=embed)


    @commands.command(aliases=["einfo", "emoteinfo"])
    async def emojiinfo(
        self, ctx: commands.Context, emoji: discord.Emoji
        ) -> discord.Embed:
        """
        shows info about an emoji

        Parameters
        ----------
        `emoji`: discord.Emoji
         the emoji to get the info of

        Returns
        -------
        `discord.Embed`
         an embed with info about the emoji
        """

        embed = discord.Embed(
            title=f"{emoji.name} info",
            colour=ColourCodes.theme_colour)

        embed.set_thumbnail(url=emoji.url)
        embed.set_footer(text=f"ID: {emoji.id}")

        embed.add_field(
            name="Info",
            value=dedent(f"""
            **name:** `{emoji.name}`
            **created:** {discord.utils.format_dt(emoji.created_at, "R")}
            **guild:** `{emoji.guild.name}`"""),
            inline=True)

        embed.add_field(
            name="Misc",
            value=dedent(f"""
            **added by:** `{str(emoji.user) if emoji.user else 'unknown'}`
            **is animated:** `{'true' if emoji.animated else 'false'}`
            **is available:** `{'true' if emoji.available else 'false'}`
            """),
            inline=True)

        await ctx.send(embed=embed)


    @commands.command(aliases=["about", "info"])
    @commands.guild_only()
    async def botinfo(self, ctx: commands.Context) -> discord.Embed:
        """
        shows info & statistics about the bot

        Returns
        -------
        `discord.Embed`
         an embed with info about the bot's performance
        """

        difference = relativedelta(self.start_time - utcnow())
        os_name = "windows" if os.name == "nt" else "ubuntu"
        cmds = list(self.bot.walk_commands())

        uptime: str = self.start_time.shift(
            seconds=-difference.seconds,
            minutes=-difference.minutes,
            hours=-difference.hours,
            days=-difference.days
        ).humanize()

        embed = discord.Embed(colour=ColourCodes.theme_colour)
        embed.set_footer(text=f"kirby started up {uptime}")
        embed.set_thumbnail(url=self.bot.user.avatar)

        embed.add_field(name="usage", value=dedent(f"""
        {Emojis.latency} **latency:** `{round(self.bot.latency * 1000, 2)}ms`
        {Emojis.memory} **memory:** `{virtual_memory().percent}%`
        {Emojis.cpu} **cpu:** `{cpu_percent()}%`"""), inline=True)

        embed.add_field(name="system", value=dedent(f"""
        {Emojis.system} **sys:** `{os_name}`
        {Emojis.commands} **cmds:** `{len(cmds)}`
        {Emojis.lines} **lines:** `{line_count()}`"""), inline=False)

        await ctx.send(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Info(bot))
