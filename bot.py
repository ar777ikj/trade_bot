import asyncio
import logging
import ccxt.async_support as ccxt
import pandas as pd
import pandas_ta as ta

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command

from config import (
    BOT_TOKEN,
    EXCHANGE_API_KEY,
    EXCHANGE_SECRET_KEY,
    TIMEFRAME,
    LIMIT
)
from keyboards import (
    get_main_menu,
    get_pairs_keyboard,
    get_pair_actions_keyboard
)

# ۱. راه‌اندازی لاگ‌ها برای خطایابی بهتر
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 2.اتصال از کتابخانه  ccxt به binance یا kucoin 
exchange = ccxt.coinex({
    'apiKey': EXCHANGE_API_KEY or '',
    'secret': EXCHANGE_SECRET_KEY or '',
    'enableRateLimit': True,
})

# ۳. راه‌اندازی ربات و دیسپچر
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


# *** توابع کمکی تحلیل تکنیکال و قیمت ***

async def fetch_ticker_price(symbol: str) -> float | None:
    """دریافت آخرین قیمت لحظه‌ای یک جفت‌ارز"""
    try:
        ticker = await exchange.fetch_ticker(symbol)
        return ticker.get('last')
    except Exception as e:
        logger.error(f"Error fetching ticker for {symbol}: {e}")
        return None


async def analyze_symbol(symbol: str) -> str:
    """دریافت کندل‌ها و محاسبه اندیکاتورهای RSI و MACD و EMA"""
    try:
        # دریافت کندل‌های OHLCV
        ohlcv = await exchange.fetch_ohlcv(symbol, timeframe=TIMEFRAME, limit=LIMIT)
        if not ohlcv or len(ohlcv) < 30:
            return "⚠️ داده‌های کندل کافی برای تحلیل تکنیکال در دسترس نیست."

        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        
        # محاسبه اندیکاتورها با pandas-ta
        df['RSI'] = df.ta.rsi(length=14)
        df['EMA20'] = df.ta.ema(length=20)
        df['EMA50'] = df.ta.ema(length=50)
        macd = df.ta.macd(fast=12, slow=26, signal=9)
        
        last_row = df.iloc[-1]
        last_macd = macd.iloc[-1]

        rsi_val = last_row['RSI']
        close_price = last_row['close']
        ema20 = last_row['EMA20']
        ema50 = last_row['EMA50']
        macd_val = last_macd['MACD_12_26_9']
        macd_signal = last_macd['MACDs_12_26_9']

        # سیگنال ساده تحلیلی
        if rsi_val < 30 and ema20 > ema50:
            trend = "🟢 سیگنال بالقوه خرید (اشباع فروش + روند صعودی کوتاه)"
        elif rsi_val > 70 and ema20 < ema50:
            trend = "🔴 سیگنال بالقوه فروش (اشباع خرید + روند نزولی کوتاه)"
        elif ema20 > ema50:
            trend = "📈 روند کلی صعودی (EMA20 > EMA50)"
        else:
            trend = "📉 روند کلی نزولی یا خنثی"

        report = (
            f"📊 **تحلیل تکنیکال {symbol}** (تایم‌فریم: {TIMEFRAME})\n"
            f"──────────────────\n"
            f"💵 **قیمت فعلی:** `{close_price:,.4f}` USDT\n"
            f"📉 **شاخص RSI (14):** `{rsi_val:.2f}`\n"
            f"📊 **میانگین EMA 20:** `{ema20:,.4f}`\n"
            f"📊 **میانگین EMA 50:** `{ema50:,.4f}`\n"
            f"⚡️ **وضعیت MACD:** `{'صعودی' if macd_val > macd_signal else 'نزولی'}`\n"
            f"──────────────────\n"
            f"🧭 **جمع‌بندی اندیکاتورها:**\n{trend}"
        )
        return report

    except Exception as e:
        logger.error(f"Error in analysis for {symbol}: {e}")
        return f"❌ خطا در دریافت اطلاعات یا تحلیل: {e}"


# --- هندلرهای تلگرام ---

@dp.message(CommandStart())
async def cmd_start(message: Message):
    """پیام خوش‌آمدگویی و منوی اصلی"""
    text = (
        f"سلام {message.from_user.first_name} عزیز! 🤖\n\n"
        "به ربات دستیار تحلیل و ترید خوش آمدید.\n"
        "از منوی زیر می‌توانید جفت‌ارزها را مشاهده و تحلیل تکنیکال آن‌ها را دریافت کنید."
    )
    await message.answer(text, reply_markup=get_main_menu())


@dp.message(F.text == "📊 لیست و تحلیل ارزها")
async def show_pairs_list(message: Message):
    """نمایش صفحه اول جفت‌ارزها"""
    await message.answer(
        "لطفاً یک جفت‌ارز را برای مشاهده قیمت یا تحلیل انتخاب کنید:",
        reply_markup=get_pairs_keyboard(page=0)
    )


@dp.message(F.text == "ℹ️ راهنما")
async def show_help(message: Message):
    help_text = (
        "💡 **راهنمای ربات:**\n\n"
        "۱. دکمه «لیست و تحلیل ارزها» را بزنید.\n"
        "۲. با دکمه‌های «قبلی / بعدی» بین ۱۰۰ جفت‌ارز جابجا شوید.\n"
        "۳. روی جفت‌ارز دلخواه کلیک کرده و گزینه تحلیل یا قیمت را بزنید."
    )
    await message.answer(help_text)


@dp.message(F.text == "💼 موجودی کیف‌پول")
async def show_balance(message: Message):
    """نمایش موجودی صرافی (در صورت داشتن API Key)"""
    if not EXCHANGE_API_KEY:
        await message.answer("⚠️ کلید صرافی (API Key) در فایل .env تعریف نشده است.")
        return
    try:
        balance = await exchange.fetch_balance()
        free_usdt = balance.get('free', {}).get('USDT', 0)
        await message.answer(f"💼 موجودی آزاد USDT شما:\n`{free_usdt:,.2f}` USDT")
    except Exception as e:
        await message.answer(f"❌ خطا در استعلام موجودی:\n{e}")


# --- هندلرهای دکمه‌های شیشه‌ای (Callback Queries) ---

@dp.callback_query(F.data.startswith("page:"))
async def handle_pagination(callback: CallbackQuery):
    """ورق زدن صفحات جفت‌ارزها"""
    page = int(callback.data.split(":")[1])
    await callback.message.edit_reply_markup(
        reply_markup=get_pairs_keyboard(page=page)
    )
    await callback.answer()


@dp.callback_query(F.data.startswith("select_pair:"))
async def handle_pair_selection(callback: CallbackQuery):
    """هنگام کلیک روی یک جفت‌ارز"""
    pair = callback.data.split(":")[1]
    await callback.message.edit_text(
        f"جفت‌ارز انتخابی: **{pair}**\nیکی از گزینه‌های زیر را انتخاب کنید:",
        reply_markup=get_pair_actions_keyboard(pair),
        parse_mode="Markdown"
    )
    await callback.answer()


@dp.callback_query(F.data.startswith("price:"))
async def handle_price_request(callback: CallbackQuery):
    """استعلام قیمت لحظه‌ای"""
    pair = callback.data.split(":")[1]
    await callback.answer("در حال دریافت قیمت...")
    
    price = await fetch_ticker_price(pair)
    if price:
        msg = f"💵 **قیمت لحظه‌ای {pair}:**\n`{price:,.4f}` USDT"
    else:
        msg = f"❌ دریافت قیمت برای {pair} با خطا مواجه شد."
        
    await callback.message.answer(msg, parse_mode="Markdown")


@dp.callback_query(F.data.startswith("analyze:"))
async def handle_analysis_request(callback: CallbackQuery):
    """اجرای تحلیل تکنیکال روی ارز انتخاب‌شده"""
    pair = callback.data.split(":")[1]
    await callback.answer("در حال محاسبه شاخص‌های تکنیکال...")
    
    report = await analyze_symbol(pair)
    await callback.message.answer(report, parse_mode="Markdown")


@dp.callback_query(F.data == "back_to_list")
async def handle_back_to_list(callback: CallbackQuery):
    """بازگشت به لیست جفت‌ارزها"""
    await callback.message.edit_text(
        "لطفاً یک جفت‌ارز را انتخاب کنید:",
        reply_markup=get_pairs_keyboard(page=0)
    )
    await callback.answer()


@dp.callback_query(F.data == "noop")
async def handle_noop(callback: CallbackQuery):
    """برای دکمه شماره صفحه که کاری انجام نمی‌دهد"""
    await callback.answer()


# --- تابع اجرای اصلی برنامه ---
async def main():
    logger.info("Bot is starting...")
    try:
        # حذف پیام‌های قبلی انباشته شده و اجرای Polling
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        # بستن ارتباط امن با صرافی و ربات
        await exchange.close()
        await bot.session.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped.")
