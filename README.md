# Aiogram 3 Telegram Bot loyihasi

Ushbu loyiha Python va **Aiogram 3** freymvorki yordamida modulli arxitektura asosida yaratilgan.

## 📁 Loyiha strukturasi

```
Tg-bot/
├── .env                  # Maxfiy kalitlar (Bot Token)
├── .gitignore            # Git uchun e'tiborga olinmaydigan fayllar
├── config.py             # Sozlamalarni yuklash
├── requirements.txt      # Kutubxonalar ro'yxati
├── main.py               # Asosiy ishga tushirish fayli
├── handlers/             # Buyruqlar va xabarlar ishlovchilari
│   ├── __init__.py
│   ├── start.py          # /start, /help va menyu tugmalari
│   └── echo.py           # Oddiy matnli xabarlar
└── keyboards/            # Bot tugmalari
    ├── __init__.py
    ├── default_kbd.py    # Reply menyu tugmalari
    └── inline_kbd.py     # Inline tugmalar va havolalar
```

## 🚀 Ishga tushirish yo'riqnomasi

### 1. Kutubxonalarni o'rnatish
Agarda o'rnatilmagan bo'lsa, quyidagi buyruqni bosing:
```bash
pip install -r requirements.txt
```

### 2. Botni ishga tushirish
```bash
python main.py
```

### 3. Botdan foydalanish
Telegram'da botingizga kirib `/start` buyrug'ini yuboring. Botingiz tayyor!
