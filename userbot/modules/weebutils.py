import random
import re
import nekos
from asyncio import sleep

from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError

from userbot import CMD_HELP, bot
from userbot.events import register


@register(outgoing=True, pattern="^.nhentai(?: |$)(.*)")
async def _(hentai):
    if hentai.fwd_from:
        return
    link = hentai.pattern_match.group(1)
    if not link:
        return await hentai.edit("**I can't search nothing**")
    chat = "@nHentaiBot"
    await hentai.edit("**Processing...**")
    async with bot.conversation(chat) as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=424466890)
            )
            msg = await bot.send_message(chat, link)
            response = await response
            """ - don't spam notif - """
            await bot.send_read_acknowledge(conv.chat_id)
        except YouBlockedUserError:
            await hentai.reply("**Please unblock @nHentaiBot and try again**")
            return
        if response.text.startswith("**Sorry I couldn't get manga from**"):
            await hentai.edit("**I think this is not the right link**")
        else:
            await hentai.delete()
            await bot.send_message(hentai.chat_id, response.message)
            await bot.send_read_acknowledge(hentai.chat_id)
            """ - cleanup chat after completed - """
            await hentai.client.delete_messages(conv.chat_id, [msg.id, response.id])

# =============================================== #

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
    await cringe.delete()

# Copyright (C) 2021 Bian Sepang
# All Rights Reserved.

@register(pattern=r"^\.hentai$", outgoing=True)
async def _(event):
    await event.edit("**Fetching...**")
    pic = nekos.img("random_hentai_gif")
    await event.client.send_file(
        event.chat_id,
        pic,
        caption=f"[Source]({pic})",
    )
    await event.delete()


@register(pattern=r"^\.pussy$", outgoing=True)
async def _(event):
    await event.edit("**Fetching...**")
    pic = nekos.img("pussy")
    await event.client.send_file(
        event.chat_id,
        pic,
        caption=f"[Source]({pic})",
    )
    await event.delete()


@register(pattern=r"^\.cum$", outgoing=True)
async def _(event):
    """Gets anime cum gif from nekos.py."""
    await event.edit("**Fetching...**")
    pic = nekos.img("cum")
    await event.client.send_file(
        event.chat_id,
        pic,
        caption=f"[Source]({pic})",
    )
    await event.delete()


@register(pattern=r"^\.nsfwneko$", outgoing=True)
async def _(event):
    """Gets nsfw neko gif from nekos.py."""
    await event.edit("**Fetching...**")
    pic = nekos.img("nsfw_neko_gif")
    await event.client.send_file(
        event.chat_id,
        pic,
        caption=f"[Source]({pic})",
    )
    await event.delete()

CMD_HELP.update(
    {
        "weebutils": 
        "`.nhentai <link / code>`"
        "\nUsage: View nhentai in telegraph page."
        "\n\n`.wf <text>`"
        "\nUsage: Cringe anime stickers in your disposal."
        "\n\n`.hentai`"
        "\nUsage: Gets random hentai gif from nekos."
        "\n\n`.pussy`"
        "\nUsage: Gets anime pussy gif from nekos."
        "\n\n`.cum`"
        "\nUsage: Gets anime cum gif from nekos."
        "\n\n`.nsfwneko`"
        "\nUsage: Gets nsfw neko gif from nekos."
    }
)