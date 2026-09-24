# config.py
import os
from dotenv import load_dotenv

# خواندن فایل .env در صورت وجود
load_dotenv()

# config.py
# در صورتی که خودتان توکن برای تلگرام دارید در"" توکن خود را جلوی BOT_TOKEN بزارید
BOT_TOKEN = os.getenv("BOT_TOKEN")
# اینم مثل بالایی
EXCHANGE_API_KEY = os.getenv("EXCHANGE_API_KEY")
EXCHANGE_SECRET_KEY = os.getenv("EXCHANGE_SECRET_KEY")


TRADING_PAIRS = [
    "BTC/USDT", "ETH/USDT", "BNB/USDT", "SOL/USDT", "XRP/USDT",
    "DOGE/USDT", "ADA/USDT", "TRX/USDT", "AVAX/USDT", "LINK/USDT",
    "SUI/USDT", "SHIB/USDT", "DOT/USDT", "NEAR/USDT", "BCH/USDT",
    "LTC/USDT", "UNI/USDT", "PEPE/USDT", "APT/USDT", "ICP/USDT",
    "XLM/USDT", "FET/USDT", "TAO/USDT", "RENDER/USDT", "AAVE/USDT",
    "POL/USDT", "ETC/USDT", "KAS/USDT", "XMR/USDT", "FIL/USDT",
    "ARB/USDT", "OP/USDT", "HBAR/USDT", "VET/USDT", "ATOM/USDT",
    "INJ/USDT", "TIA/USDT", "RUNE/USDT", "GRT/USDT", "FTM/USDT",
    "THETA/USDT", "BONK/USDT", "FLOKI/USDT", "ALGO/USDT", "WIF/USDT",
    "SEI/USDT", "JUP/USDT", "STX/USDT", "FLOW/USDT", "BEAM/USDT",
    "GALA/USDT", "IMX/USDT", "SAND/USDT", "MANA/USDT", "CHZ/USDT",
    "EOS/USDT", "NEO/USDT", "IOTA/USDT", "EGLD/USDT", "AXS/USDT",
    "KAVA/USDT", "PENDLE/USDT", "CRV/USDT", "MKR/USDT", "SNX/USDT",
    "QNT/USDT", "LDO/USDT", "DYDX/USDT", "1INCH/USDT", "ENS/USDT",
    "PYTH/USDT", "ORDI/USDT", "WLD/USDT", "BLUR/USDT", "STRK/USDT",
    "NOT/USDT", "TON/USDT", "ENA/USDT", "ZRO/USDT", "ZK/USDT",
    "RON/USDT", "JASMY/USDT", "ONDO/USDT", "CORE/USDT", "BTT/USDT",
    "CFX/USDT", "KLAY/USDT", "ROSE/USDT", "ZIL/USDT", "ENJ/USDT",
    "MINA/USDT", "ANKR/USDT", "HOT/USDT", "GNO/USDT", "WOO/USDT",
    "APE/USDT", "GMT/USDT", "COMP/USDT", "LRC/USDT", "BAT/USDT"
]

# تایم‌فریم‌های مورد استفاده برای تحلیل تکنیکال
TIMEFRAME = "1h"

# تنظیمات دیگر (مثلاً تعداد کندل‌ها برای محاسبات)
LIMIT = 100
