import os
import re
import tldextract
from pyrogram import emoji, Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ForceReply
from .. import filters
from mega.database.files import MegaFiles
from mega.database.users import MegaUsers
from mega.helpers.downloader import Downloader
from mega.helpers.media_info import MediaInfo
from mega.helpers.screens import Screens
from mega.helpers.ytdl import YTdl
pyrogram.Client.on_message(pyrogram.filters.document)
async def document(bot,update):
  await bot.send_message(
         chat_id=update.chat.id,
         text = "hi",
         reply_markup=InlineKeyboardMarkup(
     [
                [         InlineKeyboardButton(text=f"{emoji.PENCIL} Rename",
                                         callback_data=f"rename")
                ]
            ]
      ),
         
        
       
  reply_to_message_id=update.message_id

)





          



@Client.on_callback_query(filters.callback_query("rename"), group=1)
async def callback_rename_handler(c: Client, cb: CallbackQuery):
    await cb.answer()

    params = cb.payload.split('_')
    cb_message_id = int(params[1]) if len(params) > 1 else None

    await cb.message.reply_text(
        f"RENAME_{cb_message_id}:\n"
        f"Send me the new name of the file as a reply to this message.",
        reply_markup=ForceReply(True)
    )


@Client.on_message(filters.reply & filters.private, group=1)
async def reply_message_handler(c: Client, m: Message):
    func_message_obj = str(m.reply_to_message.text).splitlines()[0].split("_")
    if len(func_message_obj) > 1:
        func = func_message_obj[0]
        org_message_id = int(str(func_message_obj[1]).replace(":", ""))
        org_message = await c.get_messages(m.chat.id, org_message_id)
        if func == "RENAME":
            new_file_name = m.text

            ack_message = await m.reply_text(
                "About to start downloading the file to Local."
            )

            await Downloader().download_file(org_message.text, ack_message, new_file_name)
