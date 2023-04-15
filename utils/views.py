import discord

from ext import EXTENSIONS
from utils.functions import restart_bot
from utils.classes import ColourCodes, Emojis


#massunban cmd buttons
class Confirmation(discord.ui.View):
    """ confirmation menu for commands that could be used maliciously """

    def __init__(self):
        super().__init__(timeout=90)
        self.value = None


    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.resolved_permissions.administrator:
            return True

        warning_embed = discord.Embed(
            colour=ColourCodes.theme_colour,
            description=f"{Emojis.warning} you are not **an admin**"
            )
        await interaction.response.send_message(
            embed=warning_embed, ephemeral=True)
        return False


    @discord.ui.button(
        label="confirm",
        emoji=f"{Emojis.success}",
        style=discord.ButtonStyle.green)

    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.value = True

        for child in self.children:
            child.disabled=True

        await interaction.response.edit_message(view=self)
        self.stop()


    @discord.ui.button(
        label="cancel",
        emoji=f"{Emojis.error}",
        style=discord.ButtonStyle.danger)

    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.value = False

        for child in self.children:
            child.disabled=True

        embed = discord.Embed(
            colour=ColourCodes.theme_colour,
            description=f"{Emojis.success} cancelling...")
        await interaction.response.edit_message(embed=embed, view=self)

        self.stop()

#export ticket confirmation
class ExportConfirmation(discord.ui.View):
    """ confirmation menu for close ticket command """

    def __init__(self):
        super().__init__(timeout=90)
        self.value = None


    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user == interaction.client.application.owner:
            return True

        warning_embed = discord.Embed(
            colour=ColourCodes.theme_colour,
            description=f"{Emojis.warning} you are not the **bot owner**"
            )
        await interaction.response.send_message(
            embed=warning_embed, ephemeral=True)
        return False


    @discord.ui.button(
        label="export",
        style=discord.ButtonStyle.green)

    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.value = True

        for child in self.children:
            child.disabled=True

        await interaction.response.edit_message(view=self)
        self.stop()


    @discord.ui.button(
        label="close",
        style=discord.ButtonStyle.danger)

    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.value = False

        for child in self.children:
            child.disabled=True

        embed = discord.Embed(
            colour=ColourCodes.theme_colour,
            description=f"{Emojis.success} closing...")
        await interaction.response.edit_message(embed=embed, view=self)

        self.stop()


#panel cmd buttons
class Panel(discord.ui.View):
    """ execute owner cmds via buttons """

    def __init__(self) -> None:
        super().__init__()
        self.value = None


    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user == interaction.client.application.owner:
            return True

        embed = discord.Embed(
            colour=ColourCodes.theme_colour,
            description=f"{Emojis.warning} you are not the **bot owner**")
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return False


    @discord.ui.button(
        label="1",
        row=1,
        style=discord.ButtonStyle.secondary
        )

    async def shutdown(
        self, interaction: discord.Interaction, button: discord.ui.Button
        ) -> discord.Embed:

        for child in self.children: 
            child.disabled=True

        embed = discord.Embed(
            colour=ColourCodes.theme_colour,
            description=f"{Emojis.success} **bot was shutdown**")

        await interaction.response.edit_message(embed=embed, view=self)
        self.stop()
        await interaction.client.close()


    @discord.ui.button(
        label="2",
        row=1,
        style=discord.ButtonStyle.secondary
        )

    async def restart(
        self, interaction: discord.Interaction, button: discord.ui.Button
        ) -> discord.Embed:

        for child in self.children:
            child.disabled=True

        extensions: str = f"\n├── {Emojis.success}".join(f"`{e}`" for e in EXTENSIONS)

        embed = discord.Embed(
            colour=ColourCodes.theme_colour,
            description=extensions)

        await interaction.response.edit_message(embed=embed, view=self)
        self.stop()
        restart_bot()


    @discord.ui.button(
        label="3",
        row=1,
        style=discord.ButtonStyle.secondary
        )

    async def guildlist(
        self, interaction: discord.Interaction, button: discord.ui.Button
        ) -> discord.Embed:

        count: int = 0
        guilds: str = ""
        button.disabled: bool = True

        guild_list = interaction.client.guilds

        for count, guild in enumerate(guild_list, start=1):
            guilds += f"`{count}` **{guild.name}** | `{guild.id}`\n"

            embed = discord.Embed(
                colour=ColourCodes.theme_colour,
                description=guilds)

            embed.set_author(
                name=f"server count: {len(guild_list)}",
                icon_url=interaction.client.user.avatar)

        if len(guild_list) <= 0:
            await interaction.response.send_message(
                content="no guilds found", ephemeral=True)
        else:
            await interaction.response.send_message(
                embed=embed, ephemeral=True)