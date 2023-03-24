from datetime import timedelta
from typing import Union, Optional

import discord
from discord.ext import commands

from utils.views import Confirmation
from utils.classes import ColourCodes, Emojis


_cooldown = commands.CooldownMapping.from_cooldown(
    4.0, 15.0, commands.BucketType.user)


class Mod(
    commands.Cog, command_attrs={"cooldown": _cooldown}
    ):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot


    @commands.command(aliases=["airstrike", "bomb"])
    @commands.cooldown(2, 900, commands.BucketType.guild)
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def nuke(
        self, ctx: commands.Context, 
        channel: Optional[discord.abc.GuildChannel]
        ) -> discord.Embed:
        """
        deletes a channel and clones it

        Parameters
        ----------
        `channel`: Optional[discord.abc.GuildChannel]
         the channel to nuke (defaults to ctx.channel)

        Returns
        -------
        `discord.Embed`
         an embed with info about the nuke
        """        

        view = Confirmation()
        channel = channel or ctx.channel
        channel = discord.utils.get(ctx.guild.channels, name=channel.name)

        embed1 = discord.Embed(
            description=f"{Emojis.warning} are you sure you want to **nuke this channel**?",
            colour=ColourCodes.warning_colour)
        message = await ctx.send(embed=embed1, view=view)
        await view.wait()

        if view.value is None:
            pass

        elif view.value:
            try:
                channel = await ctx.channel.clone()
                await ctx.channel.delete()
                embed = discord.Embed(
                    description="successfully nuked the channel",
                    colour=ColourCodes.theme_colour)
                embed.set_author(name=f"{ctx.author}", icon_url=f"{ctx.author.avatar.url}")
                await channel.send(embed=embed)

            except discord.errors.Forbidden:
                embed = discord.Embed(
                    colour=ColourCodes.error_colour,
                    description=f"{Emojis.error} **my role is not high enough to do that**")
                await ctx.send(embed=embed)
        else:
            embed3 = discord.Embed(
                colour=ColourCodes.success_colour,
                description=f"{Emojis.success} cancelled **successfully**")
            await message.edit(embed=embed3)


    @commands.command(aliases=["p", "c", "clear"])
    @commands.has_permissions(manage_messages=True)
    @commands.guild_only()
    async def purge(
        self, ctx: commands.Context, limit: int
        ) -> None:
        """
        deletes a certain amount of msgs in a channel

        Parameters
        ----------
        `limit`: int
         the number of msgs to purge
        """

        try:
            await ctx.message.delete()
            await ctx.channel.purge(limit=limit)

        except discord.errors.Forbidden:
            embed = discord.Embed(
                colour=ColourCodes.error_colour,
                description=f"{Emojis.error} **my role is not high enough to do that**")
            await ctx.send(embed=embed)


    @commands.command(aliases=["nick", "nickname", "cn"])
    @commands.has_permissions(manage_nicknames=True)
    @commands.guild_only()
    async def rename(
        self, ctx: commands.Context, 
        member: discord.Member, *, nick: Optional[str]
        ) -> discord.Embed:
        """
        changes a member's nickname

        Parameters
        ----------
        `member`: discord.Member
         the member to change the nickname of
        `nick`: Optional[str]
         the new nickname of the member (defaults to the member's name)

        Returns
        -------
        `discord.Embed`
         an embed with info about the new nickname
        """

        nick = member.name if not nick else nick
        try:
            await member.edit(nick=nick)
            embed = discord.Embed(
                colour=ColourCodes.success_colour,
                description=f"{Emojis.success} changed **{member}'s** nickname to `{nick}`")
            await ctx.send(embed=embed)

        except discord.errors.Forbidden:
            embed = discord.Embed(
                colour=ColourCodes.error_colour,
                description=f"{Emojis.error} **my role is not high enough to do that**")
            await ctx.send(embed=embed)


    @commands.command(aliases=["getout"])
    @commands.has_permissions(kick_members=True)
    @commands.guild_only()
    async def kick(
        self, ctx: commands.Context, 
        member: discord.Member, *, reason: Optional[str]
        ) -> discord.Embed:
        """
        kicks a member

        Parameters
        ----------
        `member`: discord.Member
         the member to kick

        Returns
        -------
        `discord.Embed`
         an embed with info about the kicked member
        """

        if member is ctx.author:
            return await ctx.send("just leave the server dumbass")

        if member is self.bot.user:
            return await ctx.send("no")

        await ctx.guild.kick(member, reason=reason)

        embed = discord.Embed(
            colour=ColourCodes.success_colour,
            description=f"{Emojis.success} **{member}** was **kicked**")

        await ctx.send(embed=embed)


    @commands.command(aliases=["role", "arole", "gr"])
    @commands.has_permissions(manage_roles=True)
    @commands.guild_only()
    async def addrole(
        self, ctx: commands.Context, 
        member: Optional[discord.Member], *, roles: str
        ) -> discord.Embed:
        """
        adds role(s) to a member

        Parameters
        ----------
        `member`: discord.Member
         the member to add role(s) to (defaults to ctx.author)
        `role`: str
         the role(s) to add to the member

        Returns
        -------
        `discord.Embed`
         an embed with info about the added role(s)
        """

        converter = commands.RoleConverter()
        member = member or ctx.author
        seperator = ","

        roles = [
            await converter.convert(ctx, role) for role in roles.replace(", ", ",").split(seperator)
            ]
        mention_roles = ", ".join([str(role.mention) for role in roles])
        
        if all(member.get_role(int(role.id))
            for role in roles
                ):

            await member.remove_roles(*roles)
            embed = discord.Embed(
                description=f"{Emojis.success} **removed** {mention_roles} from {member.mention}",
                colour=ColourCodes.success_colour)
            await ctx.send(embed=embed)
        else:
            await member.add_roles(*roles)
            embed = discord.Embed(
                description=f"{Emojis.success} **added** {mention_roles} to {member.mention}",
                colour=ColourCodes.success_colour)
            await ctx.send(embed=embed)


    @commands.command(aliases=["crole", "cr"])
    @commands.has_permissions(manage_roles=True)
    @commands.guild_only()
    async def createrole(
        self, ctx: commands.Context,
        colour: Optional[Union[discord.Color, int]], 
        *, name: str
        ) -> discord.Embed:
        """
        creates a role

        Parameters
        ----------
        `hex`: Optional[Union[discord.Color, int]]
         the hex of the role
        `name`: str
         the name of the role

        Returns
        -------
        `discord.Embed`
         an embed with info about the created role
        """

        colour = colour or discord.Color.default()
        await ctx.guild.create_role(name=name, colour=colour)

        embed = discord.Embed(
            colour=ColourCodes.success_colour,
            description=f"{Emojis.success} **created** the role `{name}` with the hex `{colour}`")

        await ctx.send(embed=embed)


    @commands.command(aliases=["drole", "dr"])
    @commands.has_permissions(manage_roles=True)
    @commands.guild_only()
    async def deleterole(
        self, ctx: commands.Context, *, name: str
        ) -> discord.Embed:
        """
        deletes a role

        Parameters
        ----------
        `name`: str
         the name of the role

        Returns
        -------
        `discord.Embed`
         an embed with info about the deleted role
        """

        role = discord.utils.get(ctx.guild.roles, name=name)
        await role.delete()

        embed = discord.Embed(
            colour=ColourCodes.success_colour,
            description=f"{Emojis.success} **deleted** the role `{name}`")

        await ctx.send(embed=embed)


    @commands.command(aliases= ["vote"])
    @commands.has_guild_permissions(manage_messages=True)
    @commands.guild_only()
    async def poll(
        self, ctx: commands.Context, *, message: str
        ) -> discord.Embed:
        """
        starts a poll

        Parameters
        ----------
        `message:` str
         the message to start a poll about

        Returns
        -------
        `discord.Embed`
         an embed with info about the poll
        """        

        await ctx.message.delete()

        embed = discord.Embed(
            title="poll", 
            description=f"{message}", 
            colour=ColourCodes.theme_colour)
        embed.set_footer(text=f"started by {ctx.author}")

        msg = await ctx.send(embed=embed)

        await msg.add_reaction(f"{Emojis.success}")
        await msg.add_reaction(f"{Emojis.error}")


    @commands.command(aliases=["lockdown"])
    @commands.has_guild_permissions(manage_channels=True)
    @commands.guild_only()
    async def lock(
        self, ctx: commands.Context, 
        channel: Optional[discord.TextChannel]
        ) -> discord.Embed:
        """
        locks a channel

        Parameters
        ----------
        `channel`: Optional[discord.TextChannel]
         the channel to lock

        Returns
        -------
        `discord.Embed`
         an embed with info about the locked channel
        """      

        channel = channel or ctx.channel
        await channel.set_permissions(ctx.guild.default_role, send_messages=False)

        embed = discord.Embed(
            colour=ColourCodes.success_colour,
            description=f"{Emojis.success} {channel.mention} is now on lockdown mode")

        await ctx.send(embed=embed)


    @commands.command()
    @commands.has_guild_permissions(manage_channels=True)
    @commands.guild_only()
    async def unlock(
        self, ctx: commands.Context, 
        channel: Optional[discord.TextChannel]
        ) -> discord.Embed:
        """
        unlocks a channel

        Parameters
        ----------
        `channel`: Optional[discord.TextChannel]
         the channel to unlock

        Returns
        -------
        `discord.Embed`
         an embed with info about the unlocked channel
        """        

        channel = channel or ctx.channel
        await channel.set_permissions(ctx.guild.default_role, send_messages=True)

        embed = discord.Embed(
            colour=ColourCodes.success_colour,
            description=f"{Emojis.success} {channel.mention} is now unlocked")

        await ctx.send(embed=embed)


    @commands.command()
    @commands.has_permissions(manage_channels=True)
    @commands.guild_only()
    async def slowmode(
        self, ctx: commands.Context, 
        duration: Optional[int]
        ) -> discord.Embed:
        """
        enables slowmode in a channel

        Parameters
        ----------
        `duration`: Optional[int]
         the duration for the slowmode (defaults to 0)

        Returns
        -------
        `discord.Embed`
         an embed with info about the slowmode
        """   

        duration = 0 if not duration else duration
        await ctx.channel.edit(slowmode_delay=duration)

        embed = discord.Embed(
            colour=ColourCodes.success_colour,
            description=f"{Emojis.success} slowmode was set to `{duration}` secs")

        await ctx.send(embed=embed)


    @commands.command(aliases=["rip", "die", "smoke"])
    @commands.has_permissions(ban_members=True)
    @commands.guild_only()
    async def ban(
        self, ctx: commands.Context, 
        user: Union[discord.Member, discord.User], 
        *, reason: Optional[str]
        ) -> discord.Embed:
        """
        bans a member or a user

        Parameters
        ----------
        `user`: Union[discord.Member, discord.User]
         the member or user to ban
        `reason`: Optional[str]
         the reason for the ban (defaults to the ban author)

        Returns
        -------
        `discord.Embed`
         an embed with info about the ban
        """        

        reason = f"banned by {ctx.author}" if not reason else reason

        if user is ctx.author:
            return await ctx.send("just leave the server retard")

        if user is self.bot.user:
            return await ctx.send("no")

        bans = [entry.user.id async for entry in ctx.guild.bans()]
    
        if user.id in bans:
            embed = discord.Embed(
                colour=ColourCodes.error_colour,
                description=f"{Emojis.error} **{user}** is already `banned`")
            await ctx.send(embed=embed)
        else:
            await ctx.guild.ban(user, reason=reason)
            embed = discord.Embed(
                colour=ColourCodes.success_colour,
                description=f"{Emojis.success} **{user}** got smoked 🚬")
            await ctx.send(embed=embed)


    @commands.command()
    @commands.has_permissions(ban_members=True)
    @commands.guild_only()
    async def unban(
        self, ctx: commands.Context,
        *, user: discord.User
        ) -> discord.Embed:
        """
        unbans a user

        Parameters
        ----------
        `user`: discord.User
         the user to unban

        Returns
        -------
        `discord.Embed`
         an embed with info about the unban
        """

        try:
            await ctx.guild.unban(user)
            embed = discord.Embed(
                colour=ColourCodes.success_colour,
                description=f"{Emojis.success} **{user}** was unbanned")
            await ctx.send(embed=embed)

        except discord.errors.NotFound:
            embed = discord.Embed(
                colour=ColourCodes.error_colour,
                description=f"{Emojis.error} **{user}** is not `banned`")
            await ctx.send(embed=embed)


    @commands.command(aliases=["bc", "bans"])
    @commands.has_permissions(manage_messages=True)
    @commands.guild_only()
    async def bancount(self, ctx: commands.Context) -> discord.Embed:
        """
        shows the number of banned users in the guild

        Returns
        -------
        `discord.Embed`
         an embed with info about the number of banned users
        """

        bancount = 0
        banlist = ctx.guild.bans()

        if banlist is None:
            embed = discord.Embed(
                colour=ColourCodes.warning_colour, 
                description=f"{Emojis.warning} **no banned users yet**")
            await ctx.send(embed=embed)

        else:
            async for _ in banlist:
                bancount += 1

            embed = discord.Embed(
                colour=ColourCodes.theme_colour,
                description=f"{Emojis.mod} `{bancount}` **banned** users")
            await ctx.send(embed=embed)


    @commands.command(aliases=["isbanned"])
    @commands.has_permissions(ban_members=True)
    @commands.guild_only()
    async def banned(
        self, ctx: commands.Context, 
        *, user: discord.User
        ) -> discord.Embed:
        """
        checks if a user is banned or not

        Parameters
        ----------
        user : discord.User
         the user to check

        Returns
        -------
        `discord.Embed`
         an embed with info about the user's ban state
        """

        bans = [entry.user.id async for entry in ctx.guild.bans()]
        
        if user.id in bans:
            await ctx.send(f"**{user}** is banned")
        else:
            await ctx.send(f"**{user}** is not banned")


    @commands.command(aliases=["unbanall", "massun", "munban"])
    @commands.has_permissions(administrator=True)
    @commands.cooldown(2, 1000, commands.BucketType.guild)
    @commands.guild_only()
    async def massunban(self, ctx: commands.Context) -> discord.Embed:
        """
        unbans every user in the guild

        Returns
        -------
        `discord.Embed`
         an embed with info on whether to massunban or not
        """        

        view = Confirmation()
        unbanned: int = 0

        embed1 = discord.Embed(
            description=f"{Emojis.warning} are you sure you want to **unban everyone**?",
            colour=ColourCodes.warning_colour)
        message = await ctx.send(embed=embed1, view=view)
        await view.wait()

        if view.value is None:
            pass

        elif view.value:
            async for user in ctx.guild.bans():
                await ctx.guild.unban(user=user.user)
                unbanned += 1

                embed2 = discord.Embed(
                    colour=ColourCodes.success_colour,
                    description=f"{Emojis.success} **unbanned** `{unbanned}` members")
                await message.edit(embed=embed2)
        else:
            embed3 = discord.Embed(
                colour=ColourCodes.success_colour,
                description=f"{Emojis.success} cancelled **successfully**")
            await message.edit(embed=embed3)


async def setup(bot: commands.Bot):
    await bot.add_cog(Mod(bot))
