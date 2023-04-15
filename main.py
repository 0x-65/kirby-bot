from asyncio import run
from logging import getLogger

import asyncpg
import discord

from discord.ext import commands

from ext import EXTENSIONS
from ext.help import KirbyHelp

from utils.classes import Config
from utils.logs import setup_logging
from utils.functions import clear_console

# check discord for a detailed list
# figure out transcripts to trim the comment at the top
# persistent views for tickets https://github.com/Rapptz/discord.py/blob/master/examples/views/persistent.py

# add soundcloud search
# purge (channel)
# make the bot DM them with a modal for booster roles?
# security check cmd
# playstation cmd
# ice cream cmd

setup_logging()
log = getLogger(__name__)


class Kirby(commands.Bot):
    """ kirby bot object """

    def __init__(self, *args, **kwargs) -> None:
        intents = discord.Intents.default()
        intents.members: bool = True
        intents.presences: bool = True
        intents.message_content: bool = True

        super().__init__(
            command_prefix = commands.when_mentioned_or(
                ",", "k ", "kirby "
                ),
            activity = discord.Activity(
                type = discord.ActivityType.watching,
                name = "over discord.gg/order"
                ),
            status = discord.Status.do_not_disturb,
            owner_ids = [
                700937948421685362, 
                484285960671068171,
                1066429319821406208
                ],
            help_command = KirbyHelp(),
            case_insensitive = True,
            max_messages = 1000,
            intents = intents
        )

    async def setup_hook(self) -> None:
        pool = await asyncpg.create_pool(
            user="postgres", password="artist",
            database="kirby", host="127.0.0.1")

        setattr(self, "db", pool)
        log.info("connected to the database")

        await self.db.execute(
            """
            CREATE TABLE IF NOT EXISTS economy (
            user_id BIGINT NOT NULL,
            inventory TEXT,
            wallet BIGINT,
            bank BIGINT,
            PRIMARY KEY (user_id)
            );
            """
            )

        await self.db.execute(
            """
            CREATE TABLE IF NOT EXISTS boosters
            (guild BIGINT, member BIGINT, role BIGINT);
            """
        )

        await self.db.execute(
            """
            CREATE TABLE IF NOT EXISTS clients
            (client_id BIGINT, date TEXT, price TEXT, months TEXT);
            """
        )

        for ext in EXTENSIONS:
            await bot.load_extension(ext)
            log.info(f"loaded {ext}")

        await bot.load_extension("jishaku")
        log.info(f"loaded jishaku")
        log.info(f"connected: {self.user} | ID: {self.user.id})")


bot = Kirby()

async def main() -> None:
    async with bot:
        await bot.start(Config.TOKEN, reconnect=True)


if __name__ == "__main__":
    clear_console()
    run(main())
