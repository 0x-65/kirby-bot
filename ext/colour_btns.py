from textwrap import dedent
import discord

from discord.ext import commands
from utils.classes import Emojis, ColourCodes


class RedButtons(discord.ui.View):
    """ red colour buttons """

    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        style=discord.ButtonStyle.gray,
        row=1,
        emoji="<:e18:1038086484831522826>",
        custom_id="red1")

    async def first_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        role = discord.utils.get(interaction.guild.roles, id=875124063612309608)

        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            embed = discord.Embed(
                colour=ColourCodes.success_colour,
                description=f"{Emojis.success} {role.mention} successfully `removed`")
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            embed = discord.Embed(
                colour=ColourCodes.success_colour,
                description=f"{Emojis.success} {role.mention} successfully `added`")
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(
        style=discord.ButtonStyle.gray,
        row=1,
        emoji="<:e16:1038086481195044894",
        custom_id="red2")

    async def second_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        role = discord.utils.get(interaction.guild.roles, id=876586757653671937)

        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            embed = discord.Embed(
                colour=ColourCodes.success_colour,
                description=f"{Emojis.success} {role.mention} successfully `removed`")
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            embed = discord.Embed(
                colour=ColourCodes.success_colour,
                description=f"{Emojis.success} {role.mention} successfully `added`")
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(
        style=discord.ButtonStyle.gray,
        row=1,
        emoji="<:e17:1038086482855985183>",
        custom_id="red3")

    async def third_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        role = discord.utils.get(interaction.guild.roles, id=876586783364751360)

        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            embed = discord.Embed(
                colour=ColourCodes.success_colour,
                description=f"{Emojis.success} {role.mention} successfully `removed`")
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            embed = discord.Embed(
                colour=ColourCodes.success_colour,
                description=f"{Emojis.success} {role.mention} successfully `added`")
            await interaction.response.send_message(embed=embed, ephemeral=True)


class YellowButtons(discord.ui.View):
    """ yellow colour buttons """

    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        style=discord.ButtonStyle.gray,
        row=1,
        emoji="<:e19:1038086550665297971>",
        custom_id="yellow1")

    async def first_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        role = discord.utils.get(interaction.guild.roles, id=876586715299586149)

        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            embed = discord.Embed(
                colour=ColourCodes.success_colour,
                description=f"{Emojis.success} {role.mention} successfully `removed`")
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            embed = discord.Embed(
                colour=ColourCodes.success_colour,
                description=f"{Emojis.success} {role.mention} successfully `added`")
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(
        style=discord.ButtonStyle.gray,
        row=1,
        emoji="<:e20:1038086552699551834>",
        custom_id="yellow2")

    async def second_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        role = discord.utils.get(interaction.guild.roles, id=876586808912281671)
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            embed = discord.Embed(
                colour=ColourCodes.success_colour,
                description=f"{Emojis.success} {role.mention} successfully `removed`")
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            embed = discord.Embed(
                colour=ColourCodes.success_colour, 
                description=f"{Emojis.success} {role.mention} successfully `added`")
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(
        style=discord.ButtonStyle.gray,
        row=1,
        emoji="<:e21:1038086554440187904>",
        custom_id="yellow3")

    async def third_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        role = discord.utils.get(interaction.guild.roles, id=876586875102593024)
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            embed = discord.Embed(
                colour=ColourCodes.success_colour,
                description=f"{Emojis.success} {role.mention} successfully `removed`")
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            embed = discord.Embed(
                colour=ColourCodes.success_colour,
                description=f"{Emojis.success} {role.mention} successfully `added`")
            await interaction.response.send_message(embed=embed, ephemeral=True)


class GreenButtons(discord.ui.View):
    """ green colour buttons """

    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        style=discord.ButtonStyle.gray,
        row=1,
        emoji="<:e10:1038085753026130082>",
        custom_id="green1")

    async def first_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        role = discord.utils.get(interaction.guild.roles, id=876586844568059965)
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            embed = discord.Embed(
                colour=ColourCodes.success_colour,
                description=f"{Emojis.success} {role.mention} successfully `removed`")
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            embed = discord.Embed(
                colour=ColourCodes.success_colour,
                description=f"{Emojis.success} {role.mention} successfully `added`")
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(
        style=discord.ButtonStyle.gray,
        row=1,
        emoji="<:e11:1038085757404983396>",
        custom_id="green2")

    async def second_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        role = discord.utils.get(interaction.guild.roles, id=876586931121684480)
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            embed = discord.Embed(
                colour=ColourCodes.success_colour,
                description=f"{Emojis.success} {role.mention} successfully `removed`")
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            embed = discord.Embed(
                colour=ColourCodes.success_colour,
                description=f"{Emojis.success} {role.mention} successfully `added`")
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(
        style=discord.ButtonStyle.gray,
        row=1,
        emoji="<:e12:1038085759103668316>",
        custom_id="green3")

    async def third_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        role = discord.utils.get(interaction.guild.roles, id=876586903762251826)
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            embed = discord.Embed(
                colour=ColourCodes.success_colour,
                description=f"{Emojis.success} {role.mention} successfully `removed`")
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            embed = discord.Embed(
                colour=ColourCodes.success_colour,
                description=f"{Emojis.success} {role.mention} successfully `added`")
            await interaction.response.send_message(embed=embed, ephemeral=True)


class BlueButtons(discord.ui.View):
    """ blue colour buttons """

    def __init__(self):
        super().__init__(timeout=None)


    @discord.ui.button(
        style=discord.ButtonStyle.gray,
        row=1,
        emoji="<:e1:1038085623845756969>", 
        custom_id="blue1")

    async def first_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        role = discord.utils.get(interaction.guild.roles, id=876585125981347911)
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            embed = discord.Embed(
                colour=ColourCodes.success_colour,
                description=f"{Emojis.success} {role.mention} successfully `removed`")
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            embed = discord.Embed(
                colour=ColourCodes.success_colour,
                description=f"{Emojis.success} {role.mention} successfully `added`")
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(
        style=discord.ButtonStyle.gray,
        row=1,
        emoji="<:e2:1038085625519296613>",
        custom_id="blue2")

    async def second_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        role = discord.utils.get(interaction.guild.roles, id=876585268684136458)
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            embed = discord.Embed(
                colour=ColourCodes.success_colour,
                description=f"{Emojis.success} {role.mention} successfully `removed`")
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            embed = discord.Embed(
                colour=ColourCodes.success_colour,
                description=f"{Emojis.success} {role.mention} successfully `added`")
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(
        style=discord.ButtonStyle.gray,
        row=1,
        emoji="<:e3:1038085627473825832>",
        custom_id="blue3")

    async def third_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        role = discord.utils.get(interaction.guild.roles, id=876585424355721246)
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            embed = discord.Embed(
                colour=ColourCodes.success_colour,
                description=f"{Emojis.success} {role.mention} successfully `removed`")
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            embed = discord.Embed(
                colour=ColourCodes.success_colour,
                description=f"{Emojis.success} {role.mention} successfully `added`")
            await interaction.response.send_message(embed=embed, ephemeral=True)


class CyanButtons(discord.ui.View):
    """ cyan colour buttons """

    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        style=discord.ButtonStyle.gray,
        row=1,
        emoji="<:e5:1038085661976186921>",
        custom_id="cyan1")

    async def first_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        role = discord.utils.get(interaction.guild.roles, id=876585499588968508)
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            embed = discord.Embed(
                colour=ColourCodes.success_colour,
                description=f"{Emojis.success} {role.mention} successfully `removed`")
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            embed = discord.Embed(
                colour=ColourCodes.success_colour,
                description=f"{Emojis.success} {role.mention} successfully `added`")
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(
        style=discord.ButtonStyle.gray,
        row=1,
        emoji="<:e6:1038085663913955378>",
        custom_id="cyan2")

    async def second_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        role = discord.utils.get(interaction.guild.roles, id=876585366235267102)
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            embed = discord.Embed(
                colour=ColourCodes.success_colour,
                description=f"{Emojis.success} {role.mention} successfully `removed`")
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            embed = discord.Embed(
                colour=ColourCodes.success_colour,
                description=f"{Emojis.success} {role.mention} successfully `added`")
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(
        style=discord.ButtonStyle.gray,
        row=1,
        emoji="<:e4:1038085660332015667>", 
        custom_id="cyan3")

    async def third_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        role = discord.utils.get(interaction.guild.roles, id=876803172637765675)
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            embed = discord.Embed(
                colour=ColourCodes.success_colour,
                description=f"{Emojis.success} {role.mention} successfully `removed`")
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            embed = discord.Embed(
                colour=ColourCodes.success_colour,
                description=f"{Emojis.success} {role.mention} successfully `added`")
            await interaction.response.send_message(embed=embed, ephemeral=True)


class PurpleButtons(discord.ui.View):
    """ purple colour buttons """

    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        style=discord.ButtonStyle.gray,
        row=1,
        emoji="<:e15:1038086372940070963>",
        custom_id="purple1")

    async def first_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        role = discord.utils.get(interaction.guild.roles, id=876803175393411093)
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            embed = discord.Embed(
                colour=ColourCodes.success_colour,
                description=f"{Emojis.success} {role.mention} successfully `removed`")
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            embed = discord.Embed(
                colour=ColourCodes.success_colour,
                description=f"{Emojis.success} {role.mention} successfully `added`")
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(
        style=discord.ButtonStyle.gray,
        row=1,
        emoji="<:e13:1038086369710440508>",
        custom_id="purple2")

    async def second_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        role = discord.utils.get(interaction.guild.roles, id=876803178606239804)
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            embed = discord.Embed(
                colour=ColourCodes.success_colour,
                description=f"{Emojis.success} {role.mention} successfully `removed`")
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            embed = discord.Embed(
                colour=ColourCodes.success_colour,
                description=f"{Emojis.success} {role.mention} successfully `added`")
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(
        style=discord.ButtonStyle.gray,
        row=1,
        emoji="<:e14:1038086371312685087>",
        custom_id="purple3")

    async def third_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        role = discord.utils.get(interaction.guild.roles, id=876803181730988032)
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            embed = discord.Embed(
                colour=ColourCodes.success_colour,
                description=f"{Emojis.success} {role.mention} successfully `removed`")
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            embed = discord.Embed(
                colour=ColourCodes.success_colour,
                description=f"{Emojis.success} {role.mention} successfully `added`")
            await interaction.response.send_message(embed=embed, ephemeral=True)


class PinkButtons(discord.ui.View):
    """ pink colour buttons """

    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        style=discord.ButtonStyle.gray,
        row=1,
        emoji="<:e7:1038085681920098356>",
        custom_id="pink1")

    async def first_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        role = discord.utils.get(interaction.guild.roles, id=878000786968301639)
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            embed = discord.Embed(
                colour=ColourCodes.success_colour,
                description=f"{Emojis.success} {role.mention} successfully `removed`")
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            embed = discord.Embed(
                colour=ColourCodes.success_colour,
                description=f"{Emojis.success} {role.mention} successfully `added`")
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(
        style=discord.ButtonStyle.gray,
        row=1,
        emoji="<:e8:1038085683971100823>",
        custom_id="pink2")

    async def second_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        role = discord.utils.get(interaction.guild.roles, id=878000786985058325)
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            embed = discord.Embed(
                colour=ColourCodes.success_colour,
                description=f"{Emojis.success} {role.mention} successfully `removed`")
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            embed = discord.Embed(
                colour=ColourCodes.success_colour,
                description=f"{Emojis.success} {role.mention} successfully `added`")
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(
        style=discord.ButtonStyle.gray,
        row=1,
        emoji="<:e9:1038085685850144868>",
        custom_id="pink3")

    async def third_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        role = discord.utils.get(interaction.guild.roles, id=878000788683784302)
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            embed = discord.Embed(
                colour=ColourCodes.success_colour,
                description=f"{Emojis.success} {role.mention} successfully `removed`")
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            embed = discord.Embed(
                colour=ColourCodes.success_colour,
                description=f"{Emojis.success} {role.mention} successfully `added`")
            await interaction.response.send_message(embed=embed, ephemeral=True)


class NeutralButtons(discord.ui.View):
    """ neutral colour buttons """

    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        style=discord.ButtonStyle.gray,
        row=1,
        emoji="<:e24:1038086677769486346>",
        custom_id="neutral1")

    async def first_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        role = discord.utils.get(interaction.guild.roles, id=878000791284252722)
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            embed = discord.Embed(
                colour=ColourCodes.success_colour,
                description=f"{Emojis.success} {role.mention} successfully `removed`")
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            embed = discord.Embed(
                colour=ColourCodes.success_colour, 
                description=f"{Emojis.success} {role.mention} successfully `added`")
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(
        style=discord.ButtonStyle.gray,
        row=1,
        emoji="<:e22:1038086673763930132>",
        custom_id="neutral2")

    async def second_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        role = discord.utils.get(interaction.guild.roles, id=878000792274092063)
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            embed = discord.Embed(
                colour=ColourCodes.success_colour,
                description=f"{Emojis.success} {role.mention} successfully `removed`")
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            embed = discord.Embed(
                colour=ColourCodes.success_colour,
                description=f"{Emojis.success} {role.mention} successfully `added`")
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(
        style=discord.ButtonStyle.gray,
        row=1,
        emoji="<:e23:1038086675814944829>",
        custom_id="neutral3")

    async def third_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        role = discord.utils.get(interaction.guild.roles, id=878000793838567434)
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            embed = discord.Embed(
                colour=ColourCodes.success_colour,
                description=f"{Emojis.success} {role.mention} successfully `removed`")
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            embed = discord.Embed(
                colour=ColourCodes.success_colour,
                description=f"{Emojis.success} {role.mention} successfully `added`")
            await interaction.response.send_message(embed=embed, ephemeral=True)


class ColourButtons(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot


    @commands.command(hidden=True)
    @commands.is_owner()
    async def clrs(self, ctx: commands.Context):
        """ sets up the colour buttons """

        channel = ctx.guild.get_channel(1000760312066224128)

        async for msg in channel.history(limit=None):
            await msg.delete()

        red_embed = discord.Embed(
            colour=ColourCodes.invisible_colour,
            description=dedent("""
            `red`

            ・ <@&875124063612309608>
            ・ <@&876586757653671937>
            ・ <@&876586783364751360>
            """)
            )

        yellow_embed = discord.Embed(
            colour=ColourCodes.invisible_colour,
            description=dedent("""
            `yellow`

            ・ <@&876586715299586149>
            ・ <@&876586808912281671>
            ・ <@&876586875102593024>
            """)
            )

        green_embed = discord.Embed(
            colour=ColourCodes.invisible_colour,
            description=dedent("""
            `green`

            ・ <@&876586844568059965>
            ・ <@&876586931121684480>
            ・ <@&876586903762251826>
            """)
            )

        blue_embed = discord.Embed(
            colour=ColourCodes.invisible_colour,
            description=dedent("""
            `blue`

            ・ <@&876585125981347911>
            ・ <@&876585268684136458>
            ・ <@&876585424355721246>
            """)
            )

        cyan_embed = discord.Embed(
            colour=ColourCodes.invisible_colour,
            description=dedent("""
            `cyan`

            ・ <@&876585499588968508>
            ・ <@&876585366235267102>
            ・ <@&876803172637765675>
            """)
            )

        purple_embed = discord.Embed(
            colour=ColourCodes.invisible_colour,
            description=dedent("""
            `purple`

            ・ <@&876803175393411093>
            ・ <@&876803178606239804>
            ・ <@&876803181730988032>
            """)
            )

        pink_embed = discord.Embed(
            colour=ColourCodes.invisible_colour,
            description=dedent("""
            `pink`

            ・ <@&878000786968301639>
            ・ <@&878000786985058325>
            ・ <@&878000788683784302>
            """)
            )

        neutral_embed = discord.Embed(
            colour=ColourCodes.invisible_colour,
            description=dedent("""
            `neutral`

            ・ <@&878000791284252722>
            ・ <@&878000792274092063>
            ・ <@&878000793838567434>
            """)
            )

        clrs = [
            [red_embed, RedButtons()],
            [yellow_embed, YellowButtons()],
            [green_embed, GreenButtons()],
            [blue_embed, BlueButtons()],
            [cyan_embed, CyanButtons()],
            [purple_embed, PurpleButtons()],
            [pink_embed, PinkButtons()],
            [neutral_embed, NeutralButtons()]
        ]

        for item in clrs:
            await channel.send(embed=item[0], view=item[1])
        await ctx.message.add_reaction(Emojis.success)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(ColourButtons(bot))