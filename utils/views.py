import discord

from utils.classes import ColourCodes, Emojis


class Confirmation(discord.ui.View):
    """ confirmation menu for commands that could be used maliciously """

    def __init__(self):
        super().__init__(timeout=90)
        self.value = None

    @discord.ui.button(
        label="confirm",
        emoji=f"{Emojis.success}",
        style=discord.ButtonStyle.green)

    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):        
        if not interaction.user.resolved_permissions.administrator:
            warning_embed = discord.Embed(
                colour=ColourCodes.warning_colour,
                description=f"{Emojis.warning} you are not **an admin**"
                )
            return await interaction.response.send_message(
                embed=warning_embed, ephemeral=True)

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
        if not interaction.user.resolved_permissions.administrator:
            warning_embed = discord.Embed(
                colour=ColourCodes.warning_colour,
                description=f"{Emojis.warning} you are not **an admin**"
                )
            return await interaction.response.send_message(
                embed=warning_embed, ephemeral=True)

        self.value = False

        for child in self.children:
            child.disabled=True

        embed = discord.Embed(
            colour=ColourCodes.success_colour,
            description=f"{Emojis.success} cancelling...")
        await interaction.response.edit_message(embed=embed, view=self)

        self.stop()
