from aiogram import Bot, Dispatcher, F
from aiogram.enums import ParseMode, ChatType
from aiogram.types import ChatMemberUpdated, ChatPermissions, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.filters import ChatMemberUpdatedFilter, JOIN_TRANSITION

bot = Bot(token="8383046541:AAF_sxAovMUE-s5njPLoZMmH5heUg5UJbk8")
dp = Dispatcher(disable_fsm=True)


@dp.chat_member(ChatMemberUpdatedFilter(JOIN_TRANSITION), F.chat.type != ChatType.PRIVATE)
async def user_added(event: ChatMemberUpdated):
    await bot.restrict_chat_member(event.chat.id, event.new_chat_member.user.id, permissions=ChatPermissions(
        can_send_messages=False, can_send_media_messages=False, can_send_polls=False, can_send_other_messages=False,
        can_add_web_page_previews=False, can_invite_users=False, can_change_info=False, can_delete_messages=False,
        can_pin_messages=False, can_send_audios=False, can_send_videos=False, can_send_stickers=False,
        can_send_photos=False, can_send_games=False))
    await bot.send_message(event.chat.id, f"Здравствуйте! Это антиспам проверка. Нажмите кнопку ниже:",
                           parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text="Я - человек!", callback_data=f"human_{event.new_chat_member.user.id}")]]
        ))


@dp.callback_query(F.data.startswith("human_"))
async def human_verified(call: CallbackQuery):
    human_id = int(call.data.split("_")[1])
    if call.from_user.id != human_id:
        await call.answer('Эта кнопка не для вас!')
        return
    await bot.restrict_chat_member(call.message.chat.id, call.from_user.id, permissions=ChatPermissions(
        can_send_messages=True, can_send_media_messages=True, can_send_polls=True, can_send_other_messages=True,
        can_add_web_page_previews=True, can_invite_users=True, can_change_info=True, can_delete_messages=True,
        can_pin_messages=True, can_send_audios=True, can_send_videos=True, can_send_stickers=True,
        can_send_photos=True, can_send_games=True))
    await call.answer("Приятного общения!")
    await call.message.delete()


def main():
    dp.run_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == '__main__':
    main()
