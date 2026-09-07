# 10 ta bolalar o'yinchog'i ma'lumotlar bazasi
PRODUCTS = [
    {
        "id": 1,
        "name": "🚗 Masofadan boshqariladigan poyga mashinasi",
        "category": "Mashinalar",
        "price": 180000,
        "description": "Yuqori tezlikda harakatlanuvchi, akkumulyatorli va masofadan boshqarish pulti bor poyga mashinasi."
    },
    {
        "id": 2,
        "name": "🧸 Yumshoq ayiqcha (Teddy Bear)",
        "category": "Yumshoq o'yinchoqlar",
        "price": 120000,
        "description": "Juda yumshoq, gipoallergik materialdan tayyorlangan 50 sm li ayiqcha."
    },
    {
        "id": 3,
        "name": "🧱 Lego konstruktor 'Koinot kemasi'",
        "category": "Konstruktorlar",
        "price": 250000,
        "description": "350 qismdan iborat koinot kemasini yig'ish to'plami. Mantiqiy fikrlashni rivojlantiradi."
    },
    {
        "id": 4,
        "name": "🤖 Transformator Robot",
        "category": "Robotlar",
        "price": 150000,
        "description": "Mashinaga va robotga aylanadigan chiroqli hamda tovush chiqaruvchi robot."
    },
    {
        "id": 5,
        "name": "🚁 Interaktiv masofaviy vertolyot",
        "category": "Uchar o'yinchoqlar",
        "price": 210000,
        "description": "Bino ichida va tashqarisida uchirish uchun gilroskopli yengil vertolyot."
    },
    {
        "id": 6,
        "name": "🎨 Bolalar ijodiy rasm chizish to'plami",
        "category": "Rivojlantiruvchi",
        "price": 85000,
        "description": "150 qismli jamlanma: flomasterlar, akvarel bo'yoqlar, qalamlar va chizg'ichlar."
    },
    {
        "id": 7,
        "name": "🧩 500 qismli mantiqiy Pazl",
        "category": "Rivojlantiruvchi",
        "price": 65000,
        "description": "Yorqin rangli hayvonot olami tasvirlangan katta yoshdagi bolalar uchun pazl."
    },
    {
        "id": 8,
        "name": "🏎️ Metall mashinchalar to'plami (5 dona)",
        "category": "Mashinalar",
        "price": 140000,
        "description": "Mustahkam metall korpusli 5 xil poyga va kolleksiya mashinalari."
    },
    {
        "id": 9,
        "name": "🪆 Yog'och Matryoshka to'plami",
        "category": "Yog'och o'yinchoqlar",
        "price": 95000,
        "description": "Ekologik toza yog'ochdan yasalgan, qo'lda bo'yalgan 5 talik matryoshka."
    },
    {
        "id": 10,
        "name": "⚽ Interaktiv chiroqli futbol to'pi",
        "category": "Sport o'yinchoqlari",
        "price": 110000,
        "description": "Ichida LED chiroqlari bo meva beradigan, havo yostig'ida harakatlanadigan xona to'pi."
    }
]

# Foydalanuvchilar savatchalari (Xotirada saqlash): {user_id: {product_id: count}}
USER_CARTS = {}

def get_all_products():
    return PRODUCTS

def get_product_by_id(product_id: int):
    for p in PRODUCTS:
        if p["id"] == product_id:
            return p
    return None

def add_to_cart(user_id: int, product_id: int, quantity: int = 1):
    if user_id not in USER_CARTS:
        USER_CARTS[user_id] = {}
    
    current_count = USER_CARTS[user_id].get(product_id, 0)
    USER_CARTS[user_id][product_id] = current_count + quantity

def remove_from_cart(user_id: int, product_id: int):
    if user_id in USER_CARTS and product_id in USER_CARTS[user_id]:
        if USER_CARTS[user_id][product_id] > 1:
            USER_CARTS[user_id][product_id] -= 1
        else:
            del USER_CARTS[user_id][product_id]

def clear_cart(user_id: int):
    if user_id in USER_CARTS:
        USER_CARTS[user_id] = {}

def get_cart_details(user_id: int):
    """
    Foydalanuvchi savatchasini va checklist ma'lumotlarini hisoblab beradi
    """
    cart = USER_CARTS.get(user_id, {})
    items = []
    total_price = 0
    total_count = 0

    for prod_id, qty in cart.items():
        prod = get_product_by_id(prod_id)
        if prod:
            item_total = prod["price"] * qty
            total_price += item_total
            total_count += qty
            items.append({
                "product": prod,
                "quantity": qty,
                "item_total": item_total
            })

    return {
        "items": items,
        "total_price": total_price,
        "total_count": total_count
    }
