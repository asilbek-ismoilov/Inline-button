import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from states import Registor
from button import menu, computer_button, computers, send_contact, location_button
from baza import computers_info, phone_info
from inline_button import menu_inline, phones_inf_mapping

TOKEN = ""
ADMIN_ID = []

dp = Dispatcher()

# start
@dp.message(CommandStart())
async def command_start_handler(message: Message, state:FSMContext):
    full_name = message.from_user.full_name
    text = f"Salom {full_name}, Shop bot \nRo'yxatdan o'tish uchun ma'limotlarni kiriting !  \nIsmingizni kiriting"
    await message.answer(text)
    await state.set_state(Registor.ism)
# endstart

# About
@dp.message(F.text=="💁🏻‍♂️ About us")
async def about_button(message: Message):
    text = "Biz sizga istalgan turdagi telefon yoki noutbuklarni sotib olishingizda yordam beramiz !"
    pic_url = "https://i.pinimg.com/originals/40/a9/c3/40a9c329dba2278c9775798067ebae2d.jpg"
    await message.answer_photo(pic_url, caption=text)
# endabout

# contact
@dp.message(F.text=="☎️ Contact admin")
async def about_button(message: Message):
    text = "Bot adminiga murojat qilish uchun: \nTel: +998 99 999 99 99"
    await message.answer(text)
# endcontact

@dp.message(F.text=="📍 Location")
async def location(message: Message):
    text = "Bizning savdo markazimizning kodi"
    lat = 40.102607
    lon = 65.37462
    await message.answer_location(lat, lon)
    await message.answer(text)

@dp.message(F.text=="💻 Laptop")
async def my_computers(message:Message):
    text = "Noutbuk turini tugmalardan tanlang !"
    await message.answer(text,reply_markup=computer_button)

@dp.message(F.text.func(lambda computer: computer in computers))
async def computer_info(message:Message):
    info = computers_info.get(message.text)

    photo = info.get("photo")
    price = info.get("price")
    color = info.get("color")

    text = f"{message.text}\nprice: ${price}\ncolor:{color}\n...."

    await message.answer_photo(photo=photo,caption=text)

# Ro'yxatdan o'tish kod

@dp.message(F.text=="📱 Phones")
async def phones(message:Message):
    text = "Telefon turini tugmalardan tanlang !"
    await message.answer(text,reply_markup=menu_inline)

@dp.callback_query(lambda callback: callback.data in phones_inf_mapping)
async def phones_info(callback: CallbackQuery):
    phone_key = phones_inf_mapping.get(callback.data)

    await callback.answer(phone_key)

    phone = phone_info.get(phone_key)
    photo = phone.get("photo")

    if phone:
        await callback.message.answer_photo(photo, caption=f"Telefon ma'lumotlari: {phone['color']}, Narxi: ${phone['price']}")
    else:
        await callback.message.answer("Telefon ma'lumotlari topilmadi.")



# First_name
@dp.message(F.text, Registor.ism)
async def register_ism(message: Message, state:FSMContext):
    name = message.text
    await state.update_data(name = name)
    await state.set_state(Registor.familiya)
    await message.answer("Familiyani kiriting")

# Agar kiritilgan qiymat text bo'lmasa ushbu kod ishga tushadi
@dp.message(Registor.ism)
async def register_ism_del(message:Message, state:FSMContext):
    await message.delete()
    await message.answer(text= "Ismimgizni to'g'ri kiriting ❗️")

# end First_name

@dp.message(F.text, Registor.familiya)
async def register_familiya(message: Message, state:FSMContext):
    familiya = message.text 
    await state.update_data(surname = familiya)
    await state.set_state(Registor.yosh)
    await message.answer("Yoshingizni kiriting")

@dp.message(F.text, Registor.yosh)
async def register_yosh(message: Message, state:FSMContext):
    yosh = message.text
    await state.update_data(age = yosh)
    await state.set_state(Registor.tel)
    await message.answer("Telefon raqamni kiriting", reply_markup=send_contact)

# Phone_number 
@dp.message(F.contact | F.text.regexp(r"^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$"), Registor.tel)
async def register_tel(message: Message, state:FSMContext):

    if message.contact:
        tel = message.contact.phone_number # +998978710140
    else:
        tel = message.text

    await state.update_data(tel = tel)
    await state.set_state(Registor.location)
    await message.answer("Locatsiyani kiriting", reply_markup=location_button)

@dp.message(Registor.tel)
async def register_tel_del(message:Message, state:FSMContext):
    await message.delete()
    await message.answer(text= "Telefon raqamni to'g'ri kiriting ❗️")

# end Phone_number

# location

@dp.message(F.location , Registor.location)
async def register_location(message: Message, state:FSMContext):
    
    lat = message.location.latitude
    lon = message.location.longitude

    await state.update_data(lat = lat)
    await state.update_data(lon = lon)
    await state.set_state(Registor.kurs)
    await message.answer("Kursni nomini kiriting")

# end location

@dp.message(F.text, Registor.kurs)
async def register_kurs(message: Message, state:FSMContext):

    data = await state.get_data() 

    ism = data.get("name")
    familiya = data.get("surname")
    yosh = data.get("age")
    lat = data.get("lat")
    lon = data.get("lon")
    tel = data.get("tel")
    
    kurs = message.text
    
    text = f"Ism : {ism} \nFamiliya : {familiya} \nYosh : {yosh} \nTel : {tel} \nKurs : {kurs}"
    await message.answer("Siz ro'yxatdan o'tdingiz", reply_markup=menu)

    for admin in ADMIN_ID:
        await bot.send_message(chat_id= admin, text=text)
        await bot.send_location(chat_id= admin, latitude = lat, longitude=lon)
    await state.clear()

@dp.message(F.text=="Orqaga qaytish 🔙")
async def back_button(message: Message):
    text = "Menu"
    await message.answer(text, reply_markup=menu)

# end Ro'yxatdan o'tish kod

@dp.startup()
async def bot_start():
    for admin in ADMIN_ID:
        await bot.send_message(admin, "Tabriklaymiz 🎉 \nBotimiz ishga tushdi ")

@dp.shutdown()
async def bot_start():
    for admin in ADMIN_ID:
        await bot.send_message(admin, "Bot to'xtadi ❗️")

    
async def main():
    global bot
    bot = Bot(TOKEN)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
