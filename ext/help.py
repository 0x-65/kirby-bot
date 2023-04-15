from textwrap import dedent

import datetime
import discord

from discord.ext import commands
from reactionmenu import ViewMenu, ViewButton
from utils.classes import ColourCodes, Emojis


class KirbyHelp(commands.HelpCommand):
    def __init__(self):
        cmd_attrs = {
            "cooldown": commands.CooldownMapping.from_cooldown(
                4.0, 15.0, commands.BucketType.user),
            "aliases": ["cmds", "commands", "cmdlist"],
        }
        super().__init__(command_attrs=cmd_attrs)


    async def send_bot_help(self, mapping):
        """ triggers when `<prefix>help` is called"""

        bot = self.context.bot
        bot_avatar = self.context.bot.user.avatar
        prefix = self.context.clean_prefix

        help_embeds: list = []
        restricted_cogs: list[str] = [
                "Help", "Ticket", "ColourButtons", "ErrorHandler",
                "Developer", "Events", "Jishaku", "AutoPayment"
                ]

        module_emojis: dict = {
            "utility":  "https://cdn.discordapp.com/emojis/1058102343498993775.webp",
            "mod":      "https://cdn.discordapp.com/emojis/1058102336507084880.webp",
            "misc":     "https://cdn.discordapp.com/emojis/1058102331587170344.webp",
            "economy":  "https://cdn.discordapp.com/emojis/1077954962325250118.webp",
            "roblox":   "https://cdn.discordapp.com/emojis/1059207597544190032.webp",
            "server":   "https://cdn.discordapp.com/emojis/1085978665151627446.webp",
            "info":     "https://cdn.discordapp.com/emojis/1085978653768286278.webp",
            "booster":  "https://cdn.discordapp.com/emojis/906895528023949372.webp",
        }

        cmds: list = list(bot.walk_commands())
        menu = ViewMenu(self.context, menu_type=ViewMenu.TypeEmbed)

        help_embeds.append(discord.Embed(
            colour=ColourCodes.theme_colour,
            description=dedent(f"""
            `{prefix}help cmd` for info on a command
            `{prefix}help module` for info on a module

            `+` prefixs: `{prefix}` or {bot.user.mention}
            `+` cmd count: `{len(cmds)}`""")

        ).set_thumbnail(url=bot_avatar
        ).set_footer(text=f"developed by {str(bot.application.owner)}"
        ).set_author(
            name="main menu",
            icon_url="https://cdn.discordapp.com/emojis/1058804991357358080.webp"
            )
        )

        for cog, commands in mapping.items():
            if filtered_commands := await self.filter_commands(commands):

                if cog and cog.qualified_name not in restricted_cogs:
                    if cog.qualified_name == "Booster" or "Roblox":
                        filtered_commands = cog.walk_commands()

                    lower_cog_name = str(cog.qualified_name).lower()

                    if lower_cog_name in module_emojis.keys():
                        emoji = module_emojis.get(lower_cog_name)

                    name: str = cog.qualified_name

                    help_embeds.append(
                        discord.Embed(
                            colour=ColourCodes.theme_colour,
                            description=", ".join(f"`{c}`" for c in filtered_commands)

                        ).set_thumbnail(url=bot_avatar
                        ).set_author(
                            name=f"{name.lower()} module",
                            icon_url=emoji
                                )
                            )

        menu.add_pages(help_embeds)

        first_page_button = ViewButton(
            style=discord.ButtonStyle.secondary, emoji=Emojis.first_page,
            custom_id=ViewButton.ID_GO_TO_FIRST_PAGE)

        back_button = ViewButton(
            style=discord.ButtonStyle.secondary, emoji=Emojis.previous_page, 
            custom_id=ViewButton.ID_PREVIOUS_PAGE)

        stop_button = ViewButton(
            style=discord.ButtonStyle.secondary, emoji=Emojis.stop, 
            custom_id=ViewButton.ID_END_SESSION)

        next_button = ViewButton(
            style=discord.ButtonStyle.secondary, emoji=Emojis.next_page,
            custom_id=ViewButton.ID_NEXT_PAGE)

        last_page_button = ViewButton(
            style=discord.ButtonStyle.secondary, emoji=Emojis.last_page,
            custom_id=ViewButton.ID_GO_TO_LAST_PAGE)

        menu.add_button(first_page_button)
        menu.add_button(back_button)
        menu.add_button(stop_button)
        menu.add_button(next_button)
        menu.add_button(last_page_button)

        await menu.start()


    async def send_command_help(self, command: commands.Command):
        """ triggers when `<prefix>help <command>` is called"""

        bot_avatar = self.context.bot.user.avatar
        author = self.context.author
        prefix = self.context.clean_prefix

        if not command.hidden:
            aliases = command.aliases

            embed = discord.Embed( 
                colour=ColourCodes.theme_colour,
                timestamp=datetime.datetime.now())

            embed.set_footer(text=f"executed by @{author}")
            embed.set_author(name=f"module: {command.cog_name.lower()}", icon_url=bot_avatar)

            if aliases: value = ", ".join(f"`{alias}`" for alias in aliases)
            else: value = "`none`"

            embed.add_field(name="command", value=f"`{command.name}`", inline=True)
            embed.add_field(name="aliases", value=value, inline=True)
            embed.add_field(name="information", value=dedent(
                            f"""
                            ```
                            about: {command.short_doc}
                            cooldown: {command.cooldown.per / command.cooldown.rate} secs
                            usage: {prefix}{command.name} {command.signature
                                                                .replace("=None", "")
                                                                .replace("[]", "()")}
                            ```
                            """), inline=False)

            channel = self.get_destination()
            await channel.send(embed=embed)


    async def send_group_help(self, group: commands.Group):
        """ triggers when `<prefix>help <group>` is called"""

        bot_avatar = self.context.bot.user.avatar
        author = self.context.author

        if not group.hidden:
            cmds = group.commands

            embed = discord.Embed(
                colour=ColourCodes.theme_colour,
                timestamp=datetime.datetime.now())

            embed.set_footer(text=f"executed by @{author}")
            embed.set_author(name=f"module: {group.cog_name.lower()}", icon_url=bot_avatar)

            if cmds: value = ", ".join(f"`{cmd.name}`" for cmd in cmds)
            else: value = f"{Emojis.warning} **no cmds** in this group"

            embed.add_field(name="group", value=f"`{group.name}`", inline=True)
            embed.add_field(name="subcommands", value=value, inline=True)
            embed.add_field(name="information", value=dedent(
                            f"""
                            ```
                            about: {group.short_doc}
                            cooldown: {group.cooldown.per / group.cooldown.rate} secs per cmd
                            usage: {group.usage}```"""), inline=False)

            channel = self.get_destination()
            await channel.send(embed=embed)


    async def on_help_command_error(
        self, ctx: commands.Context, 
        error: commands.CommandError
        ):
        """ help command error handler """

        if isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(
                colour=ColourCodes.theme_colour,
                description=f"{Emojis.warning} **cooling down.. try again in `{round(error.retry_after)}` secs**")
            return await ctx.reply(embed=embed, mention_author=False)


class Help(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

        help_command = KirbyHelp()
        help_command.cog = self
        bot.help_command = help_command


async def setup(bot: commands.Bot):
    await bot.add_cog(Help(bot))
