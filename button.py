from aiogram.types import KeyboardButton,ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

send_contact = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Kontakt yuboish ☎️", request_contact=True)]
    ],
    resize_keyboard=True,
)

location_contact = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📍 joylashuvni yuboish", request_location=True)]
    ],
    resize_keyboard=True,
)

# 1 - usul 
menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="💻 Laptop"),KeyboardButton(text="📱 Phones")],
        [KeyboardButton(text="💁🏻‍♂️ About us"),KeyboardButton(text="📍 Location")],
        [KeyboardButton(text="☎️ Contact admin")]
    ],
    resize_keyboard=True,
    input_field_placeholder="Tugmalardan birini tanlang ..."
)

# 2 - usul

computers = [
    "Mackbook",
    "Lenovo",
    "HP",
    "ASUS",
    "Victus",
    "ACER",
    "Samsung",
]

computer_button = ReplyKeyboardBuilder()

for computer in computers:
    computer_button.add(KeyboardButton(text=computer))

computer_button.add(KeyboardButton(text="Orqaga qaytish 🔙"))

computer_button.adjust(2,repeat=True)

computer_button = computer_button.as_markup(
    resize_keyboard=True,
    input_field_placeholder="Choise computer..."
)

# back = ReplyKeyboardMarkup(
#     keyboard=[
#         [KeyboardButton(text="Orqaga qaytish 🔙", request_location=True)]
#     ],
#     resize_keyboard=True,
# )

