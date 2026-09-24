# keyboards.py
from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from env import TRADING_PAIRS

# ۱. دکمه‌های رینگی (منوی پایین صفحه - Reply Keyboard)
def main_reply_keyboard() -> ReplyKeyboardMarkup:
    kb = [
        [KeyboardButton(text="📊 لیست ارزها و تحلیل"), KeyboardButton(text="⚡️ اسکن کلی بازار")],
        [KeyboardButton(text="⚙️ تنظیمات تایم‌فریم"), KeyboardButton(text="ℹ️ راهنما")]
    ]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)


# ۲. دکمه‌های شیشه‌ای برای لیست ۱۰۰ ارز به صورت صفحه‌بندی‌شده (Pagination)
def get_crypto_page_keyboard(page: int = 0, per_page: int = 10) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    start_idx = page * per_page
    end_idx = start_idx + per_page
    current_pairs = TRADING_PAIRS[start_idx:end_idx]
    
    # دکمه ارزها (۲ ارز در هر سطر)
    for pair in current_pairs:
        # نام تمیزتر برای نمایش (مثلاً BTC)
        coin_name = pair.split('/')[0]
        builder.button(text=f"📈 {coin_name}", callback_data=f"analyze_{pair}")
    
    builder.adjust(2)
    
    # دکمه‌های قبلی/بعدی برای تغییر صفحه
    nav_buttons = []
    if page > 0:
        nav_buttons.append(InlineKeyboardButton(text="◀️ صفحه قبل", callback_data=f"page_{page - 1}"))
    
    total_pages = (len(TRADING_PAIRS) + per_page - 1) // per_page
    nav_buttons.append(InlineKeyboardButton(text=f"{page + 1}/{total_pages}", callback_data="noop"))
    
    if end_idx < len(TRADING_PAIRS):
        nav_buttons.append(InlineKeyboardButton(text="صفحه بعد ▶️", callback_data=f"page_{page + 1}"))
    
    builder.row(*nav_buttons)
    return builder.as_markup()


# ۳. دکمه‌های شیشه‌ای برای انتخاب تایم‌فریم
def timeframe_inline_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    timeframes = ["15m", "1h", "4h", "1d"]
    for tf in timeframes:
        builder.button(text=f"⏱ {tf}", callback_data=f"set_tf_{tf}")
    builder.adjust(2)
    return builder.as_markup()
