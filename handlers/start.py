from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from keyboards.default_kbd import get_main_menu

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    """/start buyrug'i uchun ishlov beruvchi"""
    user_name = message.from_user.full_name
    text = (
        f"🎈 <b>Xush kelibsiz, {user_name}!</b>\n\n"
        "Siz <b>'Ajoyib O'yinchoqlar'</b> bolalar do'konining Telegram botidasiz! 🧸✨\n\n"
        "Bu yerda siz farzandlaringiz uchun 10 xil sifatli va rivojlantiruvchi o'yinchoqlarni xarid qilishingiz mumkin.\n"
        "Boshlash uchun quyidagi <b>'🧸 O'yinchoqlar katalogi'</b> tugmasini bosing:"
    )
    await message.answer(text, parse_mode="HTML", reply_markup=get_main_menu())

@router.message(Command("help"))
async def cmd_help(message: Message):
    """/help buyrug'i uchun ishlov beruvchi"""
    text = (
        "<b>ℹ️ Yordam bo'limi:</b>\n\n"
        "• <b>/start</b> - Botni qayta ishga tushirish\n"
        "• <b>🧸 O'yinchoqlar katalogi</b> - Barcha o'yinchoqlar va ularning narxlari\n"
        "• <b>🛒 Savatcham va Chek</b> - Siz tanlagan mahsulotlar chek-listi va to'lov summasi\n"
        "• <b>📞 Aloqa</b> - Savollar bo'lsa biz bilan bog'lanish"
    )
    await message.answer(text, parse_mode="HTML")

@router.message(F.text == "ℹ️ Do'kon haqida")
async def about_us(message: Message):
    text = (
        "🎪 <b>'Ajoyib O'yinchoqlar' Do'koni Haqida:</b>\n\n"
        "Biz bolajonlar uchun xavfsiz, sifatli va mantiqiy fikrlashni rivojlantiruvchi o'yinchoqlarni taklif etamiz.\n"
        "• Top-10 o'yinchoqlar to'plami\n"
        "• Shahar bo'ylab tezkor yetkazib berish 🚚\n"
        "• Naqd va karta orqali to'lov imkoniyati 💳"
    )
    await message.answer(text, parse_mode="HTML")

@router.message(F.text == "📞 Aloqa & Manzil")
async def contact_us(message: Message):
    text = (
        "📞 <b>Biz bilan bog'lanish:</b>\n\n"
        "📱 <b>Telefon:</b> +998 (90) 123-45-67\n"
        "💬 <b>Telegram admin:</b> @ToyStoreAdmin\n"
        "📍 <b>Manzil:</b> Toshkent shahri, Chilonzor tumani, 5-mavze\n"
        "⏰ <b>Ish vaqti:</b> Har kuni 09:00 dan 20:00 gacha"
    )
    await message.answer(text, parse_mode="HTML")
