from typing import Any
from asyncio import sleep
from textwrap import dedent
from datetime import datetime

import discord

from discord.ext import commands, tasks

from utils.paginator import StaticPaginator
from utils.classes import Emojis, ColourCodes


class AutoPayment(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.currency: str = "＄"
        self.daily_clients_check.start()


    @tasks.loop(hours=24)
    async def daily_clients_check(self):
        channel = self.bot.get_channel(1069008935140474995)
        await channel.send("kirby client check")


    @daily_clients_check.before_loop
    async def before_my_task(self):
        await self.bot.wait_until_ready()


    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id == self.bot.user.id and message.content == "kirby client check":

            original_msg = message.channel.get_partial_message(message.id)
            cmd = self.bot.get_command(str(message.content).replace("kirby ", ""))
            context = await self.bot.get_context(message)

            await original_msg.delete()
            await message.channel.send("daily client checkup (every 24 hours)")
            await context.invoke(cmd)


    @commands.group(
        invoke_without_command=True,
        usage="kirby client <command>")
    @commands.guild_only()
    async def client(self, ctx: commands.Context) -> Any:
        """
        auto payments module

        Returns
        -------
        `Any`
         the help command for auto payment module
        """

        if not ctx.invoked_subcommand:
            await ctx.send_help(ctx.command)


    @client.command(aliases=["cinfo", "ci"], hidden=True)
    @commands.is_owner()
    async def info(
        self, ctx: commands.Context, 
        *, client: discord.Member
        ) -> discord.Embed:

        client_data = await self.bot.db.fetch(
        '''
        SELECT client_id
        FROM clients 
        WHERE client_id = $1
        ''', client.id)

        client_info = await self.bot.db.fetch(
        '''
        SELECT date, price, months
        FROM clients
        WHERE client_id = $1
        ''', client.id)


        if not client_data:
            embed = discord.Embed(
                color=ColourCodes.theme_colour,
                description=f'{Emojis.database} {client.mention} is not a registered **client** in the `database`')
            return await ctx.send(embed=embed)

        date = datetime.strptime(client_info[0].get("date"), "%m/%d/%Y").strftime("%B %d, %Y")
        fees = client_info[0].get("price")
        months = f"{client_info[0].get('months')} month" if client_info[0].get('months') == "1" else f"{client_info[0].get('months')} months"


        embed = discord.Embed(
            title=f'client: {str(client)}',
            color=ColourCodes.theme_colour)

        embed.set_thumbnail(url=client.avatar)

        embed.add_field(
            name='next payment:', 
            value=date, inline=False)

        embed.add_field(
            name='fees to pay:', 
            value=f"${fees}", inline=False)

        embed.add_field(
            name='payment every:', 
            value=months, inline=False)

        await ctx.send(embed=embed)


    @client.command(aliases=["list"], hidden=True)
    @commands.is_owner()
    async def clients(
        self, ctx: commands.Context) -> discord.Embed:

        client_info: str = ""
        clients: list = []

        data = await self.bot.db.fetch(
            """
            SELECT client_id, date, price, months
            FROM clients
            """)

        if not data:
            embed = discord.Embed(
                colour=ColourCodes.theme_colour,
                description=f'{Emojis.warning} **no clients** found')
            return await ctx.send(embed=embed)


        for count, table in enumerate(data, start=1):
            order_date = datetime.strptime(str(table.get("date")), "%m/%d/%Y").strftime("%B %d, %Y")
            client = ctx.guild.get_member(int(table.get("client_id")))
            price = table.get("price")
            months = f"{table.get('months')} month" if int(table.get("months")) == 1 else f"{table.get('months')} months"

            client_info = f"`{count}.` {client.mention} - **next payment:** {order_date} - **fees:** `{self.currency}{price}` (every {months})"
            clients.append(client_info)

            buttons = StaticPaginator(
                clients,
                user=ctx.author,
                line_limit=10,
                base_embed=discord.Embed(
                    title="clients found in total",
                    colour=ColourCodes.theme_colour,
                    description=clients,
                    timestamp=datetime.now())
                        )

        embeds = buttons.get_page(1)
        msg = await ctx.send(embeds=embeds) if count <= 10 else await ctx.send(embeds=embeds, view=buttons)
        buttons.response = msg


    @client.command(hidden=True)
    @commands.is_owner()
    async def check(
        self, ctx: commands.Context) -> discord.Embed:
        date_today: str = datetime.today().strftime("%m/%d/%Y")
        client_info: str = ""
        clients: list = []
        count: int = 0

        data = await self.bot.db.fetch(
            """
            SELECT client_id, date, price
            FROM clients
            """)

        embed = discord.Embed(
            colour=ColourCodes.theme_colour,
            description=f"{Emojis.loading} checking for clients with payment due **today**.."
        )

        loading_msg = await ctx.send(embed=embed)
        await sleep(3)

        if not data:
            embed = discord.Embed(
                colour=ColourCodes.theme_colour,
                description=f'{Emojis.warning} **no clients** found `at all`')
            return await loading_msg.edit(embed=embed)


        if data:
            if all(
                str(table.get("date")) != date_today
                for table in data
                ):
                embed = discord.Embed(
                    colour=ColourCodes.theme_colour,
                    description=f'{Emojis.warning} **no clients** found for `today`')
                return await loading_msg.edit(embed=embed)


        for table in data:
            if str(table.get("date")) == date_today:
                count += 1
                order_date = datetime.strptime(str(table.get("date")), "%m/%d/%Y").strftime("%B %d, %Y")
                client = ctx.guild.get_member(int(table.get("client_id")))
                price = table.get("price")

                client_info = f"`{count}.` {Emojis.success} {client.mention} --> **fees to pay:** `{self.currency}{price}`"
                clients.append(client_info)


                receipt_embed = discord.Embed(
                    colour=ColourCodes.theme_colour,
                    description=dedent(
                        f"""
                        **information:**
                        `+` fees to pay: `{self.currency}{price}`
                        `+` date of payment: **{order_date}**
                        """))

                receipt_embed.set_author(
                    name=f"monthly receipt for {str(client)}", icon_url=client.avatar)
                receipt_embed.set_footer(text="create a ticket in the server to pay the fees, you have 3 to 4 days")

                try:
                    await client.send(embed=receipt_embed)
                except discord.errors.Forbidden:
                    clients.remove(client_info)
                    clients.append(client_info.replace(f"{Emojis.success}", f"{Emojis.error}"))


                buttons = StaticPaginator(
                    clients,
                    user=ctx.author,
                    line_limit=10,
                    base_embed=discord.Embed(
                            title="clients found for today",
                            colour=ColourCodes.theme_colour,
                            description=clients
                            )
                        )

        embeds = buttons.get_page(1)
        msg = await loading_msg.edit(embeds=embeds) if count <= 10 else await loading_msg.edit(embeds=embeds, view=buttons)
        buttons.response = msg


    @client.command(hidden=True)
    @commands.is_owner()
    async def add(
        self, ctx: commands.Context,
        user: discord.User, date: str,
        price: str, months: str
        ) -> discord.Embed:

        data = await self.bot.db.fetch("SELECT client_id FROM clients")

        for table in data:
            if int(table.get("client_id")) == user.id:
                embed = discord.Embed(
                    colour=ColourCodes.theme_colour,
                    description=f'{Emojis.warning} {user.mention} is **already** a `client`')
                return await ctx.send(embed=embed)

        await self.bot.db.execute(
            """
            INSERT INTO clients (client_id, date, price, months)
            VALUES ($1, $2, $3, $4)
            """, user.id, date, price, months)

        date_due = datetime.strptime(date, "%m/%d/%Y").strftime("%B %d, %Y")
        month_date = f"{months} month" if months == "1" else f"{months} months"

        embed = discord.Embed(
            title=f"{Emojis.success} client added: {str(user)}",
            colour=ColourCodes.success_colour,
            description=dedent(
                f"""
                `+` they will be charged `{self.currency}{price}` every **{month_date}**
                `+` starting date: **{date_due}**"""))
        
        embed.set_footer(text="date will auto update after every successful payment")
        await ctx.send(embed=embed)


    @client.command(hidden=True)
    @commands.is_owner()
    async def remove(
        self, ctx: commands.Context, user: discord.User
        ) -> discord.Embed:

        await self.bot.db.execute(
            "DELETE FROM clients WHERE client_id = $1", user.id
            )

        embed = discord.Embed(
            colour=ColourCodes.success_colour,
            description=f"{Emojis.success} {user.mention} is **no longer** a `client`")
        await ctx.send(embed=embed)


    @client.command(hidden=True)
    @commands.is_owner()
    async def update(
        self, ctx: commands.Context,
        user: discord.User, date: str,
        price: str, months: str
        ) -> discord.Embed:

        await self.bot.db.execute(
            """
            UPDATE clients
            SET date = $2, price = $3, months = $4
            WHERE client_id = $1
            """, user.id, date, price, months)

        embed = discord.Embed(
            colour=ColourCodes.success_colour,
            description=f"{Emojis.success} **updated** {user.mention}'s payment & date `info`")
        await ctx.send(embed=embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(AutoPayment(bot))