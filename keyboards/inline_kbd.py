from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from data.products import PRODUCTS

def get_catalog_keyboard() -> InlineKeyboardMarkup:
    """10 ta o'yinchoq katalogi Inline tugmalari"""
    builder = InlineKeyboardBuilder()
    
    for prod in PRODUCTS:
        # Narxini chiroyli formatlash (masalan 180 000 so'm)
        formatted_price = f"{prod['price']:,}".replace(',', ' ')
        btn_text = f"{prod['name']} - {formatted_price} so'm"
        builder.button(text=btn_text, callback_data=f"prod_{prod['id']}")
    
    builder.adjust(1) # Har bir qatorda 1 ta mahsulot
    return builder.as_markup()

def get_product_detail_keyboard(product_id: int) -> InlineKeyboardMarkup:
    """Alohida o'yinchoq sahifasi uchun tugmalar"""
    builder = InlineKeyboardBuilder()
    
    builder.button(text="➕ Savatga qo'shish", callback_data=f"add_{product_id}")
    builder.button(text="🛒 Savatchaga o'tish", callback_data="open_cart")
    builder.button(text="⬅️ Katalogga qaytish", callback_data="open_catalog")
    
    builder.adjust(1, 2)
    return builder.as_markup()

def get_cart_keyboard(cart_details: dict) -> InlineKeyboardMarkup:
    """Savatcha va Checklist sahifasi uchun tugmalar"""
    builder = InlineKeyboardBuilder()
    
    # Har bir mahsulot uchun + va - va o'chirish tugmalari
    for item in cart_details.get("items", []):
        p_id = item["product"]["id"]
        p_name = item["product"]["name"]
        
        builder.button(text=f"➖", callback_data=f"dec_{p_id}")
        builder.button(text=f"{p_name[:20]}.. ({item['quantity']})", callback_data=f"prod_{p_id}")
        builder.button(text=f"➕", callback_data=f"inc_{p_id}")

    if cart_details.get("items"):
        builder.button(text="✅ Buyurtmani rasmiylashtirish", callback_data="checkout")
        builder.button(text="🗑️ Savatni tozalash", callback_data="clear_cart")
    
    builder.button(text="🧸 Katalogga qaytish", callback_data="open_catalog")
    
    # Tugmalar joylashuvini moslash: har bir mahsulot uchun 3 ta tugma ( - | nomi | + )
    layout = [3] * len(cart_details.get("items", []))
    if cart_details.get("items"):
        layout.extend([1, 1]) # Checkout va Clear
    layout.append(1) # Back to catalog
    
    builder.adjust(*layout)
    return builder.as_markup()
