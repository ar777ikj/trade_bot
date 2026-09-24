import math
from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from config import TRADING_PAIRS

PAGE_SIZE = 10  # تعداد ارزها در هر صفحه


# ۱. منوی اصلی پایین صفحه (Reply Keyboard)
def get_main_menu() -> ReplyKeyboardMarkup:
    kb = [
        [KeyboardButton(text="📊 لیست و تحلیل ارزها")],
        [KeyboardButton(text="💼 موجودی کیف‌پول"), KeyboardButton(text="ℹ️ راهنما")]
    ]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)


# ۲. کیبورد اینلاین جفت‌ارزها با قابلیت صفحه‌بندی (Pagination)
def get_pairs_keyboard(page: int = 0) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    total_pairs = len(TRADING_PAIRS)
    total_pages = math.ceil(total_pairs / PAGE_SIZE)

    # اطمینان از قرار گرفتن شماره صفحه در محدوده مجاز
    page = max(0, min(page, total_pages - 1))

    # برش دادن ۱۰ ارز برای صفحه فعلی
    start_idx = page * PAGE_SIZE
    end_idx = start_idx + PAGE_SIZE
    current_pairs = TRADING_PAIRS[start_idx:end_idx]

    # افزودن دکمه‌های ارزها (در سطرهای ۲تایی)
    for pair in current_pairs:
        # callback_data را طوری می‌گذاریم که در bot.py بفهمیم کدام ارز کلیک شده
        builder.button(
            text=pair,
            callback_data=f"select_pair:{pair}"
        )
    builder.adjust(2)  # چینش دکمه‌های ارزها در ۲ ستون

    # دکمه‌های ناوبری (قبلی / بعدی / شماره صفحه)
    nav_buttons = []
    
    # دکمه صفحه قبل
    if page > 0:
        nav_buttons.append(
            InlineKeyboardButton(text="⬅️ قبلی", callback_data=f"page:{page - 1}")
        )
    else:
        nav_buttons.append(
            InlineKeyboardButton(text="⏹", callback_data="noop")
        )

    # نمایشگر صفحه فعلی
    nav_buttons.append(
        InlineKeyboardButton(text=f"📄 {page + 1}/{total_pages}", callback_data="noop")
    )

    # دکمه صفحه بعد
    if page < total_pages - 1:
        nav_buttons.append(
            InlineKeyboardButton(text="بعدی ➡️", callback_data=f"page:{page + 1}")
        )
    else:
        nav_buttons.append(
            InlineKeyboardButton(text="⏹", callback_data="noop")
        )

    # افزودن ردیف دکمه‌های ناوبری به انتهای کیبورد
    builder.row(*nav_buttons)

    return builder.as_markup()


# ۳. کیبورد انتخاب عملیات برای ارز انتخاب‌شده (تحلیل، خرید، فروش)
def get_pair_actions_keyboard(pair: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="📈 تحلیل تکنیکال (RSI/MACD)", callback_data=f"analyze:{pair}")
    builder.button(text="💵 استعلام قیمت لحظه‌ای", callback_data=f"price:{pair}")
    builder.button(text="🔙 بازگشت به لیست", callback_data="back_to_list")
    builder.adjust(1)
    return builder.as_markup()
