import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from states import Registor
from button import menu, computer_button, computers
from baza import computers_info

TOKEN = "..."
ADMIN_ID = [...]

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

# latitude bilan longitude olish kodi 
# @dp.message(F.location)
# async def location(message: Message):
#     lat = message.location.latitude
#     lon = message.location.longitude

#     text = f"latitude:<code>{lat}</code>\n"
#     text += f"longitude:<code>{lon}</code>"

#     await message.answer(text, parse_mode="html")

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

# @dp.message(Command("reg"))
# async def register(message: Message, state:FSMContext):
    # await message.answer("Ro'yxatdan o'tish uchun ma'limotlarni kiriting !  \nIsmingizni kiriting ")
    # await state.set_state(Registor.ism)

# First_name
@dp.message(F.text, Registor.ism)
async def register_ism(message: Message, state:FSMContext):
    photo = message.text
    await state.update_data(rasm = photo)
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
    # await message.answer("Telefon raqamni kiriting", reply_markup=)

# Phone_number  F.contact | F.text, SingUp.tel
@dp.message(F.contact | F.text, Registor.tel)
async def register_tel(message: Message, state:FSMContext):
    tel = message.text
    await state.update_data(tel = tel)
    await state.set_state(Registor.kurs)
    await message.answer("Kursni nomini kiriting")

@dp.message(Registor.tel)
async def register_tel_del(message:Message, state:FSMContext):
    await message.delete()
    await message.answer(text= "Telefon raqamni to'g'ri kiriting ❗️")

# end Phone_number

@dp.message(F.text, Registor.kurs)
async def register_kurs(message: Message, state:FSMContext):

    data = await state.get_data() 

    ism = data.get("name")
    familiya = data.get("surname")
    yosh = data.get("age")
    tel = data.get("tel")
    
    kurs = message.text

    text = f"Ism : {ism} \nFamiliya : {familiya} \nYosh : {yosh} \nTel : {tel} \nKurs : {kurs}"
    await message.answer("Siz ro'yxatdan o'tdingiz", reply_markup=menu)

    for admin in ADMIN_ID:
        await bot.send_message(chat_id= admin, text=text)
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
