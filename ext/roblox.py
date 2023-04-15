from typing import Any
from textwrap import dedent

import discord

from discord.ext import commands
from roblox import Client, AvatarThumbnailType

from utils.functions import better_numbers
from utils.classes import Emojis, ColourCodes


class RobloxLinks(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=90)


_cooldown = commands.CooldownMapping.from_cooldown(
    4.0, 15.0, commands.BucketType.user)


class Roblox(
    commands.Cog, command_attrs={"cooldown": _cooldown}
    ):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.client = Client()


    @commands.group(
        invoke_without_command=True,
        aliases=["rblx"],
        usage="kirby roblox <command>")
    @commands.guild_only()
    async def roblox(self, ctx: commands.Context) -> Any:
        """
        roblox module

        Returns
        -------
        `Any`
         the help command for roblox
        """

        if not ctx.invoked_subcommand:
            await ctx.send_help(ctx.command)


    @roblox.command(aliases=["player"])
    @commands.guild_only()
    async def user(
        self, ctx: commands.Context, *, user: int
        ) -> discord.Embed:
        """
        shows info about a roblox user

        Parameters
        ----------
        `user`: int
         the id of the user to get the info of
        
        Returns
        -------
        `discord.Embed`
         an embed with info about the user
        """

        view = RobloxLinks()
        user = await self.client.get_user(user)
        user_thumbnails = await self.client.thumbnails.get_user_avatar_thumbnails(
            users=[user],
            type=AvatarThumbnailType.full_body,
            size=(420, 420))

        if len(user_thumbnails) > 0:
            user_thumbnail = user_thumbnails[0]

        view.add_item(discord.ui.Button(
            label="profile",
            emoji=f"{Emojis.roblox}",
            style=discord.ButtonStyle.link,
            url=f"https://www.roblox.com/users/{user.id}/profile"))

        embed = discord.Embed(colour=ColourCodes.roblox_colour)

        embed.set_thumbnail(url=user_thumbnail.image_url)
        embed.set_footer(text=f"ID: {user.id}")
        embed.set_author(
            name="roblox user",
            icon_url="https://cdn.discordapp.com/emojis/1059207597544190032.webp")

        embed.add_field(
            name="Info",
            value=dedent(f"""
            **name: `{user.name}`
            display name: `{user.display_name}`
            created:** {discord.utils.format_dt(user.created, style="R")}"""))

        embed.add_field(
            name="Misc",
            value=dedent(f"""
            **follower count: `{better_numbers(await user.get_follower_count())}`
            following count: `{better_numbers(await user.get_following_count())}`
            friends count:** `{better_numbers(await user.get_friend_count())}`"""))

        await ctx.send(embed=embed, view=view)


    @roblox.command()
    @commands.guild_only()
    async def group(
        self, ctx: commands.Context, *, group: int
        ) -> discord.Embed:
        """
        shows info about a roblox group

        Parameters
        ----------
        `group`: int
         the id of the group to get the info of

        Returns
        -------
        `discord.Embed`
         an embed with info about the group
        """

        view = RobloxLinks()
        group = await self.client.get_group(group)
        group_thumbnails = await self.client.thumbnails.get_group_icons(
            groups=[group],
            size=(420, 420))

        if len(group_thumbnails) > 0:
            group_thumbnail = group_thumbnails[0]

        view.add_item(discord.ui.Button(
            label="group",
            emoji=f"{Emojis.roblox}",
            style=discord.ButtonStyle.link,
            url=f"https://www.roblox.com/groups/{group.id}"))

        embed = discord.Embed(colour=ColourCodes.roblox_colour)

        embed.set_thumbnail(url=group_thumbnail.image_url)
        embed.set_footer(text=f"ID: {group.id}")
        embed.set_author(
            name="roblox group",
            icon_url="https://cdn.discordapp.com/emojis/1059207597544190032.webp")

        embed.add_field(
            name="Info",
            value=dedent(f"""
            **name:** `{group.name}`
            **owner:** `{group.owner.name}`
            **membercount:** `{better_numbers(group.member_count)}`"""))

        embed.add_field(
            name="Extra",
            value=dedent(f"""
            **is locked:** `{group.is_locked}`
            **public entry allowed:** `{group.public_entry_allowed}`"""))

        if group.shout.body:
            embed.add_field(
                name="shout",
                value=f"```{group.shout.body}```",
                inline=False)

        await ctx.send(embed=embed, view=view)


    @roblox.command()
    @commands.guild_only()
    async def badge(
        self, ctx: commands.Context, *, badge: int
        ) -> discord.Embed:
        """
        shows info about a roblox badge

        Parameters
        ----------
        `badge`: int
         the id of the badge to get the info of

        Returns
        -------
        `discord.Embed`
         an embed with info about the badge
        """

        view = RobloxLinks()
        badge = await self.client.get_badge(badge)
        badge_thumbnails = await self.client.thumbnails.get_badge_icons(
            badges=[badge],
            size=(150, 150))

        if len(badge_thumbnails) > 0:
            badge_thumbnail = badge_thumbnails[0]

        view.add_item(discord.ui.Button(
            label="badge",
            emoji=f"{Emojis.roblox}",
            style=discord.ButtonStyle.link,
            url=f"https://www.roblox.com/badges/{badge.id}"))

        embed = discord.Embed(colour=ColourCodes.roblox_colour)

        embed.set_thumbnail(url=badge_thumbnail.image_url)
        embed.set_footer(text=f"ID: {badge.id}")
        embed.set_author(
            name="roblox badge",
            icon_url="https://cdn.discordapp.com/emojis/1059207597544190032.webp")

        embed.add_field(
            name="Info",
            value=dedent(f"""
            **name:** `{badge.name}`
            **created:** {discord.utils.format_dt(badge.created, style="R")}
            **updated:** {discord.utils.format_dt(badge.updated, style="R")}
            """))

        embed.add_field(
            name="Extra",
            value=dedent(f"""
            **game:** `{badge.awarding_universe.name}`
            **all time awarded:** `{better_numbers(badge.statistics.awarded_count)}`
            **is enabled:** `{badge.enabled}`
            """))

        await ctx.send(embed=embed, view=view)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Roblox(bot))
