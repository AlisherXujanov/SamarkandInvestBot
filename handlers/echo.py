from aiogram import Router
from aiogram.types import Message

router = Router()

@router.message()
async def echo_handler(message: Message):
    """Noma'lum yoki oddiy matnli xabarlarga aks-sado (echo) javob qaytarish"""
    await message.answer(f"Siz yubordingiz: {message.text}")
