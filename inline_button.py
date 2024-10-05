from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

phones_inf_mapping = {
    "apple_16_pro": "Apple 16 pro",
    "samsung_24_ultra": "Samsung 24 ultra",
    "redmi": "Redmi",
    "honor": "Honor"
}

menu_inline = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Apple 16 pro", callback_data="apple_16_pro"), 
            InlineKeyboardButton(text="Samsung 24 ultra", callback_data="samsung_24_ultra")
        ],
        [
            InlineKeyboardButton(text="Redmi", callback_data="redmi"), 
            InlineKeyboardButton(text="Honor", callback_data="honor")
        ]
    ]
)
