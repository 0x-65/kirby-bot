import datetime

from os import remove
from typing import Any
from textwrap import dedent

import discord
import chat_exporter

from discord import ui
from discord.ext import commands

from utils.classes import Config, Emojis, ColourCodes


SEPERATOR: str = "`+`"


class BotInfo(ui.Modal, title="custom bot"):
    name = ui.TextInput(label="bot type (modmail, moderation, etc)")
    answer = ui.TextInput(
        label="bot info", 
        style=discord.TextStyle.paragraph, 
        min_length=100)

    async def on_submit(self, interaction: discord.Interaction):
        view = FormButtons()
        view.remove_item(view.form_fillout)

        overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(
                read_messages=False),
            interaction.guild.me : discord.PermissionOverwrite(
                view_channel=True, read_messages=True),
            interaction.user: discord.PermissionOverwrite(
                read_messages=True, send_messages=True,
                attach_files=True, embed_links=True)
        }

        embed = discord.Embed(
            colour=ColourCodes.theme_colour,
            title=f"{self.name.value}",
            description=dedent(f"""
            if you forgot or missed something, type it in chat

            **bot information:**
            {self.answer.value}"""),
            timestamp=datetime.datetime.now())

        embed.set_footer(text=f"client: {str(interaction.user)}")
        embed.set_thumbnail(url=interaction.user.avatar),

        await interaction.response.edit_message(
            content="you may type now", embed=embed, view=view)
        await interaction.channel.edit(overwrites=overwrites)


class UpdateInfo(ui.Modal, title="update"):
    answer = ui.TextInput(
        label="provide details about the update for your bot", 
        style=discord.TextStyle.paragraph)

    async def on_submit(self, interaction: discord.Interaction):
        ticket_name = f"update-{interaction.user.name}"

        ticket_category = discord.utils.get(
            interaction.guild.categories, id=1066848157918576651)

        overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(
                read_messages=False),
            interaction.guild.me : discord.PermissionOverwrite(
                view_channel=True, read_messages=True),
            interaction.user: discord.PermissionOverwrite(
                read_messages=True, send_messages=True,
                attach_files=True, embed_links=True)
        }

        creation = await interaction.guild.create_text_channel(
            ticket_name, overwrites=overwrites, category=ticket_category)

        embed = discord.Embed(
            colour=ColourCodes.success_colour,
            description=f"{Emojis.success} **ticked created**: {creation.mention}")
        
        await interaction.response.send_message(embed=embed, ephemeral=True)

        embed = discord.Embed(
            colour=ColourCodes.theme_colour,
            description=dedent(f"""
            the dev will be here shortly, please be patient
            
            **update information**
            {self.answer.value}"""),
            timestamp=datetime.datetime.now())

        embed.set_footer(text=f"client: {str(interaction.user)}")
        embed.set_thumbnail(url=interaction.user.avatar)

        await creation.send("<@&906656381115973632>", embed=embed)


class InquiryInfo(ui.Modal, title="inquiry"):
    answer = ui.TextInput(
        label="provide details about your inquiry:", 
        style=discord.TextStyle.paragraph,
        min_length=30)

    async def on_submit(self, interaction: discord.Interaction):
        ticket_name = f"inquiry-{interaction.user.name}"

        ticket_category = discord.utils.get(
            interaction.guild.categories, id=1066848157918576651)

        overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(
                read_messages=False),
            interaction.guild.me : discord.PermissionOverwrite(
                view_channel=True, read_messages=True),
            interaction.user: discord.PermissionOverwrite(
                read_messages=True, send_messages=True,
                attach_files=True, embed_links=True)
        }

        creation = await interaction.guild.create_text_channel(
            ticket_name, overwrites=overwrites, category=ticket_category)

        embed = discord.Embed(
            colour=ColourCodes.success_colour,
            description=f"{Emojis.success} **ticked created**: {creation.mention}")
        
        await interaction.response.send_message(embed=embed, ephemeral=True)

        embed = discord.Embed(
            colour=ColourCodes.theme_colour,
            description=dedent(f"""
            support will be here shortly, please be patient
            
            **inquiry information**
            {self.answer.value}"""),
            timestamp=datetime.datetime.now())

        embed.set_footer(text=f"inquiry by: {str(interaction.user)}")
        embed.set_thumbnail(url=interaction.user.avatar)

        await creation.send("<@&906656381115973632>", embed=embed)


class KirbyTickets(discord.ui.Select):
    def __init__(self):

        options = [
            discord.SelectOption(
                label="purchase a custom bot",
                emoji=f"{Emojis.system}"),

            discord.SelectOption(
                label="update an already purchased bot",
                emoji=f"{Emojis.system}"),

            discord.SelectOption(
                label="pay monthly fees",
                emoji=f"{Emojis.money}"),

            discord.SelectOption(
                label="inquiry or general help",
                emoji=f"{Emojis.ticket}")
            ]

        super().__init__(
            placeholder="select a reason to open a ticket",
            min_values=0,
            max_values=1,
            options=options)

    async def callback(self, interaction: discord.Interaction):
        if self.values[0] == "inquiry or general help":

            ticket_name = f"inquiry-{interaction.user.name}"
            ticket_channel = discord.utils.get(
                interaction.guild.channels, name=ticket_name)

            if ticket_channel is not None:
                embed = discord.Embed(
                    colour=ColourCodes.warning_colour,
                    description=f"{Emojis.warning} you already **created** a ticket")
                embed.set_footer(text="1 ticket at a time to prevent spam")

                await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                await interaction.response.send_modal(InquiryInfo())


        if self.values[0] == "purchase a custom bot":
            embed = discord.Embed(
                title="important note",
                colour=ColourCodes.theme_colour,
                description=dedent(
                    """
                    payments are done **once every 1, 3, or 6 months** (you choose while ordering). if you're unable to pay, please **don't proceed**. 
                    this decision was taken due to the high hosting fees that I have to pay **monthly** to keep **your bots** up and running, the least you could do is contribute, thank you.
                    """))
            
            embed.set_footer(text="dismiss this message if you dont wish to proceed :)")

            await interaction.response.send_message(
                embed=embed, ephemeral=True, view=ConfirmationButton()
                )


        if self.values[0] == "update an already purchased bot":
            client_role = interaction.guild.get_role(1054485213083869274)
            ticket_name = f"update-{interaction.user.name}"
            ticket_channel = discord.utils.get(
                interaction.guild.channels, name=ticket_name)

            if ticket_channel is not None:
                embed = discord.Embed(
                    colour=ColourCodes.warning_colour,
                    description=f"{Emojis.warning} you already **created** a ticket")
                embed.set_footer(text="1 ticket at a time to prevent spam")

                return await interaction.response.send_message(embed=embed, ephemeral=True)

            if client_role not in interaction.user.roles:
                embed = discord.Embed(
                    colour=ColourCodes.warning_colour,
                    description=f"{Emojis.warning} you are not a **client**")

                return await interaction.response.send_message(embed=embed, ephemeral=True)
                
            await interaction.response.send_modal(UpdateInfo())


        if self.values[0] == "pay monthly fees":
            client_role = interaction.guild.get_role(1054485213083869274)
            ticket_name = f"monthly-{interaction.user.name}"

            ticket_channel = discord.utils.get(
                interaction.guild.channels, name=ticket_name)
            ticket_category = discord.utils.get(
                interaction.guild.categories, id=1066848157918576651)

            overwrites = {
                interaction.guild.default_role: discord.PermissionOverwrite(
                    read_messages=False),
                interaction.guild.me : discord.PermissionOverwrite(
                    view_channel=True, read_messages=True),
                interaction.user: discord.PermissionOverwrite(
                    read_messages=True, send_messages=True, attach_files=True)
            }

            if ticket_channel is not None:
                embed = discord.Embed(
                    colour=ColourCodes.warning_colour,
                    description=f"{Emojis.warning} you already **created** a ticket")
                embed.set_footer(text="1 ticket at a time to prevent spam")

                return await interaction.response.send_message(embed=embed, ephemeral=True)

            if client_role not in interaction.user.roles:
                embed = discord.Embed(
                    colour=ColourCodes.warning_colour,
                    description=f"{Emojis.warning} you are not a **client**")

                return await interaction.response.send_message(embed=embed, ephemeral=True)


            creation = await interaction.guild.create_text_channel(
                ticket_name, overwrites=overwrites, category=ticket_category)

            embed = discord.Embed(
                colour=ColourCodes.success_colour,
                description=f"{Emojis.success} **ticked created**: {creation.mention}")
            
            await interaction.response.send_message(embed=embed, ephemeral=True)
            embed = discord.Embed(
                title="instructions",
                colour=ColourCodes.theme_colour,
                description=dedent(
                f"""
                **after you successfully send the money, do the following:**

                {SEPERATOR} attach a screenshot of the payment
                {SEPERATOR} click the confirmation button below
                """)
            )
            await creation.send(f"{interaction.user.mention}", embed=embed, view=ConfirmMonthlyPayment())


class KirbyTicketsView(discord.ui.View):
    def __init__(self, timeout=None) -> None:
        super().__init__(timeout=timeout)
        self.add_item(KirbyTickets())


class FormButtons(discord.ui.View):
    def __init__(self) -> None:
        super().__init__(timeout=None)

    @discord.ui.button(
        label="form",
        emoji="🗒️",
        style=discord.ButtonStyle.grey)

    async def form_fillout(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(BotInfo())

    @discord.ui.button(
        label="payment methods",
        emoji="💰",
        style=discord.ButtonStyle.grey)

    async def methods_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            colour=ColourCodes.theme_colour,
            title="payment methods",
            description=dedent(f"""
            {Emojis.paypal} [JulyssaBrown98](https://paypal.me/JulyssaBrown98) **(f&f only)**
            {Emojis.cashapp} `$44kozy`
            {Emojis.btc} `bc1q0dfnw68k00du5a06a24slcs53pexf9pzt6la7t`
            {Emojis.eth} `0xcea47AA34B5cB3bf16D4be5E6C9c1C5B78E1a459`
            {Emojis.usdt} `0xcea47AA34B5cB3bf16D4be5E6C9c1C5B78E1a459` **(eth network)**"""))
        await interaction.response.send_message(embed=embed, ephemeral=True)


class ConfirmationButton(discord.ui.View):
    def __init__(self) -> None:
        super().__init__(timeout=None)

    @discord.ui.button(
        label="proceed",
        style=discord.ButtonStyle.green)

    async def proceed_to_order(self, interaction: discord.Interaction, button: discord.ui.Button):
            ticket_name = f"order-{interaction.user.name}"
            ticket_channel = discord.utils.get(
                interaction.guild.channels, name=ticket_name)
            ticket_category = discord.utils.get(
                interaction.guild.categories, id=1066848157918576651)

            overwrites = {
                interaction.guild.default_role: discord.PermissionOverwrite(
                    read_messages=False),
                interaction.guild.me : discord.PermissionOverwrite(
                    view_channel=True, read_messages=True),
                interaction.user: discord.PermissionOverwrite(
                    read_messages=True, send_messages=False)
            }

            if ticket_channel is not None:
                embed = discord.Embed(
                    colour=ColourCodes.warning_colour,
                    description=f"{Emojis.warning} you already **created** a ticket")
                embed.set_footer(text="1 ticket at a time to prevent spam")

                await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                creation = await interaction.guild.create_text_channel(
                    ticket_name, overwrites=overwrites, category=ticket_category)

                embed = discord.Embed(
                    colour=ColourCodes.success_colour,
                    description=f"{Emojis.success} **ticked created**: {creation.mention}")

                await interaction.response.send_message(embed=embed, ephemeral=True)
                embed = discord.Embed(
                    colour=ColourCodes.theme_colour,
                    description=dedent(f"""
                    **please be money ready before placing an order**

                    {SEPERATOR} __bot name__ **(self explanatory)**:
                    {SEPERATOR} __bot pfp__ **(url or send in channel)**:
                    {SEPERATOR} __bot theme__ **(hex/colour for embeds)**:
                    {SEPERATOR} __bot prefix__ **(self explanatory)**:
                    {SEPERATOR} __bot status__ **(dnd, online, idle)**:
                    {SEPERATOR} __bot activity__ **(streaming, watching, etc)**:
                    {SEPERATOR} __server link__ **(self explanatory):**
                    {SEPERATOR} __payment method__ **(strictly NO nitro)**:
                    {SEPERATOR} __payment type__ **(1, 3, or 6 months)**:
                    {SEPERATOR} __payment time__ **(before or halfway)**:
                    """)
                    )

                embed.set_footer(text="additional info will be discussed in the ticket")
                embed.set_thumbnail(url=interaction.user.avatar)

                await creation.send(
                    dedent(f"""
                    {interaction.user.mention} you may type after you fill out the form"""),
                    embed=embed, view=FormButtons())


class ConfirmMonthlyPayment(discord.ui.View):
    def __init__(self) -> None:
        super().__init__(timeout=None)
        self.value = True

    @discord.ui.button(
        label="confirm",
        style=discord.ButtonStyle.green)

    async def confirm_payment(self, interaction: discord.Interaction, button: discord.ui.Button):
        data = await interaction.client.db.fetch(
        """
        SELECT client_id, date, months 
        FROM clients
        """)

        for table in data:
            if table.get("client_id") == interaction.user.id:

                due_date: str = table.get("date")
                updated_months: int = int(due_date.split("/")[0]) +  int(table.get("months"))
                date = due_date.replace(due_date.split("/")[0], str(updated_months), 1)
                next_date = datetime.datetime.strptime(date, "%x").strftime("%B %d, %Y")

                await interaction.client.db.execute(
                    """
                    UPDATE clients
                    SET date = $1
                    WHERE client_id = $2
                    """, date, interaction.user.id)

                embed = discord.Embed(
                    colour=ColourCodes.success_colour,
                    description=f"thank you! your next payment is on **{next_date}**"
                )

        for child in self.children:
            child.disabled = True

        await interaction.response.edit_message(embed=embed, view=self)
        self.stop()


class Ticket(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot


    @commands.group(
        invoke_without_command=True,
        aliases=["tkt"])
    @commands.guild_only()
    async def ticket(self, ctx: commands.Context) -> Any:
        """
        ticket module

        Returns
        -------
        `Any`
         the help command for ticket module
        """

        if not ctx.invoked_subcommand:
            await ctx.send_help(ctx.command)


    @ticket.command(hidden=True)
    @commands.is_owner()
    async def close(self, ctx: commands.Context):
        """ exports the chats in a channel and closes it """

        file_name: str = f"{ctx.channel.name}.html"
        chatlogs = await chat_exporter.export(ctx.channel, fancy_times=True)

        await ctx.typing()

        with open(file_name, "w", encoding="utf-8") as file:
            file.writelines(chatlogs)

        send_file = discord.File(fp=file_name)

        await ctx.channel.delete()

        await self.bot.application.owner.send(file=send_file)
        remove(file_name)


    @ticket.command(hidden=True)
    @commands.is_owner()
    async def setup(self, ctx: commands.Context):
        """ sets up the ticket system embeds """

        channel = ctx.guild.get_channel(998868431396937788)

        async for msg in channel.history(limit=None): 
            await msg.delete()

        ticket_embed = discord.Embed(
            colour=ColourCodes.theme_colour)

        ticket_embed.add_field(
            name="about", value=dedent(f"""
            {SEPERATOR} building custom bots for your servers
            {SEPERATOR} high quality bots & affordable prices"""), inline=False)

        ticket_embed.add_field(
            name="payment",
            value=dedent(f"""
            {SEPERATOR} payment is done first or half way in
            {SEPERATOR} monthly payment plans up to 6 months"""), inline=False)

        ticket_embed.set_author(name="information", icon_url=self.bot.user.avatar)
        ticket_embed.set_footer(text="create a ticket to place an order")


        donate_embed = discord.Embed(
            colour=ColourCodes.theme_colour,
            description=dedent(f"""
            **＄5+**
            {SEPERATOR} <@&1070202745765777469> role, custom role
            {SEPERATOR} access to staff chat, own emote & sticker

            **＄15+**
            {SEPERATOR} <@&1072791283871002654> role, all of the above
            {SEPERATOR} donator only gws, own command & ban immunity

            **＄35+**
            {SEPERATOR} <@&1072792726417981492> role, all of the above
            {SEPERATOR} server shoutout, & custom bot of choice""")
            )
        donate_embed.set_author(
            name="donations",
            icon_url="https://cdn.discordapp.com/emojis/924657421438316554.gif")

        donate_embed.set_footer(text="any amount helps, dm elias to donate")


        end_embed = discord.Embed(
            colour=ColourCodes.theme_colour,
            description="all orders are final, there's no refund policy")        

        end_embed.set_footer(text="and please always use common sense")


        await channel.send(embed=ticket_embed, view=KirbyTicketsView())
        await channel.send(embed=donate_embed)
        await channel.send(embed=end_embed)
        await channel.send("https://discord.gg/YxkSp5fKG3")
        await ctx.message.add_reaction(Emojis.success)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Ticket(bot))
