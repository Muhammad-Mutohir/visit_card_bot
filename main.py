
from PIL import Image, ImageDraw, ImageFont
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import InputFile
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

API_TOKEN = '8149180998:AAFX_WRrzwOpvEGOEyJoMzWGzHarj-P4mzs'
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class Form(StatesGroup):
    company_name = State()
    full_name = State()
    phone = State()
    address = State()
    email = State()



def overlay_text(image_path, company_name, full_name, phone, address, email):
    img = Image.open(image_path)
    draw = ImageDraw.Draw(img)
    try:
        font_large = ImageFont.truetype("arial.ttf", 40)
        font_medium = ImageFont.truetype("arial.ttf", 30)
        font_small = ImageFont.truetype("arial.ttf", 20)
    except IOError:
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
        font_small = ImageFont.load_default()

    company_position = (487, 425)
    full_name_position = (333, 610)
    phone_position = (370, 720)
    address_position = (370, 755)
    email_position = (370, 790)

    color = (1, 95, 20)

    # Draw text onto the image
    draw.text(company_position, company_name, fill=color, font=font_large)
    draw.text(full_name_position, full_name, fill=color, font=font_medium)
    draw.text(phone_position, "Phone: " + phone, fill=color, font=font_small)
    draw.text(address_position, "Address: " + address, fill=color, font=font_small)
    draw.text(email_position, "Email: " + email, fill=color, font=font_small)


    img.save('output_image_with_details.png')


@dp.message_handler(commands=['start'])
async def ask_for_company_name(message: types.Message):
    await message.answer("Please enter the company name:")
    await Form.company_name.set()



@dp.message_handler(state=Form.company_name)
async def get_company_name(message: types.Message, state: FSMContext):
    await state.update_data(company_name=message.text.upper())
    await message.answer("Enter your full name:")
    await Form.next()



async def get_full_name(message: types.Message, state: FSMContext):
    await state.update_data(full_name=message.text.title())
    await message.answer("Enter your phone number:")
    await Form.next()


@dp.message_handler(state=Form.phone)
async def get_phone_number(message: types.Message, state: FSMContext):
    await state.update_data(phone=message.text)
    await message.answer("Enter your address:")
    await Form.next()



@dp.message_handler(state=Form.address)
async def get_address(message: types.Message, state: FSMContext):
    await state.update_data(address=message.text.title())
    await message.answer("Enter your email address:")
    await Form.next()



@dp.message_handler(state=Form.email)
async def get_email(message: types.Message, state: FSMContext):
    await state.update_data(email=message.text)
    user_data = await state.get_data()
    await message.answer("thanks for your data wait your results")
    company_name = user_data['company_name']
    full_name = user_data['full_name']
    phone = user_data['phone']
    address = user_data['address']
    email = user_data['email']
    image_path = 'White And Green Minimalist Id Card Mockup Instagram Post.png'
    overlay_text(image_path, company_name, full_name, phone, address, email)
    print(f"{message.from_user.username}\n{company_name}\n{full_name}\n{address}\n{email}")
    with open('output_image_with_details.png', 'rb') as img:
        await bot.send_photo(message.chat.id, InputFile(img))
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
