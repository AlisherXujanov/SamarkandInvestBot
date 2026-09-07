from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from data.products import (
    get_all_products, get_product_by_id, add_to_cart, 
    remove_from_cart, clear_cart, get_cart_details
)
from keyboards.default_kbd import get_main_menu, get_phone_keyboard
from keyboards.inline_kbd import (
    get_catalog_keyboard, get_product_detail_keyboard, get_cart_keyboard
)

router = Router()

class CheckoutState(StatesGroup):
    waiting_for_phone = State()
    waiting_for_address = State()

# --- KATALOG VA MAHSULOTLAR ---

@router.message(F.text == "🧸 O'yinchoqlar katalogi")
async def show_catalog(message: Message):
    text = (
        "<b>🧸 Bolalar o'yinchoqlari katalogi</b>\n\n"
        "Quyida do'konimizdagi 10 xil qiziqarli o'yinchoqlar ro'yxati keltirilgan. "
        "Batafsil ma'lumot olish va savatga qo'shish uchun o'yinchoqni tanlang:"
    )
    await message.answer(text, parse_mode="HTML", reply_markup=get_catalog_keyboard())

@router.callback_query(F.data == "open_catalog")
async def process_open_catalog(callback: CallbackQuery):
    text = (
        "<b>🧸 Bolalar o'yinchoqlari katalogi</b>\n\n"
        "Batafsil ma'lumot olish va savatga qo'shish uchun o'yinchoqni tanlang:"
    )
    await callback.message.edit_text(text, parse_mode="HTML", reply_markup=get_catalog_keyboard())
    await callback.answer()

@router.callback_query(F.data.startswith("prod_"))
async def process_product_detail(callback: CallbackQuery):
    prod_id = int(callback.data.split("_")[1])
    product = get_product_by_id(prod_id)
    
    if not product:
        await callback.answer("Mahsulot topilmadi!", show_alert=True)
        return
        
    formatted_price = f"{product['price']:,}".replace(',', ' ')
    text = (
        f"<b>{product['name']}</b>\n\n"
        f"🏷 <b>Toifa:</b> {product['category']}\n"
        f"💵 <b>Narxi:</b> {formatted_price} so'm\n\n"
        f"📝 <b>Tavsif:</b> {product['description']}"
    )
    await callback.message.edit_text(text, parse_mode="HTML", reply_markup=get_product_detail_keyboard(prod_id))
    await callback.answer()

# --- SAVATCHA VA CHECKLIST ---

@router.callback_query(F.data.startswith("add_"))
async def process_add_to_cart(callback: CallbackQuery):
    prod_id = int(callback.data.split("_")[1])
    product = get_product_by_id(prod_id)
    
    if product:
        add_to_cart(callback.from_user.id, prod_id)
        await callback.answer(f"✅ '{product['name']}' savatga qo'shildi!", show_alert=True)
    else:
        await callback.answer("Xatolik yuz berdi!", show_alert=True)

@router.message(F.text == "🛒 Savatcham va Chek")
async def show_cart_message(message: Message):
    await render_cart(message.from_user.id, message.answer)

@router.callback_query(F.data == "open_cart")
async def show_cart_callback(callback: CallbackQuery):
    await render_cart(callback.from_user.id, callback.message.edit_text)
    await callback.answer()

async def render_cart(user_id: int, send_func):
    """Savatcha va Checklist ko'rinishini shakllantiruvchi yordamchi funksiya"""
    cart_details = get_cart_details(user_id)
    items = cart_details["items"]
    
    if not items:
        text = (
            "🛒 <b>Sizning savatchangiz bo'sh!</b>\n\n"
            "Katalog bo'limiga o'tib, yoqtirgan o'yinchoqlaringizni qo'shishingiz mumkin."
        )
        await send_func(text, parse_mode="HTML", reply_markup=get_catalog_keyboard())
        return

    # CHECKLIST tayyorlash
    checklist_text = "📋 <b>BUYURTMA CHECKLIST SAHIFASI</b>\n"
    checklist_text += "━━━━━━━━━━━━━━━━━━━━━\n\n"
    
    for idx, item in enumerate(items, 1):
        p = item["product"]
        price_fmt = f"{p['price']:,}".replace(',', ' ')
        total_fmt = f"{item['item_total']:,}".replace(',', ' ')
        checklist_text += (
            f"<b>{idx}. {p['name']}</b>\n"
            f"   └ {item['quantity']} dona x {price_fmt} so'm = <b>{total_fmt} so'm</b>\n\n"
        )
    
    total_price_fmt = f"{cart_details['total_price']:,}".replace(',', ' ')
    checklist_text += "━━━━━━━━━━━━━━━━━━━━━\n"
    checklist_text += f"📊 <b>Jami mahsulotlar:</b> {cart_details['total_count']} dona\n"
    checklist_text += f"💰 <b>JAMI TO'LOV SUMMASI:</b> <u>{total_price_fmt} so'm</u>\n\n"
    checklist_text += "<i>Mahsulot sonini o'zgartirish uchun pastdagi ➕ va ➖ tugmalaridan foydalaning.</i>"

    await send_func(checklist_text, parse_mode="HTML", reply_markup=get_cart_keyboard(cart_details))

@router.callback_query(F.data.startswith("inc_"))
async def process_increment(callback: CallbackQuery):
    prod_id = int(callback.data.split("_")[1])
    add_to_cart(callback.from_user.id, prod_id, 1)
    await render_cart(callback.from_user.id, callback.message.edit_text)
    await callback.answer("Soni oshirildi ➕")

@router.callback_query(F.data.startswith("dec_"))
async def process_decrement(callback: CallbackQuery):
    prod_id = int(callback.data.split("_")[1])
    remove_from_cart(callback.from_user.id, prod_id)
    await render_cart(callback.from_user.id, callback.message.edit_text)
    await callback.answer("Soni kamaytirildi ➖")

@router.callback_query(F.data == "clear_cart")
async def process_clear_cart(callback: CallbackQuery):
    clear_cart(callback.from_user.id)
    text = "🗑 <b>Savatchangiz tozalandi!</b>"
    await callback.message.edit_text(text, parse_mode="HTML", reply_markup=get_catalog_keyboard())
    await callback.answer("Savat tozalandi")

# --- CHECKOUT / BUYURTMA RASMIYLASHTIRISH ---

@router.callback_query(F.data == "checkout")
async def start_checkout(callback: CallbackQuery, state: FSMContext):
    cart_details = get_cart_details(callback.from_user.id)
    if not cart_details["items"]:
        await callback.answer("Savatchangiz bo'sh!", show_alert=True)
        return
        
    await state.set_state(CheckoutState.waiting_for_phone)
    text = (
        "<b>📦 Buyurtmani rasmiylashtirish:</b>\n\n"
        "Kuryer siz bilan bog'lanishi uchun telefon raqamingizni yuboring "
        "yoki pastdagi <b>'📱 Telefon raqamni yuborish'</b> tugmasini bosing:"
    )
    await callback.message.delete()
    await callback.message.answer(text, parse_mode="HTML", reply_markup=get_phone_keyboard())
    await callback.answer()

@router.message(F.text == "❌ Bekor qilish")
async def cancel_checkout(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Buyurtma bekor qilindi.", reply_markup=get_main_menu())

@router.message(CheckoutState.waiting_for_phone)
async def process_phone(message: Message, state: FSMContext):
    phone = message.contact.phone_number if message.contact else message.text
    await state.update_data(phone=phone)
    await state.set_state(CheckoutState.waiting_for_address)
    
    await message.answer(
        "📍 Rahmat! Endi yetkazib berish manzilini va mo'ljalni kiriting:",
        reply_markup=get_main_menu()
    )

@router.message(CheckoutState.waiting_for_address)
async def process_address(message: Message, state: FSMContext):
    user_data = await state.get_data()
    phone = user_data.get("phone")
    address = message.text
    
    cart_details = get_cart_details(message.from_user.id)
    
    # Buyurtma chekini shakllantirish
    order_receipt = "✅ <b>BUYURTMANINGIZ QABUL QILINDI!</b> 🎉\n"
    order_receipt += "━━━━━━━━━━━━━━━━━━━━━\n\n"
    order_receipt += f"👤 <b>Mijoz:</b> {message.from_user.full_name}\n"
    order_receipt += f"📞 <b>Telefon:</b> {phone}\n"
    order_receipt += f"📍 <b>Manzil:</b> {address}\n\n"
    order_receipt += "🧾 <b>Xarid cheki (Checklist):</b>\n"
    
    for idx, item in enumerate(cart_details["items"], 1):
        p = item["product"]
        total_fmt = f"{item['item_total']:,}".replace(',', ' ')
        order_receipt += f"  {idx}. {p['name']} ({item['quantity']} dona) = {total_fmt} so'm\n"
        
    total_price_fmt = f"{cart_details['total_price']:,}".replace(',', ' ')
    order_receipt += "━━━━━━━━━━━━━━━━━━━━━\n"
    order_receipt += f"💵 <b>JAMI TO'LOV SUMMASI:</b> <u>{total_price_fmt} so'm</u>\n\n"
    order_receipt += "🚚 Tezarada kuryerimiz siz bilan bog'lanadi va buyurtmangizni yetkazib beradi!"

    # Savatni tozalash va holatni yakunlash
    clear_cart(message.from_user.id)
    await state.clear()
    
    await message.answer(order_receipt, parse_mode="HTML", reply_markup=get_main_menu())
