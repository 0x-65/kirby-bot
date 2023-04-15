from typing import Optional
from datetime import datetime

import random

from discord.ext import commands

import discord

from utils.functions import better_numbers
from utils.classes import ColourCodes, EconomyList, Emojis
from utils.paginator import StaticPaginator


_cooldown = commands.CooldownMapping.from_cooldown(
    3.0, 15.0, commands.BucketType.user)


class Economy(
    commands.Cog, command_attrs={"cooldown": _cooldown}
    ):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.currency: str = "koins"
        self.jobs = EconomyList.jobs
        self.celebs = EconomyList.celebs
        self.prizes = EconomyList.roles


    async def get_account(self, user: discord.User):
        '''gets the balance of a user '''

        info = await self.bot.db.fetchrow(
            """
            SELECT *
            FROM economy
            WHERE user_id = $1
            """,
            user,
        )
        if info is None:
            await self.bot.db.execute(
                """
                    INSERT INTO economy (user_id, wallet, bank, inventory)
                    VALUES ($1, $2, $3, $4)
                """,
                user,
                0,
                0,
                "you havent bought any roles yet",
            )
            return await self.bot.db.fetchrow(
                """
                SELECT *
                FROM economy
                WHERE user_id = $1
                """,
                user,
            )
        else:
            return info
    

    @commands.command(aliases=["lb"])
    async def leaderboard(self, ctx: commands.Context) -> discord.Embed:
        """
        shows a list of the current users and their total koins

        Returns
        -------
        `discord.Embed`
         an embed with a list of the users and their total koins
        """

        users = await self.bot.db.fetch(
        """
        SELECT user_id, wallet, bank
        FROM economy
        """
        )

        count: int = 0
        leaderboard: str = ""
        stats: list[str] = []

        users.sort(key=lambda x: x.get("bank") + x.get("wallet"), reverse=True)

        if users:
            for table in users:
                if ctx.guild.get_member(table.get("user_id")) != None and table.get("bank") + table.get("wallet") != 0:
                    count += 1

                    total: int = table.get("bank") + table.get("wallet")
                    user = self.bot.get_user(int(table.get("user_id")))

                    leaderboard = f"`{count}.` **{str(user)}** --> total {self.currency}: `{better_numbers(total)}`"
                    stats.append(leaderboard)

            buttons = StaticPaginator(
                stats,
                user=ctx.author,
                line_limit=10,
                base_embed=discord.Embed(
                    title=f"{ctx.guild.name}'s leaderboard",
                    color=ColourCodes.theme_colour),
                        )

            embeds = buttons.get_page(1)
            msg = await ctx.send(embeds=embeds) if count <= 10 else await ctx.send(embeds=embeds, view=buttons)
            buttons.response = msg
        else:
            wrn_embed = discord.Embed(
                description=f"{Emojis.warning} no users **found**",
                colour=ColourCodes.theme_colour)
            await ctx.send(embed=wrn_embed)    


    @commands.command()
    async def shop(self, ctx: commands.Context) -> str:
        """
        shows the shop

        Returns
        -------
        `str`
         a msg redirecting user's to the shop channel
        """

        shop: str = ""

        for count, prize in enumerate(self.prizes.items(), start=1):
            role = discord.utils.get(ctx.guild.roles, name=str(prize[0]))
            role_name = ctx.guild.get_role(role.id)

            shop += f"\n`{count}.` **price:** `{better_numbers(prize[1])}` {Emojis.koin} **prize:** {role.mention}"

            embed = discord.Embed(
                title="kirby's shop",
                description=shop,
                color=ColourCodes.theme_colour)

            embed.set_footer(text="use kirby buy <rolename> to buy a role")

        await ctx.send(embed=embed)


    @commands.command(aliases=['balance', 'bal', 'inventory'])
    async def profile(
        self, ctx: commands.Context, 
        *, user: Optional[discord.User]
        ) -> discord.Embed:
        """
        shows a user's balance and inventory

        Parameters
        ----------
        `user`: Optional[discord.User]
         the user to get the balance of

        Returns
        -------
        `discord.Embed`
         an embed with info about the user's balance
        """

        user = user or ctx.author
        info = await self.get_account(user.id)

        embed = discord.Embed(
            color=ColourCodes.theme_colour)

        embed.set_author(name=f"{user.name}'s profile", icon_url=user.avatar)

        embed.add_field(
            name=f"{Emojis.koin} wallet",
            value=f'`{better_numbers(info["wallet"])}`')

        embed.add_field(
            name=f"{Emojis.koin} bank",
            value=f'`{better_numbers(info["bank"])}`')

        embed.add_field(
            name=f"{Emojis.koin} total",
            value=f'`{better_numbers(info["bank"] + info["wallet"])}`')

        embed.add_field(
            name='inventory',
            value=info["inventory"],
            inline=False)
        
        await ctx.send(embed=embed)


    @commands.command(aliases=["claim"])
    async def buy(
        self, ctx: commands.Context, *, rolename: str
        ) -> discord.Embed:
        """
        buy roles in exchange for koins

        Returns
        -------
        `discord.Embed`
         an embed with the role you bought
        """

        info = await self.get_account(ctx.author.id)
        role_to_buy: int = self.prizes.get(rolename)


        for role in ctx.guild.roles:
            if rolename in role.name:
                role = ctx.guild.get_role(role.id)
                break


        if role_to_buy > info["wallet"]:
            embed = discord.Embed(
                colour=ColourCodes.theme_colour,
                description=f"{Emojis.error} you dont have **enough** {self.currency} to buy that `role`")
            return await ctx.send(embed=embed)


        if role in ctx.author.roles:
            embed = discord.Embed(
                colour=ColourCodes.theme_colour,
                description=f"{Emojis.warning} you already **bought** that `role`")
            return await ctx.send(embed=embed)


        wallet = info["wallet"] - role_to_buy
        if info["inventory"] == "you havent bought any roles yet":
            inventory = f"<@&{role.id}>" 
        else:
            inventory = info["inventory"] + f", <@&{role.id}>" 

        await self.bot.db.execute(
            """
            UPDATE economy
            SET wallet = $2, inventory = $3
            WHERE user_id = $1;
            """,
            ctx.author.id,
            wallet,
            inventory
        )

        await ctx.author.add_roles(role)

        embed = discord.Embed(
            colour=ColourCodes.success_colour,
            description=f"{Emojis.success} you sucessfully **bought** {role.mention} for `{better_numbers(role_to_buy)}` {self.currency}")
        await ctx.send(embed=embed)


    @commands.command(aliases=["with"])
    async def withdraw(
        self, ctx: commands.Context, amount
        ) -> discord.Embed:
        """
        withdraws the desired amount of koins to a user's wallet

        Parameters
        ----------
        `amount`: int
         the amount to withdraw

        Returns
        -------
        `discord.Embed`
         an embed with info about the amount you withdrew
        """        

        info = await self.get_account(ctx.author.id)

        if amount == "all":
            amount = info["bank"]
        else:
            try:
                amount = int(amount)
            except ValueError:
                embed = discord.Embed(
                    colour=ColourCodes.theme_colour,
                    description=f"{Emojis.error} **invalid** amount, make sure you're providing a `number`")
                return await ctx.send(embed=embed)

        if amount > info["bank"]:
            embed = discord.Embed(
                colour=ColourCodes.theme_colour,
                description=f'{Emojis.warning} cant withdraw **more than** you have in your `bank`')
            return await ctx.send(embed=embed)

        bank = info["bank"] - amount
        wallet = info["wallet"] + amount

        await self.bot.db.execute(
            """
            UPDATE economy
            SET wallet = $2, bank = $3
            WHERE user_id = $1;
            """,
            ctx.author.id,
            wallet,
            bank,
        )

        embed = discord.Embed(
            colour=ColourCodes.theme_colour,
            description=f'{Emojis.koin} `{better_numbers(amount)}` {self.currency} **withdrawn** to your `wallet`')

        await ctx.send(embed=embed)


    @commands.command(aliases=["dep"])
    async def deposit(
        self, ctx: commands.Context, amount
        ) -> discord.Embed:
        """
        deposits the desired amount of koins to a user's bank

        Parameters
        ----------
        `amount`: int
         the amount to deposit

        Returns
        -------
        `discord.Embed`
         an embed with info about the amount you deposited
        """ 

        info = await self.get_account(ctx.author.id)

        if amount == "all":
            amount = info["wallet"]
        else:
            try:
                amount = int(amount)
            except ValueError:
                embed = discord.Embed(
                    colour=ColourCodes.theme_colour,
                    description=f"{Emojis.error} **invalid** amount, make sure you're **providing** a `number`")
                return await ctx.send(embed=embed)

        if amount > info["wallet"]:
            embed = discord.Embed(
                colour=ColourCodes.theme_colour,
                description=f'{Emojis.warning} cant withdraw **more than** you have in your `wallet`')
            return await ctx.send(embed=embed)

        bank = info["bank"] + amount
        wallet = info["wallet"] - amount

        await self.bot.db.execute(
            """
            UPDATE economy
            SET wallet = $2, bank = $3
            WHERE user_id = $1;
            """,
            ctx.author.id,
            wallet,
            bank,
        )

        embed = discord.Embed(
            colour=ColourCodes.theme_colour,
            description=f'{Emojis.koin} `{better_numbers(amount)}` {self.currency} **deposited** to your `bank`')

        await ctx.send(embed=embed)


    @commands.command()
    @commands.cooldown(3, 120, commands.BucketType.user)
    async def beg(self, ctx: commands.Context) -> discord.Embed:
        """
        begs a celebrity in hopes of getting some koins

        Returns
        -------
        `discord.Embed`
         an embed with info abt the celebrity and how much they gave you
        """

        celeb = random.choice(self.celebs)

        amount = random.randint(1, 500)
        info = await self.get_account(ctx.author.id)
        wallet = info["wallet"] + amount

        if random.random() < 0.5:
            embed = discord.Embed(
                colour=ColourCodes.theme_colour,
                description=f'😂 **{celeb}** says go away you broke bum')
            return await ctx.send(embed=embed)

        await self.bot.db.execute(
            """
            UPDATE economy
            SET wallet = $2
            WHERE user_id = $1;
            """,
            ctx.author.id,
            wallet,
        )

        embed = discord.Embed(
            colour=ColourCodes.theme_colour,
            description=f'{Emojis.koin} **{celeb}** felt bad and gave you `{better_numbers(amount)}` {self.currency}')

        await ctx.send(embed=embed)


    @commands.command()
    @commands.cooldown(2, 3600, commands.BucketType.user)
    async def work(self, ctx: commands.Context) -> discord.Embed:
        """
        work a random job in hopes of getting some koins

        Returns
        -------
        `discord.Embed`
         an embed with info about the job you worked and how much you earned
        """

        job = random.choice(self.jobs)
        info = await self.get_account(ctx.author.id)

        amount = random.randint(1, 1000)
        wallet = info["wallet"] + amount

        await self.bot.db.execute(
            """
            UPDATE economy
            SET wallet = $2
            WHERE user_id = $1;
            """,
            ctx.author.id,
            wallet,
        )

        embed = discord.Embed(
            colour=ColourCodes.theme_colour,
            description=f'{Emojis.koin} you worked as a **{job}** and earned `{better_numbers(amount)}` {self.currency}')

        await ctx.send(embed=embed)


    @commands.command(aliases=["rob"])
    @commands.cooldown(3, 90, commands.BucketType.user)
    async def steal(
        self, ctx: commands.Context, 
        *, user: discord.User
        ) -> discord.Embed:
        """
        steals koins from a user

        Parameters
        ----------
        `user`: discord.User
         the user to steal from

        Returns
        -------
        `discord.Embed`
         an embed with info about the amount you stole
        """        

        possibility: list = [
            "robbery", "caught"
            ]

        author_account = await self.get_account(ctx.author.id)
        user_account = await self.get_account(user.id)

        if user == ctx.author:
            return await ctx.send('are u dumb?')

        if user_account["wallet"] < 1:
            embed = discord.Embed(
                colour=ColourCodes.theme_colour,
                description=f'😂 **{user.mention}** is too broke lol')
            return await ctx.send(embed=embed)


        amount: int = random.randint(1, user_account["wallet"])


        if random.choice(possibility) == "caught":
            if author_account["wallet"] < 1:
                embed = discord.Embed(
                    colour=ColourCodes.theme_colour,
                    description=f"{Emojis.koin} you were **caught** but you're too `broke` so they let you go")

                return await ctx.send(embed=embed)

            if author_account["wallet"] < 1000:
                amount: int = random.randint(1, author_account["wallet"])
            else:
                amount: int = random.randint(1, 1000)

            wallet = author_account["wallet"] - amount
            await self.bot.db.execute(
                """
                    UPDATE economy
                    SET wallet = $2
                    WHERE user_id = $1;
                    """,
                ctx.author.id,
                wallet,
            )

            wallet = user_account["wallet"] + amount
            await self.bot.db.execute(
                """
                    UPDATE economy
                    SET wallet = $2
                    WHERE user_id = $1;
                    """,
                user.id,
                wallet,
            )
            embed = discord.Embed(
                colour=ColourCodes.theme_colour,
                description=f'{Emojis.koin} you were **caught..** you paid {user.mention} `{better_numbers(amount)}` {self.currency}')

            return await ctx.send(embed=embed)


        wallet = author_account["wallet"] + amount
        await self.bot.db.execute(
            """
                UPDATE economy
                SET wallet = $2
                WHERE user_id = $1;
                """,
            ctx.author.id,
            wallet,
        )

        wallet = user_account["wallet"] - amount
        await self.bot.db.execute(
            """
                UPDATE economy
                SET wallet = $2
                WHERE user_id = $1;
                """,
            user.id,
            wallet,
        )

        embed = discord.Embed(
            colour=ColourCodes.theme_colour,
            description=f'{Emojis.koin} you **stole** `{better_numbers(amount)}` {self.currency} from {user.mention}')

        await ctx.send(embed=embed)


    @commands.command()
    async def give(
        self, ctx: commands.Context, 
        amount: int, *, user: discord.User
        ) -> discord.Embed:
        """
        gives koins to a user 

        Parameters
        ----------
        `amount`: int
         the amount to give
        `user`: discord.User
         the user to give

        Returns
        -------
        `discord.Embed`
         an embed with info about the amount you gave to the user
        """        

        user_account = await self.get_account(ctx.author.id)
        author_account = await self.get_account(user.id)

        if user == ctx.author:
            return await ctx.send('you cant give yourself money dummy')

        if user_account["wallet"] < 1:
            embed = discord.Embed(
                colour=ColourCodes.theme_colour,
                description=f'😂 **{ctx.author.mention}** you are too broke lol')
            return await ctx.send(embed=embed)

        if amount > user_account["wallet"]:
            embed = discord.Embed(
                colour=ColourCodes.theme_colour,
                description=f'{Emojis.error} **insufficient** {self.currency}, try giving a `lower` amount')
            return await ctx.send(embed=embed)

        wallet = author_account["wallet"] + amount
        await self.bot.db.execute(
            """
            UPDATE economy
            SET wallet = $2
            WHERE user_id = $1;
            """,
            user.id,
            wallet,
        )
        wallet = user_account["wallet"] - amount
        await self.bot.db.execute(
            """
            UPDATE economy
            SET wallet = $2
            WHERE user_id = $1;
            """,
            ctx.author.id,
            wallet,
        )

        embed = discord.Embed(
            colour=ColourCodes.theme_colour,
            description=f'{Emojis.koin} you **gave** `{better_numbers(amount)}` {self.currency} to {user.mention}')
        return await ctx.send(embed=embed)


    @commands.command(aliases=["cf", "coinf"])
    async def coinflip(
        self, ctx: commands.Context, 
        amount, *, side: str
        ) -> discord.Embed:
        """
        flip a coin in hopes of getting some koins

        Returns
        -------
        `discord.Embed`
         an embed with info about the job you worked and how much you earned
        """

        computer: list = ["heads", "tails"]
        choice = random.choice(computer)

        job = random.choice(self.jobs)
        account = await self.get_account(ctx.author.id)

        if side not in computer:
            embed = discord.Embed(
                colour=ColourCodes.theme_colour,
                description=f'{Emojis.error} thats not a **valid** side.. choose between `heads` and `tails`')
            return await ctx.send(embed=embed)

        if amount == "all":
            amount = account["wallet"]
        else:
            try:
                amount = int(amount)
            except ValueError:
                embed = discord.Embed(
                    colour=ColourCodes.theme_colour,
                    description=f"{Emojis.error} **invalid** amount, make sure you're **providing** a `number`")
                return await ctx.send(embed=embed)

        if amount > account["wallet"]:
            embed = discord.Embed(
                colour=ColourCodes.theme_colour,
                description=f'{Emojis.error} you dont have **enough** {self.currency}.. try a `lower` amount')
            return await ctx.send(embed=embed)

        if side != choice:
            wallet = account["wallet"] - amount

            await self.bot.db.execute(
                """
                UPDATE economy
                SET wallet = $2
                WHERE user_id = $1;
                """,
                ctx.author.id,
                wallet,
            )

            embed = discord.Embed(
                colour=ColourCodes.theme_colour,
                description=f'{Emojis.koin} it was **{choice}**.. you lost `{better_numbers(amount)}` {self.currency}')
            return await ctx.send(embed=embed)
        
        win_amount: int = amount * 2
        wallet = account["wallet"] + win_amount

        await self.bot.db.execute(
            """
            UPDATE economy
            SET wallet = $2
            WHERE user_id = $1;
            """,
            ctx.author.id,
            wallet,
        )

        embed = discord.Embed(
            colour=ColourCodes.theme_colour,
            description=f'{Emojis.koin} it was **{choice}**! you won `{better_numbers(win_amount)}` {self.currency}')

        await ctx.send(embed=embed)


    @commands.command()
    async def slots(
        self, ctx: commands.Context, 
        amount,
        ) -> discord.Embed:
        """
        try your luck and you might earn huge amounts of koins

        Parameters
        ----------
        `amount`: int
         the amount to bet

        Returns
        -------
        `discord.Embed`
         an embed with info about how much you earned or lost
        """

        account = await self.get_account(ctx.author.id)
        slots: list[str] = []

        for i in range(3):
            a = random.choice(
                [
                "🤓", "🍑", "🍪", "💙", "🥺", "🥵"
                ]
            )
            slots.append(a)

        if amount == "all":
            amount = account["wallet"]
        else:
            try:
                amount = int(amount)
            except ValueError:
                embed = discord.Embed(
                    colour=ColourCodes.theme_colour,
                    description=f"{Emojis.error} **invalid** amount, make sure you're **providing** a `number`")
                return await ctx.send(embed=embed)

        if amount > account["wallet"]:
            embed = discord.Embed(
                colour=ColourCodes.theme_colour,
                description=f'{Emojis.error} you dont have **enough** {self.currency}.. try a `lower` amount')
            return await ctx.send(embed=embed)

        embed = discord.Embed(
            colour=ColourCodes.theme_colour,
            description="doing the magic.."
        )

        loading_msg = await ctx.send(embed=embed)

        choices = " ".join(i for i in slots)
        amount_jp: int = (amount * 3)
        amount_double: int = (amount * 2)


        if slots[0] == slots[1] == slots[2]:
            wallet = account["wallet"] + amount_jp

            await self.bot.db.execute(
                """
                UPDATE economy
                SET wallet = $2
                WHERE user_id = $1;
                """,
                ctx.author.id,
                wallet,
            )

            jp_embed = discord.Embed(
                title="you hit the jackpot!",
                colour=ColourCodes.success_colour,
                description=f"{choices}\nyou won `{better_numbers(amount_jp)}` {self.currency}",
                timestamp=datetime.now()
            ).set_thumbnail(url=ctx.author.avatar)

            await loading_msg.edit(embed=jp_embed)

        elif slots[0] == slots[1] or slots[1] == slots[2] or slots[0] == slots[2]:
            wallet = account["wallet"] + amount_double

            await self.bot.db.execute(
                """
                UPDATE economy
                SET wallet = $2
                WHERE user_id = $1;
                """,
                ctx.author.id,
                wallet,
            )

            double_embed = discord.Embed(
                title="you hit a double!",
                colour=ColourCodes.success_colour,
                description=f"{choices}\nyou won `{better_numbers(amount_jp)}` {self.currency}",
                timestamp=datetime.now()
            ).set_thumbnail(url=ctx.author.avatar)

            await loading_msg.edit(embed=double_embed)

        else:
            wallet = account["wallet"] - amount

            await self.bot.db.execute(
                """
                UPDATE economy
                SET wallet = $2
                WHERE user_id = $1;
                """,
                ctx.author.id,
                wallet,
            )
            lose_embed = discord.Embed(
                title="you lost!",
                colour=ColourCodes.theme_colour,
                description=f"{choices}\nyou lost `{better_numbers(amount)}` {self.currency}",
                timestamp=datetime.now()
            ).set_thumbnail(url=ctx.author.avatar)

            await loading_msg.edit(embed=lose_embed)


    @commands.command(aliases=["rolldice", "dice"])
    async def gamble(
        self, ctx: commands.Context, 
        amount,
        ) -> discord.Embed:
        """
        try your luck and you might earn huge amounts of koins

        Parameters
        ----------
        `amount`: int
         the amount to bet

        Returns
        -------
        `discord.Embed`
         an embed with info about how much you earned or lost
        """

        account = await self.get_account(ctx.author.id)
        double_amount: int = amount * 2
        _range: int = random.randint(1, 100)

        if amount == "all":
            amount = account["wallet"]
            double_amount = amount * 2
        else:
            try:
                amount = int(amount)
                double_amount = int(amount) * 2
            except ValueError:
                embed = discord.Embed(
                    colour=ColourCodes.theme_colour,
                    description=f"{Emojis.error} **invalid** amount, make sure you're **providing** a `number`")
                return await ctx.send(embed=embed)

        if amount > account["wallet"]:
            embed = discord.Embed(
                colour=ColourCodes.theme_colour,
                description=f'{Emojis.error} you dont have **enough** {self.currency}.. try a `lower` amount')
            return await ctx.send(embed=embed)

        if _range >= 50:
            wallet = account["wallet"] + double_amount

            await self.bot.db.execute(
                """
                UPDATE economy
                SET wallet = $2
                WHERE user_id = $1;
                """,
                ctx.author.id,
                wallet,
            )

            lose_embed = discord.Embed(
                title="you won!",
                colour=ColourCodes.success_colour,
                description=f"rolled **{_range}/100** \nyou won `{better_numbers(double_amount)}` {self.currency}",
                timestamp=datetime.now()
            ).set_thumbnail(url=ctx.author.avatar)
            
            await ctx.send(embed=lose_embed)

        else:
            wallet = account["wallet"] - amount

            await self.bot.db.execute(
                """
                UPDATE economy
                SET wallet = $2
                WHERE user_id = $1;
                """,
                ctx.author.id,
                wallet,
            )

            lose_embed = discord.Embed(
                title="you lost!",
                colour=ColourCodes.theme_colour,
                description=f"rolled **{_range}/100** \nyou lost `{better_numbers(amount)}` {self.currency}",
                timestamp=datetime.now()
            ).set_thumbnail(url=ctx.author.avatar)
            
            await ctx.send(embed=lose_embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Economy(bot))
