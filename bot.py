# bot.py
import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart

import env
import keyboards as kb

logging.basicConfig(level=logging.INFO)

bot = Bot(token=env.BOT_TOKEN)
dp = Dispatcher()


# هندلر استارت (/start)
@dp.message(CommandStart())
async def cmd_start(message: Message):
    text = (
        "سلام! 👋 به ربات تحلیل تکنیکال رمزارز خوش آمدید.\n\n"
        "یکی از گزینه‌های زیر را از منوی پایین انتخاب کنید:"
    )
    await message.answer(text, reply_markup=kb.main_reply_keyboard())


# دکمه رینگی: "📊 لیست ارزها و تحلیل"
@dp.message(F.text == "📊 لیست ارزها و تحلیل")
async def show_crypto_list(message: Message):
    await message.answer(
        "ارز مورد نظر خود را جهت دریافت سیگنال و تحلیل انتخاب کنید:",
        reply_markup=kb.get_crypto_page_keyboard(page=0)
    )


# دکمه رینگی: "⚙️ تنظیمات تایم‌فریم"
@dp.message(F.text == "⚙️ تنظیمات تایم‌فریم")
async def select_timeframe(message: Message):
    await message.answer(
        "تایم‌فریم پیش‌فرض تحلیل را انتخاب کنید:",
        reply_markup=kb.timeframe_inline_keyboard()
    )


# هندلر جابجایی بین صفحات دکمه‌های شیشه‌ای ارزها
@dp.callback_query(F.data.startswith("page_"))
async def handle_pagination(callback: CallbackQuery):
    page = int(callback.data.split("_")[1])
    await callback.message.edit_reply_markup(
        reply_markup=kb.get_crypto_page_keyboard(page=page)
    )
    await callback.answer()


# هندلر کلیک روی دکمه شیشه‌ای یک ارز خاص
@dp.callback_query(F.data.startswith("analyze_"))
async def handle_coin_analysis(callback: CallbackQuery):
    pair = callback.data.split("_")[1]
    await callback.answer(f"در حال دریافت دیتای {pair}...")
    
    # پیام موقت تا ساخت ماژول صرافی و تحلیل
    await callback.message.answer(
        f"📊 **تحلیل {pair}**\n\n"
        f"⏱ تایم‌فریم: {env.DEFAULT_TIMEFRAME}\n"
        "در مراحل بعدی، سیگنال RSI، MACD، مووینگ‌ها و روند بازار اینجا نمایش داده می‌شود."
    )


# هندلر تغییر تایم‌فریم
@dp.callback_query(F.data.startswith("set_tf_"))
async def handle_tf_change(callback: CallbackQuery):
    tf = callback.data.split("_")[2]
    env.DEFAULT_TIMEFRAME = tf
    await callback.answer(f"تایم‌فریم روی {tf} تنظیم شد.")
    await callback.message.edit_text(f"✅ تایم‌فریم با موفقیت به {tf} تغییر یافت.")


# جلوگیری از بسته شدن بدون پاسخ دکمه شمارنده صفحه
@dp.callback_query(F.data == "noop")
async def handle_noop(callback: CallbackQuery):
    await callback.answer()


async def main():
    print("ربات در حال اجرا است...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
