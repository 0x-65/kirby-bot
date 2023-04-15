import discord

from discord.ext import commands
from utils.classes import Emojis, ColourCodes


class ErrorHandler(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot


    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.MissingRequiredArgument):
            return await ctx.send_help(ctx.command)


        if isinstance(error, commands.BadArgument):
            return await ctx.send_help(ctx.command)


        if isinstance(error, commands.NotOwner):
            embed = discord.Embed(
                colour=ColourCodes.theme_colour,
                description=f"{Emojis.warning} you are not the **bot owner**")
            return await ctx.reply(embed=embed, mention_author=False)


        if isinstance(error, commands.CommandOnCooldown):
            if error.retry_after > 120:
                error = f"`{round(error.retry_after / 60)}` minutes"
            else:
                error = f"`{round(error.retry_after)}` seconds"
            embed = discord.Embed(
                colour=ColourCodes.theme_colour,
                description=f"{Emojis.warning} **cooling down..** try again in {error}")
            return await ctx.reply(embed=embed, mention_author=False)


        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                color=ColourCodes.theme_colour,
                description=f"{Emojis.warning} you are **not allowed** to `execute` this command")
            return await ctx.reply(embed=embed, mention_author=False)


        if isinstance(error, commands.BotMissingPermissions):
            embed = discord.Embed(
                color=ColourCodes.theme_colour,
                description=f"{Emojis.error} im **not allowed** to `execute` this command")
            return await ctx.reply(embed=embed, mention_author=False)


        if isinstance(error, commands.GuildNotFound):
            embed = discord.Embed(
                color=ColourCodes.theme_colour,
                description=f"{Emojis.error} I was **unable** to find that `guild`")
            return await ctx.reply(embed=embed, mention_author=False)


        if isinstance(error, commands.RoleNotFound):
            embed = discord.Embed(
                color=ColourCodes.theme_colour,
                description=f"{Emojis.error} I was **unable** to find that `role`")
            return await ctx.reply(embed=embed, mention_author=False)


        if isinstance(error, commands.ChannelNotFound):
            embed = discord.Embed(
                colour=ColourCodes.theme_colour,
                description=f"{Emojis.error} I was **unable** to find that `channel`**")
            return await ctx.reply(embed=embed, mention_author=False)


        if isinstance(error, commands.MemberNotFound):
            embed = discord.Embed(
                color=ColourCodes.theme_colour,
                description=f"{Emojis.error} I was **unable** to find that `member`")
            return await ctx.reply(embed=embed, mention_author=False)


        if isinstance(error, commands.UserNotFound):
            embed = discord.Embed(
                colour=ColourCodes.theme_colour,
                description=f"{Emojis.error} I was **unable** to find that `user`")
            return await ctx.reply(embed=embed, mention_author=False)


        if isinstance(error, commands.NoPrivateMessage):
            embed = discord.Embed(
                color=ColourCodes.theme_colour,
                description=f"{Emojis.error} this command **cannot** be used in `private messages`")
            return await ctx.reply(embed=embed, mention_author=False)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(ErrorHandler(bot))

