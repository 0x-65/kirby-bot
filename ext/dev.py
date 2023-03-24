from random import choice
from datetime import datetime
from typing import Optional, Union, List

import discord
from discord.ext import commands

from ext import EXTENSIONS
from utils.functions import restart_bot
from utils.classes import Emojis, ColourCodes


class Panel(discord.ui.View):
    """ execute owner cmds via buttons """

    def __init__(self) -> None:
        super().__init__()
        self.value = None


    @discord.ui.button(
        label="1",
        row=1,
        style=discord.ButtonStyle.secondary
        )

    async def shutdown(
        self, interaction: discord.Interaction, button: discord.ui.Button
        ) -> discord.Embed:
        owner_id: int = interaction.client.application.owner.id
        
        if interaction.user.id != owner_id:
            warning_embed = discord.Embed(
                colour=ColourCodes.warning_colour,
                description=f"{Emojis.warning} you are not the **bot owner**"
                )
            return await interaction.response.send_message(
                embed=warning_embed, ephemeral=True)

        for child in self.children: 
            child.disabled=True

        embed = discord.Embed(
            colour=ColourCodes.success_colour,
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

        owner_id: int = interaction.client.application.owner.id
        
        if interaction.user.id != owner_id:
            warning_embed = discord.Embed(
                colour=ColourCodes.warning_colour,
                description=f"{Emojis.warning} you are not the **bot owner**"
                )
            return await interaction.response.send_message(
                embed=warning_embed, ephemeral=True)

        for child in self.children:
            child.disabled=True

        extensions: str = f"\n├── {Emojis.success}".join(f"`{e}`" for e in EXTENSIONS)

        embed = discord.Embed(
            colour=ColourCodes.success_colour,
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
        owner_id: int = interaction.client.application.owner.id

        if interaction.user.id != owner_id:
            warning_embed = discord.Embed(
                colour=ColourCodes.warning_colour,
                description=f"{Emojis.warning} you are not the **bot owner**"
                )
            return await interaction.response.send_message(
                embed=warning_embed, ephemeral=True)

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


class Developer(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot


    @commands.command(hidden=True)
    @commands.is_owner()
    async def toggle(
        self, ctx: commands.Context, *, cmd_name: str
        ) -> discord.Embed:
        """
        enables or disables a command

        Parameters
        ----------
        `cmd_name`: str
         the name of the command to enable or disable    
        """        

        cmd = self.bot.get_command(cmd_name)
        keyword: str = ""

        if cmd.enabled:
            cmd.update(enabled=False)
            keyword = "disabled"
        else:
            cmd.update(enabled=True)
            keyword = "enabled"

        embed = discord.Embed(
            colour=ColourCodes.success_colour,
            description=f"{Emojis.success} **{cmd.qualified_name}** is now **{keyword}**")
        await ctx.send(embed=embed)


    @commands.command(aliases=["embedcode", "ec"], hidden=True)
    @commands.is_owner()
    async def copyembed(
        self, ctx: commands.Context,
        message: Optional[discord.Message]=None
        ) -> discord.Embed:
        """
        gets the code of an embed

        Parameters
        ----------
        `message`: discord.Message
         (optional, defaults to ctx.message.reference)

        Returns
        -------
        `discord.Embed`
         an embed with info about the code
        """
        
        if not message:
            if not ctx.message.reference:
                return
            message=ctx.message.reference.resolved
            
        if not message.embeds:
            return
        
        embed=message.embeds[0]
        code="{embed}"
        if embed.description:
            code+="{description: "+embed.description+"}"
            
        if embed.title:
            code+="$v{title: "+embed.title+"}"
            
        if embed.footer:
            x=""
            if embed.footer.text:
                x+=embed.footer.text
            if embed.footer.icon_url:
                x+=f" && icon: {embed.footer.icon_url}"
            code+="$v{footer: "+x+"}"
            
        if embed.thumbnail:
            code+="$v{thumbnail: "+embed.thumbnail.url+"}"
            
        if embed.image:
            code+="$v{image: "+embed.image.url+"}"
            
        if embed.fields:
            for field in embed.fields:
                x=""
                n=field.name
                v=field.value
                i=field.inline
                x+=f"{n} && value: {v} && inline: {'true' if i else 'false'}"
                code+="$v{field: "+x+"}"
                
        if embed.author:
            x=""
            n=embed.author.name
            i=embed.author.icon_url
            u=embed.author.url
            x+=n
            if i:
                x+=f" && icon: {i}"
            if u: 
                x+=f" && url: {u}"
            code+="$v{author: "+x+"}"
                
        if embed.timestamp:
            code+="$v{timestamp: true}"
            
        if message.components:
            comp=message.components[0]
            if isinstance(comp, discord.ActionRow):
                for button in comp.children:
                    if button.style == discord.ButtonStyle.link:
                        x=""
                        l=button.label
                        u=button.url
                        x+=f"{l} && link: {u}"
                        code+="$v{label: "+x+"}"
                        
        if embed.color:
            if embed.color.value == 0:
                code+="$v{color: #000000}"
            else:
                c=hex(embed.color.value).replace("0x", "")
                code+="$v{color: "+c+"}"
                
        code+="$v"

        embed = discord.Embed(colour=ColourCodes.theme_colour)

        embed.set_footer(text="use this code to create embeds easily")
        embed.add_field(name="", value=f"```{code}```")

        return await ctx.reply(embed=embed)


    @commands.command(hidden=True)
    @commands.is_owner()
    async def panel(self, ctx: commands.Context) -> discord.Embed:
        """ basically to run commands easier lol """

        value: str = ""
        cmds: list = [
            Panel.shutdown.__name__,
            Panel.restart.__name__,
            Panel.guildlist.__name__
            ]

        for count, cmd in enumerate(cmds, start=1):
            value += f"`{count}` | `{cmd}`\n"

            embed = discord.Embed(
                colour=ColourCodes.theme_colour,
                description=value)

        await ctx.send(embed=embed, view=Panel())


    @commands.command(aliases=["link", "inv"], hidden=True)
    @commands.is_owner()
    async def guildinvite(
        self, ctx: commands.Context, *, guild: Optional[discord.Guild]
        ) -> discord.Invite:
        """
        gets an invite link to a guild

        Parameters
        ----------
        `guild`: discord.Guild
         (optional, defaults to ctx.guild)

        Returns
        -------
        `discord.Invite`
         the invite link of the guild
        """

        await ctx.message.delete()

        owner: discord.User = self.bot.get_user(700937948421685362)
        guild: discord.Guild = ctx.guild or self.bot.get_guild(guild)
        link: discord.Invite = await choice(
            guild.text_channels).create_invite(max_age=0, max_uses=0)

        await owner.send(f"**invite:** {link}")


    @commands.command(aliases=["webs"], hidden=True)
    @commands.is_owner()
    async def webhooks(
        self, ctx: commands.Context, *, guild: Optional[discord.Guild]
        ) -> discord.Embed:
        """
        lists all the webhooks in the guild

        Parameters
        ----------
        `guild`: Optionaldiscord.Guild]
         (optional, defaults to ctx.guild)

        Returns
        -------
        `discord.Embed`
         an embed containing all the webhooks in the guild
        """

        guild: discord.Guild = ctx.guild or self.bot.get_guild(guild)
        webs: list = await guild.webhooks()
        webhooks: str = ""

        for count, webhook in enumerate(webs, start=1):
            webhooks += f"`{count}` [{webhook.name}]({webhook.url}) {webhook.channel}\n"

            embed = discord.Embed( 
                colour=ColourCodes.theme_colour, 
                description=webhooks
            ).set_author(name=guild.name, icon_url=guild.icon)

        await ctx.send("no webhooks found") if len(webs) <= 0 else await ctx.send(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Developer(bot))
