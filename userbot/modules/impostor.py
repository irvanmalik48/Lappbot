from telethon.tl.functions.account import UpdateProfileRequest
from telethon.tl.functions.photos import (DeletePhotosRequest,
                                          UploadProfilePhotoRequest)
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import InputPhoto

from userbot import CMD_HELP, LOGS, STORAGE, bot
from userbot.events import register

if not hasattr(STORAGE, "userObj"):
    STORAGE.userObj = False


@register(outgoing=True, pattern=r"^\.take ?(.*)")
async def take(event):
    inputArgs = event.pattern_match.group(1)

    if "back" in inputArgs:
        await event.edit("**Reverting...**")
        if not STORAGE.userObj:
            return await event.edit(
                "**Take some identity then come back.**")
        await updateProfile(STORAGE.userObj, restore=True)
        return await event.edit("**Glad to be me.**")
    elif inputArgs:
        try:
            user = await event.client.get_entity(inputArgs)
        except:
            return await event.edit("**Invalid username/ID.")
        userObj = await event.client(GetFullUserRequest(user))
    elif event.reply_to_msg_id:
        replyMessage = await event.get_reply_message()
        if replyMessage.sender_id is None:
            return await event.edit(
                "**Can't take anonymous admins' identity.**")
        userObj = await event.client(GetFullUserRequest(replyMessage.sender_id)
                                     )
    else:
        return await event.edit(
            "**Do** `.help impostor` **to learn how to use it.**")

    if not STORAGE.userObj:
        STORAGE.userObj = await event.client(
            GetFullUserRequest(event.sender_id))

    LOGS.info(STORAGE.userObj)

    await event.edit("**Taking target's identity...**")
    await updateProfile(userObj)
    await event.edit("**Hello, me.**")


async def updateProfile(userObj, restore=False):
    firstName = "Deleted Account" if userObj.user.first_name is None else userObj.user.first_name
    lastName = "" if userObj.user.last_name is None else userObj.user.last_name
    userAbout = userObj.about if userObj.about is not None else ""
    userAbout = "" if len(userAbout) > 70 else userAbout
    if restore:
        userPfps = await bot.get_profile_photos('me')
        userPfp = userPfps[0]
        await bot(
            DeletePhotosRequest(id=[
                InputPhoto(id=userPfp.id,
                           access_hash=userPfp.access_hash,
                           file_reference=userPfp.file_reference)
            ]))
    else:
        try:
            userPfp = userObj.profile_photo
            pfpImage = await bot.download_media(userPfp)
            await bot(
                UploadProfilePhotoRequest(await bot.upload_file(pfpImage)))
        except BaseException:
            pass
    await bot(
        UpdateProfileRequest(about=userAbout,
                             first_name=firstName,
                             last_name=lastName))


CMD_HELP.update({
    "impostor":
    ">`.take` (as a reply to a message of a user)\
    \nUsage: Steals the user's identity.\
    \n\n>`.take <username/ID>`\
    \nUsage: Steals the given username/ID's identity.\
    \n\n>`.take back`\
    \nUsage: Revert back to your true identity.\
    \n\n**Always revert before running it again.**\
"
})
