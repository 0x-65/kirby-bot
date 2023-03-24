from textwrap import dedent
from typing import Any, Union

import discord

from discord.ext import commands

from utils.classes import ColourCodes, Emojis
from utils.paginator import StaticPaginator


class Booster(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot


    @commands.group(
        aliases=["bst"],
        invoke_without_command=True
        )
    @commands.guild_only()
    async def booster(
        self, ctx: commands.Context) -> Any:
        """
        booster module to create booster roles

        Returns
        -------
        `Any`
         the help command for the booster group
        """        

        if not ctx.invoked_subcommand:
            await ctx.send_help(ctx.command)


    @booster.command(aliases=["list"])
    async def roles(self, ctx: commands.Context) -> discord.Embed:
        """
        shows a list of the current booster roles in a guild

        Returns
        -------
        `discord.Embed`
         an embed with a list of the booster roles
        """

        users = await self.bot.db.fetch(
        """
        SELECT guild, member, role
        FROM boosters WHERE guild = $1
        """, ctx.guild.id)

        count: int = 0
        br_info: str = ""
        roles: list[str] = []

        if users:
            for table in users:
                member = ctx.guild.get_member(table.get("member"))
                role = ctx.guild.get_role(int(table.get("role")))
                if member and role != None:
                    count += 1

                    embed = discord.Embed(color=ColourCodes.theme_colour)

                    embed.set_author(
                        name=f"booster roles in {ctx.guild.name}", 
                        icon_url="https://cdn.discordapp.com/emojis/906895528023949372.webp")

                    br_info = f"`{count}.` **{member.mention}** **role:** {role.mention}"
                    roles.append(br_info)

            buttons = StaticPaginator(
                roles,
                line_limit=10,
                base_embed=discord.Embed(
                        color=ColourCodes.theme_colour
                        ).set_author(
                            name=f"booster roles in {ctx.guild.name}", 
                            icon_url="https://cdn.discordapp.com/emojis/906895528023949372.webp")
                        )

            embeds = buttons.get_page(1)
            await ctx.send(embeds=embeds, view=buttons)
        else:
            wrn_embed = discord.Embed(
                description=f"{Emojis.warning} no booster roles **found**",
                colour=ColourCodes.warning_colour)
            await ctx.send(embed=wrn_embed) 


    @booster.command(aliases=["br", "createrole"])
    @commands.guild_only()
    async def role(
        self, ctx: commands.Context,
        hexcode: Union[discord.Color, int, None], *,
        role_name: str
        ) -> discord.Embed:
        """ creates a custom booster role """

        data = await self.bot.db.fetch(
        """
        SELECT member
        FROM boosters""")

        hexcode = hexcode or discord.Color.default()
        booster_role = ctx.guild.premium_subscriber_role

        for table in data:
            user = table.get("member")

            if int(user) == ctx.author.id:
                embed = discord.Embed(
                    color=ColourCodes.warning_colour,
                    description=f"{Emojis.warning} **{str(ctx.author)}** you already created a **custom role**")

                embed.set_footer(text="you can only create one custom role to prevent spam")
                return await ctx.send(embed=embed)

        if booster_role in ctx.author.roles:
            await ctx.typing(ephemeral=True)

            created_role = await ctx.guild.create_role(name=role_name, colour=hexcode)
            await created_role.edit(position=booster_role.position)
            await ctx.author.add_roles(created_role)

            await self.bot.db.execute(
            """
            INSERT INTO boosters (role, member, guild)
            VALUES ($1, $2, $3)
            """, created_role.id, ctx.author.id, ctx.guild.id)

            embed = discord.Embed(
                colour=ColourCodes.success_colour,
                description=f"{Emojis.success} you were assigned a **booster role** with the colour `{hexcode}`")
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                colour=ColourCodes.warning_colour,
                description=f"{Emojis.warning} you need to be a **booster** to use this command")
            await ctx.send(embed=embed)


    @booster.command(aliases=["delete", "del"])
    @commands.guild_only()
    async def remove(self, ctx: commands.Context) -> discord.Embed:
        """ deletes your booster role """

        data = await self.bot.db.fetch(
        """
        SELECT member, role
        FROM boosters 
        WHERE guild = $1
        """, ctx.guild.id)

        for table in data:
            role = ctx.guild.get_role(int(table.get("role")))

            if int(table.get("member")) == ctx.author.id:
                await ctx.typing(ephemeral=True)

                await self.bot.db.execute(
                    "DELETE FROM boosters WHERE member = $1",
                    ctx.author.id)
                await role.delete()

                embed = discord.Embed(
                    colour=ColourCodes.success_colour,
                    description=f"{Emojis.success} your **booster role** in this server has been `deleted`")

                await ctx.send(embed=embed)


    @booster.command(aliases=["name", "rn"])
    @commands.guild_only()
    async def rename(
        self, ctx: commands.Context, *, name: str
        ) -> discord.Embed:
        """ updates your booster role"s name """

        data = await self.bot.db.fetch(
        """
        SELECT member, role
        FROM boosters 
        WHERE guild = $1
        """, ctx.guild.id)

        for table in data:
            role = ctx.guild.get_role(int(table.get("role")))

            if int(table.get("member")) == ctx.author.id:
                await ctx.typing(ephemeral=True)
                await role.edit(name=name)

                embed = discord.Embed(
                    colour=ColourCodes.success_colour,
                    description=f"{Emojis.success} updated the **name** of your `booster role`")

                await ctx.send(embed=embed)


    @booster.command(aliases=["colour", "color", "clr"])
    @commands.guild_only()
    async def reclr(
        self, ctx: commands.Context, 
        hexcode: Union[discord.Color, int, None] = None
        ) -> discord.Embed:
        """ updates your booster role"s colour """

        data = await self.bot.db.fetch(
        """
        SELECT member, role
        FROM boosters 
        WHERE guild = $1
        """, ctx.guild.id)

        hexcode = hexcode or discord.Color.default()

        for table in data:
            role = ctx.guild.get_role(int(table.get("role")))

            if int(table.get("member")) == ctx.author.id:
                await ctx.typing(ephemeral=True)
                await role.edit(colour=hexcode)

                embed = discord.Embed(
                    colour=ColourCodes.success_colour,
                    description=f"{Emojis.success} updated the **colour** of your `booster role`")

                await ctx.send(embed=embed)


    @booster.command(aliases=["icn", "ri"])
    @commands.guild_only()
    async def icon(
        self, ctx: commands.Context,
        icon: Union[discord.Emoji, discord.PartialEmoji, str]
        ) -> discord.Embed:
        """ adds a role icon to your booster role """

        data = await self.bot.db.fetch(
        """
        SELECT member, role
        FROM boosters WHERE guild = $1
        """, ctx.guild.id)

        if isinstance(icon, str):
            str(icon)
        else:
            icon = await icon.read()

        for table in data:
            role = ctx.guild.get_role(int(table.get("role")))

            if int(table.get("member")) == ctx.author.id:
                await ctx.typing(ephemeral=True)
                await role.edit(display_icon=icon)

                embed = discord.Embed(
                    colour=ColourCodes.success_colour,
                    description=f"{Emojis.success} updated the **icon** of your `booster role`")

                await ctx.send(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Booster(bot))
