from typing import Any, Union
import discord

from discord.ext import commands
from utils.classes import ColourCodes
from utils.paginator import StaticPaginator


_cooldown = commands.CooldownMapping.from_cooldown(
    4.0, 15.0, commands.BucketType.user)


class Server(
    commands.Cog, command_attrs={"cooldown": _cooldown}
    ):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot


    @commands.command(aliases=['mc'])
    @commands.guild_only()
    async def membercount(self, ctx: commands.Context) -> discord.Embed:
        """
        shows the amount of members in the guild

        Returns
        -------
        `discord.Embed`
         an embed with the number of members & bots
        """

        bot_count: int = 0
        member_count: int = 0

        for member in ctx.guild.members:
            member_count += 1

            if member.bot is True:
                bot_count += 1

        human_count: int = member_count - bot_count

        embed = discord.Embed(
            color=ColourCodes.theme_colour,
            description=f'**`{human_count}` members & `{bot_count}` bots**')

        embed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon)
        embed.set_footer(text=f'executed by @{ctx.author.name}')
        await ctx.send(embed=embed)


    @commands.command(aliases=['sexy'])
    @commands.guild_only()
    async def boosters(self, ctx: commands.Context) -> discord.Embed:
        """
        shows a list of the current boosters in the guild

        Returns
        -------
        `discord.Embed`
         an embed with a list of the current boosters
        """

        count: int = 0
        _booster: str = ""
        boosters: list = []
        booster_list = ctx.guild.premium_subscribers

        for booster in booster_list:
            count += 1
            since = discord.utils.format_dt(booster.premium_since, style='D')
            _booster = f"`{count}` {booster.mention} since {since}"
            boosters.append(_booster)

            buttons = StaticPaginator(
                boosters,
                line_limit=10,
                base_embed=discord.Embed(
                        color=ColourCodes.booster_colour
                        ).set_author(
                    name=f"{ctx.guild.name}'s boosters",
                    icon_url='https://cdn.discordapp.com/emojis/906895528023949372.webp')
                        )

        embeds = buttons.get_page(1)
        await ctx.send(embeds=embeds) if count <= 10 else await ctx.send(embeds=embeds, view=buttons)


    @commands.command(aliases=['sbanner', 'guildbanner'])
    @commands.guild_only()
    async def serverbanner(self, ctx: commands.Context) -> discord.Asset:
        """
        shows the guild's banner

        Returns
        -------
        `discord.Asset`
         the guild's banner asset
        """

        embed = discord.Embed(
            title=f"{ctx.guild.name}'s banner",
            url=f'{ctx.guild.banner}',
            color=ColourCodes.theme_colour)
        embed.set_image(url=ctx.guild.banner)

        try:
            await ctx.send(embed=embed)
        except discord.errors.NotFound:
            await ctx.send(f'**{ctx.guild.name}** does not have a server banner')


    @commands.command(aliases=['sicon', 'guildicon'])
    @commands.guild_only()
    async def servericon(self, ctx: commands.Context) -> discord.Asset:
        """
        shows the guild's icon

        Returns
        -------
        `discord.Asset`
         the guild's icon asset
        """

        embed = discord.Embed(
            title=f"{ctx.guild.name}'s icon",
            url=f'{ctx.guild.icon}',
            color=ColourCodes.theme_colour)
        embed.set_image(url=ctx.guild.icon)

        try:
            await ctx.send(embed=embed)
        except discord.errors.NotFound:
            await ctx.send(f'**{ctx.guild.name}** does not have a server icon')


    @commands.group(
        invoke_without_command=True,
        aliases=["emote"],
        usage="kirby emoji <command>")
    @commands.guild_only()
    @commands.has_permissions(manage_emojis=True)
    async def emoji(self, ctx: commands.Context) -> Any:
        """
        emoji module

        Returns
        -------
        `Any`
         the help command for emoji module
        """

        if not ctx.invoked_subcommand:
            await ctx.send_help(ctx.command)


    @emoji.command(aliases=["steal"])
    @commands.guild_only()
    @commands.has_permissions(manage_emojis=True)
    async def add(
        self, ctx: commands.Context, *, 
        emoji: Union[discord.Emoji, discord.PartialEmoji]
        ) -> discord.Embed:
        """
        creates a custom emoji in the guild

        Parameters
        ----------
        `emoji`: Union[discord.Emoji, discord.PartialEmoji]
         the emoji to add to the guild

        Returns
        -------
        `discord.Embed`
         an embed with info about the added emoji
        """        

        bytes_obj: bytes = await emoji.read()

        created_emoji = await ctx.guild.create_custom_emoji(
            name=emoji.name, image=bytes_obj)

        embed = discord.Embed(
            colour=ColourCodes.success_colour,
            description=f"{Emojis.success} **added** the emoji {created_emoji} to the `guild`")
        await ctx.send(embed=embed)


    @emoji.command(aliases=["remove"])
    @commands.guild_only()
    @commands.has_permissions(manage_emojis=True)
    async def delete(
        self, ctx: commands.Context, *, 
        emoji: Union[discord.Emoji, discord.PartialEmoji]
        ) -> discord.Embed:
        """
        deletes a custom emoji from the guild

        Parameters
        ----------
        `emoji`: Union[discord.Emoji, discord.PartialEmoji]
         the emoji to delete from the guild

        Returns
        -------
        `discord.Embed`
         an embed with info about the deleted emoji
        """ 

        embed = discord.Embed(
            colour=ColourCodes.success_colour,
            description=f"{Emojis.success} **deleted** the emoji {emoji} from the `guild`")
        await ctx.send(embed=embed)

        await ctx.guild.delete_emoji(emoji)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Server(bot))
