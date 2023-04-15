from textwrap import dedent

import discord

from discord.ext import commands, tasks
from utils.classes import Emojis, ColourCodes
from ext.economy import Economy


class Events(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.vanity_check.start()


    @tasks.loop(seconds=2)
    async def vanity_check(self) -> None:
        """ checks if the member has a certain keyword in their status """

        guild = self.bot.get_guild(705778500782653473)
        role = guild.get_role(927137948145684500)
        vanity: str = f"/{guild.vanity_url_code}" if guild.vanity_url_code else "/YxkSp5fKG3"

        for member in guild.members:
            if vanity in str(member.activity) and not role in member.roles:
                await member.add_roles(role)

            elif vanity not in str(member.activity) and role in member.roles:
                await member.remove_roles(role)


    @vanity_check.before_loop
    async def before_my_task(self):
        await self.bot.wait_until_ready()


    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        '''checks if the booster role was deleted to remove it from the database'''

        data = await self.bot.db.fetch(
        '''
        SELECT role
        FROM boosters WHERE guild = $1
        ''', role.guild.id)

        if data:
            for table in data:
                custom_role = role.guild.get_role(table.get('role'))
                if role.id == custom_role.id:
                    await self.bot.db.execute(
                        "DELETE FROM boosters WHERE role = $1", 
                        custom_role.id
                        )


    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        '''checks if the member is boosting or not to keep/remove their custom role'''

        data = await self.bot.db.fetch(
        '''
        SELECT member, role, guild
        FROM boosters''')

        if data:
            for table in data:
                guild = self.bot.get_guild(table.get('guild'))
                await guild.chunk()
                member = guild.get_member(table.get('member'))
                custom_role = guild.get_role(table.get('role'))
                booster_role = guild.premium_subscriber_role
                channel = guild.system_channel

                if booster_role not in after.roles and custom_role in before.roles:
                    await custom_role.delete()
                    await self.bot.db.execute(
                        '''
                        DELETE FROM boosters
                        WHERE member = $1''', int(member.id))

                    embed = discord.Embed(
                        color=ColourCodes.theme_colour,
                        description=f'{Emojis.warning} **{str(after)}** is no longer boosting so their role was **deleted**')
                    return await channel.send(embed=embed)
                else:
                    pass


    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        """ sends a msg when a member joins the guild """

        channel = self.bot.get_channel(1086735157463089223)

        welc_embed = discord.Embed(
            colour=ColourCodes.theme_colour,
            description="**check** <#998868431396937788> to order a **custom bot**")

        await channel.send(f"welcome {member.mention}", embed=welc_embed)


    @commands.Cog.listener()
    async def on_message(self, message):
        """ sends a msg when a member boosts the guild """

        message_types: list = [
            discord.MessageType.premium_guild_subscription,
            discord.MessageType.premium_guild_tier_1,
            discord.MessageType.premium_guild_tier_2,
            discord.MessageType.premium_guild_tier_3
            ]

        if message.type in message_types:
            await message.delete()
            
            info = await Economy.get_account(self, message.author.id)
            new_balance: int = info["wallet"] + 100000

            await self.bot.db.execute(
                """
                UPDATE economy 
                SET wallet = $1
                WHERE user_id = $2
                """, new_balance, message.author.id)

            embed = discord.Embed(
                colour=ColourCodes.theme_colour,
                description=dedent(f"""
                `+` thx for **boosting** {message.author.mention}
                `+` check **pinned msgs** for perks""")
                )

            embed.set_footer(text=f"100k koins have been added to your wallet")
            embed.set_author(
                name=f"{message.guild.premium_subscription_count} boosts",
                icon_url="https://cdn.discordapp.com/emojis/906898503773597696.webp")

            await message.channel.send(embed=embed)
        
        elif message.content == "donate":
                await message.channel.send("check <#998868431396937788> for instructions on how to donate")


async def setup(bot: commands.Bot):
    await bot.add_cog(Events(bot))
