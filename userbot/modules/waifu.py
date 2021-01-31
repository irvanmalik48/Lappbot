# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.

import random
import re
from asyncio import sleep

from userbot import CMD_HELP, bot
from userbot.events import register

EMOJI_PATTERN = re.compile(
    "["
    "\U0001F1E0-\U0001F1FF"  
    "\U0001F300-\U0001F5FF"  
    "\U0001F600-\U0001F64F"  
    "\U0001F680-\U0001F6FF"  
    "\U0001F700-\U0001F77F"  
    "\U0001F780-\U0001F7FF"  
    "\U0001F800-\U0001F8FF"  
    "\U0001F900-\U0001F9FF"  
    "\U0001FA00-\U0001FA6F"  
    "\U0001FA70-\U0001FAFF"  
    "\U00002702-\U000027B0"
    "]+"
)


def deEmojify(inputString: str) -> str:
    return re.sub(EMOJI_PATTERN, "", inputString)


@register(outgoing=True, pattern=r"^\.wf(?: |$)(.*)")
async def waifu(cringe):
    text = cringe.pattern_match.group(1)
    if not text:
        if cringe.is_reply:
            text = (await cringe.get_reply_message()).message
        else:
            await cringe.answer("**No text given. Please give text or I kil.**")
            return
    animus = [20, 32, 33, 40, 41, 42, 58]
    sticcers = await bot.inline_query(
        "stickerizerbot", f"#{random.choice(animus)}{(deEmojify(text))}"
    )
    try:
        await sticcers[0].click(
            cringe.chat_id,
            reply_to=cringe.reply_to_msg_id,
            silent=True if cringe.is_reply else False,
            hide_via=True,
        )
    except Exception:
        return await cringe.edit(
            "**You cannot send inline results in this chat.**"
        )
    await sleep(5)
    await cringe.delete()


CMD_HELP.update(
    {
        "waifu":
        ">`.wf`"
        "\nUsage: Cringe anime stickers at your disposal."
    }
)