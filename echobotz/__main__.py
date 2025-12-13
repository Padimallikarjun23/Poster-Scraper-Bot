# ruff: noqa: E402

import asyncio
import os
from datetime import datetime
from logging import Formatter

from pytz import timezone as tz
from pyrogram import idle

from config import Config
from . import LOGGER
from .core.EchoClient import EchoBot
from .core.plugs import add_plugs
from .helper.utils.db import database
from .helper.utils.bot_cmds import _get_bot_commands

try:
    from web import _start_web, _ping
    WEB_OK = True
except ImportError:
    WEB_OK = False


bot_loop = asyncio.get_event_loop()


async def main():
    def changetz(*args):
        return datetime.now(tz(Config.TIMEZONE)).timetuple()

    Formatter.converter = changetz

    await database._load_all()

    EchoBot.start()
    EchoBot.set_bot_commands(_get_bot_commands())
    LOGGER.info("Bot Cmds Set Successfully")

    me = EchoBot.get_me()
    LOGGER.info(f"Echo Bot Started as: @{me.username}")

    add_plugs()

    if Config.WEB_SERVER and WEB_OK:
        LOGGER.info("Starting web server...")
        bot_loop.create_task(_start_web())
        bot_loop.create_task(_ping(Config.PING_URL, Config.PING_TIME))
    else:
        LOGGER.info("Web server disabled")

    await idle()

    EchoBot.stop()
    LOGGER.info("Echo Client stopped.")


bot_loop.run_until_complete(main())
