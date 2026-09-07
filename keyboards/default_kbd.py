from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

def get_main_menu() -> ReplyKeyboardMarkup:
    """O'yinchoqlar do'koni asosiy menyusi"""
    builder = ReplyKeyboardBuilder()
    
    builder.button(text="🧸 O'yinchoqlar katalogi")
    builder.button(text="🛒 Savatcham va Chek")
    builder.button(text="ℹ️ Do'kon haqida")
    builder.button(text="📞 Aloqa & Manzil")
    
    builder.adjust(2, 2)
    return builder.as_markup(resize_keyboard=True)

def get_phone_keyboard() -> ReplyKeyboardMarkup:
    """Telefon raqamni yuborish tugmasi"""
    builder = ReplyKeyboardBuilder()
    builder.button(text="📱 Telefon raqamni yuborish", request_contact=True)
    builder.button(text="❌ Bekor qilish")
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)
