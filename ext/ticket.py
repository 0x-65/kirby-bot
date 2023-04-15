import datetime

from os import remove
from re import search
from typing import Any
from requests import get
from asyncio import sleep
from textwrap import dedent

import discord
import chat_exporter

from discord import ui
from discord.ext import commands

from utils.views import ExportConfirmation
from utils.classes import Emojis, ColourCodes


SEPERATOR: str = "`+`"


class GeneralBotInfo(ui.Modal, title="custom bot"):
    name = ui.TextInput(
        label="name", placeholder="(self explanatory)", required=True)

    pfp = ui.TextInput(
        label="pfp", placeholder="(url or send in channel)", required=True)
    theme = ui.TextInput(
        label="theme", placeholder="(hex for embeds)", required=True)
    prefix = ui.TextInput(
        label="prefix", placeholder="(self explanatory)", required=True)
    activity = ui.TextInput(
        label="activity", placeholder="(streaming, watching, etc)", required=False)


    async def on_submit(self, interaction: discord.Interaction):
        view = FormButtons()
        view.children[0].disabled = True
        view.children[1].disabled = False

        overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(
                read_messages=False),
            interaction.guild.me : discord.PermissionOverwrite(
                view_channel=True, read_messages=True),
            interaction.user: discord.PermissionOverwrite(
                read_messages=True, send_messages=False)
        }

        embed = discord.Embed(
            colour=ColourCodes.theme_colour,
            title="general information:",
            description=dedent(f"""
            {SEPERATOR} __name:__ {self.name.value}
            {SEPERATOR} __pfp:__ [link]({self.pfp.value})
            {SEPERATOR} __theme:__ {self.theme.value}
            {SEPERATOR} __prefix:__ {self.prefix.value}
            {SEPERATOR} __activity:__ {self.activity.value}
            """),
            timestamp=datetime.datetime.now())

        embed.set_footer(text=f"client: {str(interaction.user)}")
        embed.set_thumbnail(url=interaction.user.avatar),

        await interaction.response.edit_message(
            content="please fill out the second form", 
            embed=embed, view=view)

        await interaction.channel.edit(overwrites=overwrites)


class AdditionalBotInfo(ui.Modal, title="custom bot"):
    server = ui.TextInput(
        label="server link", placeholder="(link to the server the bot will be in)", required=True)
    payment_method = ui.TextInput(
        label="payment method", placeholder="(strictly NO nitro)", required=True)
    payment_type = ui.TextInput(
        label="payment type", placeholder="(1, 3, or 6 months)", required=True)
    payment_time = ui.TextInput(
        label="payment time", placeholder="(before or halfway)", required=True)

    general_info = ui.TextInput(
        label="general info (cmds, ideas, examples)",
        placeholder="example: i want a modmail bot with `cmd1` and `cmd2` that does `this` and `that`",
        style=discord.TextStyle.paragraph, required=True)


    async def on_submit(self, interaction: discord.Interaction):
        view = FormButtons()
        view.children[0].disabled = True
        view.children[1].disabled = True

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
            title="additional information",
            colour=ColourCodes.theme_colour,
            description=dedent(f"""
            {SEPERATOR} __server link:__ {self.server.value}
            {SEPERATOR} __payment method:__ {self.payment_method.value}
            {SEPERATOR} __payment type:__ {self.payment_type.value}
            {SEPERATOR} __payment time:__ {self.payment_time.value}
            """),
            timestamp=datetime.datetime.now())

        embed.set_footer(text=f"client: {str(interaction.user)}")
        embed.set_thumbnail(url=interaction.user.avatar),
        embed.add_field(
            name="", value=f"```{self.general_info.value}```")

        await interaction.response.send_message(
            "if you forgot something type it in the ticket",
            embed=embed, view=PaymentMethodsButton())
        await interaction.channel.edit(overwrites=overwrites)
        await interaction.message.edit(view=view)


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
            colour=ColourCodes.theme_colour,
            description=f"{Emojis.success} **ticked created**: {creation.mention}")
        
        await interaction.response.send_message(embed=embed, ephemeral=True)

        embed = discord.Embed(
            title="update information",
            colour=ColourCodes.theme_colour,
            description=dedent(
                f"""
                {self.answer.value}
                """),
            timestamp=datetime.datetime.now())

        embed.set_footer(text=f"client: {str(interaction.user)}")
        embed.set_thumbnail(url=interaction.user.avatar)

        await creation.send("the dev will be here shortly", embed=embed, view=PaymentMethodsView())


class BitcoinDonationInfo(ui.Modal, title="bitcoin donation"):
    transaction_id = ui.TextInput(
        label="transaction ID", min_length=60, required=True)
    screenshot = ui.TextInput(
        label="transaction screenshot URL", min_length=80, required=True)


    async def on_submit(self, interaction: discord.Interaction):
        try:
            btc_rate: float = 30135.30
            view = DonationFormButtons()
            for item in view.children:
                item.disabled = True

            overwrites = {
                interaction.guild.default_role: discord.PermissionOverwrite(
                    read_messages=False),
                interaction.guild.me : discord.PermissionOverwrite(
                    view_channel=True, read_messages=True),
                interaction.user: discord.PermissionOverwrite(
                    read_messages=True, send_messages=True, attach_files=True)
            }

            html = get(f"https://live.blockcypher.com/btc/tx/{self.transaction_id.value}/")
            found_confirmations = search('<strong>(.*?)</strong> confirmations.', html.text)
            confirmations = int(found_confirmations.group(1).replace('.','').replace(',',''))

            found_amount = search('(.*?) BTC', html.text)
            amount = (found_amount.group(1).strip())

            
            if confirmations >= 1:
                transaction_fail_embed = discord.Embed(
                    colour=ColourCodes.theme_colour,
                    description=f"{Emojis.warning} this transaction has already been **completed**")
                return await interaction.response.send_message(embed=transaction_fail_embed, ephemeral=True)


            payment_ss_embed = discord.Embed(
                title="transaction screenshot",
                colour=ColourCodes.theme_colour
            )
            payment_ss_embed.set_image(url=self.screenshot.value)

            transaction_embed = discord.Embed(
                title="view transaction",
                url=f"https://live.blockcypher.com/btc/tx/{self.transaction_id.value}/",
                colour=ColourCodes.theme_colour,
                description=dedent(f"""
                {Emojis.warning} status: `pending`
                {Emojis.success} confirmations: `{str(confirmations)}`
                {Emojis.btc} amount: `{amount} BTC` **({round(float(amount) * btc_rate, 2)} USD)**
                """))

            transaction_embed.set_footer(text="will be marked as complete at 1 confirmation")

            await interaction.response.send_message(
                f"{interaction.client.application.owner.mention} transaction detected, you will be notified as soon as it's completed",
                embeds=[transaction_embed, payment_ss_embed])

            await interaction.channel.edit(overwrites=overwrites)
            await interaction.message.edit(view=view)

            while True:
                await sleep(2)
                if confirmations >= 1:
                    transaction_embed = discord.Embed(
                        title="view transaction",
                        url=f"https://live.blockcypher.com/btc/tx/{self.transaction_id.value}/",
                        colour=ColourCodes.theme_colour,
                        description=dedent(f"""
                        {Emojis.warning} status: `completed`
                        {Emojis.success} confirmations: `{str(confirmations)}`
                        {Emojis.btc} amount: `{fees} BTC` **({round(float(amount) * btc_rate, 2)} USD)**
                        """))

                    transaction_embed.set_footer(text=f"transaction author: {str(interaction.user)}")

                    await interaction.channel.send(
                        f"{interaction.client.application.owner.mention} the transaction was completed",
                        embed=transaction_embed)

                    donations: dict = {
                        5: 1070202745765777469,
                        10: 1072791283871002654,
                        25: 1072792726417981492
                    }
                    donated_amount: int = int(interaction.channel.name.split("-")[1])

                    if donated_amount in donations.keys():
                        donator_role = interaction.guild.get_role(donations[donated_amount])

                        await interaction.user.add_roles(donator_role)

                        perks_embed = discord.Embed(
                            colour=ColourCodes.theme_colour,
                            description=dedent(f"""
                            {SEPERATOR} you have been given the {donator_role.mention} role for donating **${donated_amount}**
                            {SEPERATOR} list the perks you would like to claim in the ticket
                            """)
                        )

                        await interaction.channel.send(interaction.user.mention, embed=perks_embed)
                        break

        except discord.errors.HTTPException:
            warn_embed = discord.Embed(
                colour=ColourCodes.theme_colour,
                description=f"{Emojis.warning} **invalid** image url")
            await interaction.response.send_message(embed=warn_embed, ephemeral=True)

        except:
            warn_embed = discord.Embed(
                colour=ColourCodes.theme_colour,
                description=f"{Emojis.warning} **invalid** transaction ID, make sure to provide a **valid** one")
            await interaction.response.send_message(embed=warn_embed, ephemeral=True)


class NormalDonationInfo(ui.Modal, title="donation"):
    screenshot = ui.TextInput(
        label="transaction screenshot URL", min_length=80, required=True)


    async def on_submit(self, interaction: discord.Interaction):
        try:
            view = DonationFormButtons()
            for item in view.children:
                item.disabled = True

            overwrites = {
                interaction.guild.default_role: discord.PermissionOverwrite(
                    read_messages=False),
                interaction.guild.me : discord.PermissionOverwrite(
                    view_channel=True, read_messages=True),
                interaction.user: discord.PermissionOverwrite(
                    read_messages=True, send_messages=True, attach_files=True)
            }

            payment_ss_embed = discord.Embed(
                title="transaction screenshot",
                colour=ColourCodes.theme_colour
            )
            payment_ss_embed.set_image(url=self.screenshot.value)

            await interaction.response.send_message(embed=payment_ss_embed)
            await interaction.channel.edit(overwrites=overwrites)
            await interaction.message.edit(view=view)

            donations: dict = {
                5: 1070202745765777469,
                10: 1072791283871002654,
                25: 1072792726417981492
            }
            donated_amount: int = int(interaction.channel.name.split("-")[1])

            if donated_amount in donations.keys():
                donator_role = interaction.guild.get_role(donations[donated_amount])

                await interaction.user.add_roles(donator_role)

                perks_embed = discord.Embed(
                    colour=ColourCodes.theme_colour,
                    description=dedent(f"""
                    {SEPERATOR} you received the {donator_role.mention} role for donating **${donated_amount}**
                    {SEPERATOR} list the perks you would like to claim in the ticket
                    """)
                )
                await interaction.channel.send(interaction.user.mention, embed=perks_embed)

        except discord.errors.HTTPException:
            warn_embed = discord.Embed(
                colour=ColourCodes.theme_colour,
                description=f"{Emojis.warning} **invalid** image url")
            await interaction.response.send_message(embed=warn_embed, ephemeral=True)


class BitcoinUpdateInfo(ui.Modal, title="bitcoin payment"):
    transaction_id = ui.TextInput(
        label="transaction ID", min_length=60, required=True)
    screenshot = ui.TextInput(
        label="transaction screenshot URL", min_length=80, required=True)


    async def on_submit(self, interaction: discord.Interaction):
        try:
            btc_rate: float = 30135.30
            view = DonationFormButtons()
            for item in view.children:
                item.disabled = True

            html = get(f"https://live.blockcypher.com/btc/tx/{self.transaction_id.value}/")
            found_confirmations = search('<strong>(.*?)</strong> confirmations.', html.text)
            confirmations = int(found_confirmations.group(1).replace('.','').replace(',',''))

            found_amount = search('(.*?) BTC', html.text)
            amount = (found_amount.group(1).strip())


            if confirmations >= 1:
                transaction_fail_embed = discord.Embed(
                    colour=ColourCodes.theme_colour,
                    description=f"{Emojis.warning} this transaction has already been **completed**")
                return await interaction.response.send_message(embed=transaction_fail_embed, ephemeral=True)


            payment_ss_embed = discord.Embed(
                title="transaction screenshot",
                colour=ColourCodes.theme_colour
            )
            payment_ss_embed.set_image(url=self.screenshot.value)

            transaction_embed = discord.Embed(
                title="view transaction",
                url=f"https://live.blockcypher.com/btc/tx/{self.transaction_id.value}/",
                colour=ColourCodes.theme_colour,
                description=dedent(f"""
                {Emojis.warning} status: `pending`
                {Emojis.success} confirmations: `{str(confirmations)}`
                {Emojis.btc} amount: `{amount} BTC` **({round(float(amount) * btc_rate, 2)} USD)**
                """))

            transaction_embed.set_footer(text="will be marked as complete at 1 confirmation")

            await interaction.response.send_message(
                f"{interaction.client.application.owner.mention} transaction detected, you will be notified as soon as it's completed",
                embeds=[transaction_embed, payment_ss_embed])

            await interaction.message.edit(view=view)

            while True:
                await sleep(2)
                if confirmations >= 1:
                    transaction_embed = discord.Embed(
                        title="view transaction",
                        url=f"https://live.blockcypher.com/btc/tx/{self.transaction_id.value}/",
                        colour=ColourCodes.theme_colour,
                        description=dedent(f"""
                        {Emojis.warning} status: `completed`
                        {Emojis.success} confirmations: `{str(confirmations)}`
                        {Emojis.btc} amount: `{fees} BTC` **({round(float(amount) * btc_rate, 2)} USD)**
                        """))

                    transaction_embed.set_footer(text=f"transaction author: {str(interaction.user)}")

                    await interaction.channel.send(
                        f"{interaction.client.application.owner.mention} the transaction was completed",
                        embed=transaction_embed)

        except discord.errors.HTTPException:
            warn_embed = discord.Embed(
                colour=ColourCodes.theme_colour,
                description=f"{Emojis.warning} **invalid** image url")
            await interaction.response.send_message(embed=warn_embed, ephemeral=True)

        except:
            warn_embed = discord.Embed(
                colour=ColourCodes.theme_colour,
                description=f"{Emojis.warning} **invalid** transaction ID, make sure to provide a **valid** one")
            await interaction.response.send_message(embed=warn_embed, ephemeral=True)


class NormalUpdateInfo(ui.Modal, title="payment"):
    screenshot = ui.TextInput(
        label="transaction screenshot URL", min_length=80, required=True)

    async def on_submit(self, interaction: discord.Interaction):
        try:  
            view = PaymentMethodsView()
            for item in view.children:
                item.disabled = True
          
            payment_embed = discord.Embed(
                title="transaction screenshot",
                colour=ColourCodes.theme_colour
            )
            payment_embed.set_image(url=self.screenshot.value)
            payment_embed.set_footer(
                text="the transaction has been processed successfully",
                icon_url="https://cdn.discordapp.com/emojis/1095048642219475034.webp")

            await interaction.response.send_message(
                interaction.client.application.owner.mention,
                embed=payment_embed)
            await interaction.message.edit(view=view)

        except discord.errors.HTTPException:
            warn_embed = discord.Embed(
                colour=ColourCodes.theme_colour,
                description=f"{Emojis.warning} **invalid** image url")
            await interaction.response.send_message(embed=warn_embed, ephemeral=True)


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
            colour=ColourCodes.theme_colour,
            description=f"{Emojis.success} **ticked created**: {creation.mention}")
        
        await interaction.response.send_message(embed=embed, ephemeral=True)

        embed = discord.Embed(
            title="inquiry information",
            colour=ColourCodes.theme_colour,
            description=self.answer.value,
            timestamp=datetime.datetime.now())

        embed.set_footer(text=f"inquiry by: {str(interaction.user)}")
        embed.set_thumbnail(url=interaction.user.avatar)

        await creation.send("support will be here shortly", embed=embed)


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
                label="donate",
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
                    colour=ColourCodes.theme_colour,
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
                    f"""
                    **by proceeding you agree to the following terms:**

                    {SEPERATOR} pay monthly for your bot(s) hosting & maintenance. (features are one-time)
                    {SEPERATOR} no refunds, you can't host on your own, and you can't buy the source code.
                    {SEPERATOR} when you buy a bot, you're buying an instance not the code itself.
                    """))
            
            embed.set_footer(text="dismiss this message if you dont wish to proceed")

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
                    colour=ColourCodes.theme_colour,
                    description=f"{Emojis.warning} you already **created** a ticket")
                embed.set_footer(text="1 ticket at a time to prevent spam")

                return await interaction.response.send_message(embed=embed, ephemeral=True)

            if client_role not in interaction.user.roles:
                embed = discord.Embed(
                    colour=ColourCodes.theme_colour,
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
                    colour=ColourCodes.theme_colour,
                    description=f"{Emojis.warning} you already **created** a ticket")
                embed.set_footer(text="1 ticket at a time to prevent spam")

                return await interaction.response.send_message(embed=embed, ephemeral=True)

            if client_role not in interaction.user.roles:
                embed = discord.Embed(
                    colour=ColourCodes.theme_colour,
                    description=f"{Emojis.warning} you are not a **client**")

                return await interaction.response.send_message(embed=embed, ephemeral=True)


            creation = await interaction.guild.create_text_channel(
                ticket_name, overwrites=overwrites, category=ticket_category)

            embed = discord.Embed(
                colour=ColourCodes.theme_colour,
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


        if self.values[0] == "donate":
            embed = discord.Embed(
                colour=ColourCodes.theme_colour,
                description=dedent(
                f"""
                {SEPERATOR} you must click on the perks first to be able to donate
                {SEPERATOR} after that click on an amount to start the donation process
                """)
            )

            embed.set_footer(text="dismiss this message if you don't wish to proceed")

            await interaction.response.send_message(
                embed=embed, view=DonationButtons(), ephemeral=True
                )


class KirbyTicketsView(discord.ui.View):
    def __init__(self, timeout=None) -> None:
        super().__init__(timeout=timeout)
        self.add_item(KirbyTickets())


class PaymentMethods(discord.ui.Select):
    def __init__(self):

        options = [
            discord.SelectOption(
                label="bitcoin",
                emoji=f"{Emojis.btc}"),

            discord.SelectOption(
                label="cashapp",
                emoji=f"{Emojis.cashapp}"),

            discord.SelectOption(
                label="paypal",
                emoji=f"{Emojis.paypal}"),
            ]

        super().__init__(
            placeholder="select a payment method",
            min_values=0,
            max_values=1,
            options=options)

    async def callback(self, interaction: discord.Interaction):
        if self.values[0] == "bitcoin":
            await interaction.response.send_modal(BitcoinDonationInfo())

        elif self.values[0] == "cashapp":
            await interaction.response.send_modal(NormalUpdateInfo())

        elif self.values[0] == "paypal":
            await interaction.response.send_modal(NormalUpdateInfo())


class PaymentMethodsView(discord.ui.View):
    def __init__(self, timeout=None) -> None:
        super().__init__(timeout=timeout)
        self.add_item(PaymentMethods())


class FormButtons(discord.ui.View):
    def __init__(self) -> None:
        super().__init__(timeout=None)

    @discord.ui.button(
        label="general info",
        emoji="🗒️",
        style=discord.ButtonStyle.grey)

    async def first_form_fillout(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(GeneralBotInfo())


    @discord.ui.button(
        label="additional info",
        emoji="🗒️",
        style=discord.ButtonStyle.grey,
        disabled=True)


    async def second_form_fillout(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(AdditionalBotInfo())


class DonationFormButtons(discord.ui.View):
    def __init__(self) -> None:
        super().__init__(timeout=None)


    @discord.ui.button(
        label="bitcoin",
        emoji=f"{Emojis.btc}",
        style=discord.ButtonStyle.grey)

    async def bitcoin_form(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(BitcoinDonationInfo())


    @discord.ui.button(
        label="cashapp",
        emoji=f"{Emojis.cashapp}",
        style=discord.ButtonStyle.grey)

    async def cashapp_form(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(NormalDonationInfo())


    @discord.ui.button(
        label="paypal",
        emoji=f"{Emojis.paypal}",
        style=discord.ButtonStyle.grey)

    async def paypal_form(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(NormalDonationInfo())



class PaymentMethodsButton(discord.ui.View):
    def __init__(self) -> None:
        super().__init__(timeout=None)

    @discord.ui.button(
        label="payment methods",
        emoji="💰",
        style=discord.ButtonStyle.grey)

    async def methods_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            colour=ColourCodes.theme_colour,
            title="payment methods",
            description=dedent(f"""
            {Emojis.paypal} [custom bots](https://paypal.me/JulyssaBrown98) **(fnf only, anything else will be voided)**
            {Emojis.cashapp} `$44kozy`
            {Emojis.btc} `bc1q0dfnw68k00du5a06a24slcs53pexf9pzt6la7t`
            {Emojis.eth} `0xcea47AA34B5cB3bf16D4be5E6C9c1C5B78E1a459`
            {Emojis.usdt} `0xcea47AA34B5cB3bf16D4be5E6C9c1C5B78E1a459` **(eth network)**"""))
        embed.set_footer(text="crypto and cashapp are preferred the most")
        await interaction.response.send_message(embed=embed, ephemeral=True)


class DonationButtons(discord.ui.View):
    def __init__(self) -> None:
        super().__init__(timeout=None)

    @discord.ui.button(
        label="＄5",
        emoji=f"{Emojis.money}",
        row=1,
        style=discord.ButtonStyle.green,
        disabled=True)

    async def donation_5_usd(self, interaction: discord.Interaction, button: discord.ui.Button):
            ticket_name = f"donation-5-{interaction.user.name}"

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
                    colour=ColourCodes.theme_colour,
                    description=f"{Emojis.warning} you already **created** a ticket")
                embed.set_footer(text="1 ticket at a time to prevent spam")

                return await interaction.response.send_message(embed=embed, ephemeral=True)


            creation = await interaction.guild.create_text_channel(
                ticket_name, overwrites=overwrites, category=ticket_category)

            embed = discord.Embed(
                colour=ColourCodes.theme_colour,
                description=f"{Emojis.success} **ticked created**: {creation.mention}")
            
            await interaction.response.send_message(embed=embed, ephemeral=True)

            form_embed = discord.Embed(
                colour=ColourCodes.theme_colour,
                description="**select a payment method to donate**")

            await creation.send(embed=form_embed, view=DonationFormButtons())


    @discord.ui.button(
        label="＄10",
        emoji=f"{Emojis.money}",
        row=1,
        style=discord.ButtonStyle.green,
        disabled=True)

    async def donation_10_usd(self, interaction: discord.Interaction, button: discord.ui.Button):
            ticket_name = f"donation-10-{interaction.user.name}"

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
                    colour=ColourCodes.theme_colour,
                    description=f"{Emojis.warning} you already **created** a ticket")
                embed.set_footer(text="1 ticket at a time to prevent spam")

                return await interaction.response.send_message(embed=embed, ephemeral=True)


            creation = await interaction.guild.create_text_channel(
                ticket_name, overwrites=overwrites, category=ticket_category)

            embed = discord.Embed(
                colour=ColourCodes.theme_colour,
                description=f"{Emojis.success} **ticked created**: {creation.mention}")
            
            await interaction.response.send_message(embed=embed, ephemeral=True)

            form_embed = discord.Embed(
                colour=ColourCodes.theme_colour,
                description="which payment method will you be using?")

            await creation.send(embed=form_embed, view=DonationFormButtons())

    @discord.ui.button(
        label="＄25",
        emoji=f"{Emojis.money}",
        row=1,
        style=discord.ButtonStyle.green,
        disabled=True)

    async def donation_25_usd(self, interaction: discord.Interaction, button: discord.ui.Button):
            ticket_name = f"donation-25-{interaction.user.name}"

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
                    colour=ColourCodes.theme_colour,
                    description=f"{Emojis.warning} you already **created** a ticket")
                embed.set_footer(text="1 ticket at a time to prevent spam")

                return await interaction.response.send_message(embed=embed, ephemeral=True)


            creation = await interaction.guild.create_text_channel(
                ticket_name, overwrites=overwrites, category=ticket_category)

            embed = discord.Embed(
                colour=ColourCodes.theme_colour,
                description=f"{Emojis.success} **ticked created**: {creation.mention}")
            
            await interaction.response.send_message(embed=embed, ephemeral=True)

            form_embed = discord.Embed(
                colour=ColourCodes.theme_colour,
                description="which payment method will you be using?")

            await creation.send(embed=form_embed, view=DonationFormButtons())


    @discord.ui.button(
        label="donator perks",
        emoji="🗒️",
        row=2,
        style=discord.ButtonStyle.grey)

    async def donation_perks_usd(self, interaction: discord.Interaction, button: discord.ui.Button):
        view = DonationButtons()
        view.children[0].disabled = False
        view.children[1].disabled = False
        view.children[2].disabled = False

        donate_perks_embed = discord.Embed(
            colour=ColourCodes.theme_colour,
            description=dedent(f"""
            **＄5**
            {SEPERATOR} <@&1070202745765777469> role, custom role
            {SEPERATOR} access to staff chat, own emote & sticker
            
            **＄10**
            {SEPERATOR} <@&1072791283871002654> role, all of the above
            {SEPERATOR} donator only gws, own command & ban immunity
            
            **＄25**
            {SEPERATOR} <@&1072792726417981492> role, all of the above
            {SEPERATOR} server shoutout, & a custom bot of choice
            """))

        await interaction.response.edit_message(view=view)
        await interaction.edit_original_response(embed=donate_perks_embed)


class ConfirmationButton(discord.ui.View):
    def __init__(self) -> None:
        super().__init__(timeout=None)

    @discord.ui.button(
        label="I agree & wish to proceed",
        style=discord.ButtonStyle.grey)

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
                    colour=ColourCodes.theme_colour,
                    description=f"{Emojis.warning} you already **created** a ticket")
                embed.set_footer(text="1 ticket at a time to prevent spam")

                await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                creation = await interaction.guild.create_text_channel(
                    ticket_name, overwrites=overwrites, category=ticket_category)

                embed = discord.Embed(
                    colour=ColourCodes.theme_colour,
                    description=f"{Emojis.success} **ticked created**: {creation.mention}")

                await interaction.response.send_message(embed=embed, ephemeral=True)
                embed = discord.Embed(
                    title="instructions",
                    colour=ColourCodes.theme_colour,
                    description=dedent(f"""
                    {SEPERATOR} __please be money ready before you proceed__
                    {SEPERATOR} __you may type after you fill out both forms__
                    {SEPERATOR} __additional info will be discussed in the ticket__
                    """)
                    )

                embed.set_footer(text="the dev will be here shortly")
                embed.set_thumbnail(url=interaction.user.avatar)

                await creation.send(interaction.user.mention, embed=embed, view=FormButtons())


class ConfirmMonthlyPayment(discord.ui.View):
    def __init__(self) -> None:
        super().__init__(timeout=None)
        self.value = True

    @discord.ui.button(
        label="confirm",
        style=discord.ButtonStyle.gray)

    async def confirm_payment(self, interaction: discord.Interaction, button: discord.ui.Button):
        data = await interaction.client.db.fetch(
        """
        SELECT client_id, date, months 
        FROM clients
        """)

        for table in data:
            if table.get("client_id") == interaction.user.id:

                date = datetime.datetime.strptime(table.get("date"), "%m/%d/%Y")
                weeks: float = 0

                if int(table.get("months")) == 6:
                    weeks = 26.0
                elif int(table.get("months")) == 3:
                    weeks = 13.0
                elif int(table.get("months")) == 1:
                    weeks = 4.34524

                new_date = date + datetime.timedelta(weeks=weeks)
                next_date = new_date.strftime("%B %d, %Y")

                await interaction.client.db.execute(
                    """
                    UPDATE clients
                    SET date = $1
                    WHERE client_id = $2
                    """, new_date.strftime("%m/%d/%Y"), interaction.user.id)

                embed = discord.Embed(
                    colour=ColourCodes.theme_colour,
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

        view = ExportConfirmation()

        embed = discord.Embed(
            description=f"{Emojis.warning} would you like to **export** this ticket?",
            colour=ColourCodes.theme_colour)
        await ctx.send(embed=embed, view=view)
        await view.wait()

        if view.value is None:
            pass

        elif view.value:
            file_name: str = f"{ctx.channel.name}.html"
            chatlogs = await chat_exporter.export(ctx.channel, fancy_times=True)

            with open(file_name, "w", encoding="utf-8") as file:
                file.writelines(chatlogs)

            send_file = discord.File(fp=file_name)

            await ctx.channel.delete()

            await self.bot.application.owner.send(file=send_file)
            remove(file_name)
        else:
            await ctx.channel.delete()



    @ticket.command(hidden=True)
    @commands.is_owner()
    async def setup(self, ctx: commands.Context):
        """ sets up the ticket system embeds """

        channel = ctx.guild.get_channel(998868431396937788)



        ticket_embed = discord.Embed(
            colour=ColourCodes.theme_colour)

        ticket_embed.add_field(
            name="about", value=dedent(f"""
            {SEPERATOR} building custom bots for your servers
            {SEPERATOR} high quality bots & affordable prices"""), inline=False)

        ticket_embed.add_field(
            name="notice",
            value=dedent(f"""
            {SEPERATOR} all orders are final there's no refund policy
            {SEPERATOR} always use common sense and ask if you're unsure"""), inline=False)

        ticket_embed.add_field(
            name="payment",
            value=dedent(f"""
            {SEPERATOR} payment is done first or half way in
            {SEPERATOR} monthly payment plans up to 6 months"""), inline=False)

        ticket_embed.add_field(
            name="donation",
            value=dedent(f"""
            {SEPERATOR} create a ticket with the reason "donate"
            {SEPERATOR} any amount helps and will go directly to hosting"""), inline=False)

        ticket_embed.set_author(name="information", icon_url=self.bot.user.avatar)
        ticket_embed.set_footer(text="create a ticket to order, donate, or if you need assistance")


        await channel.send(embed=ticket_embed, view=KirbyTicketsView())
        await channel.send("https://discord.gg/YxkSp5fKG3", view=PaymentMethodsButton())
        await ctx.message.add_reaction(Emojis.success)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Ticket(bot))
