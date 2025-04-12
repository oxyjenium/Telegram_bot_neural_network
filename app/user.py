from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
import app.keyboards as kb
from app.states import Chat, Image
from aiogram.fsm.context import FSMContext
from app.generators import gpt_text, gpt_image
from app.database.requests import set_user, get_user, calculate
from decimal import Decimal

user = Router()

@user.message(F.text == "Отмена")
@user.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await set_user(message.from_user.id)
    await message.answer('Добро пожаловать',
                         reply_markup=kb.main)
    await state.clear()
    
@user.message(F.text == 'Чат')
async def chatting(message: Message, state: FSMContext):
    user = await get_user(message.from_user.id)
    if Decimal(user.balance) > 0:
        await state.set_state(Chat.text)
        await message.answer("Введите ваш запрос", reply_markup=kb.cancel)
    else:
        await message.answer("Недостаточно средств на балансе")
    
@user.message(Chat.text)
async def chat_response(message: Message, state: FSMContext):
    await state.set_state(Chat.wait)
    user = await get_user(message.from_user.id)
    if Decimal(user.balance) > 0:
        response = await gpt_text(message.text, 'gpt-4o-mini')
        await calculate(message.from_user.id, response['usage'], 'gpt-4o')
        await message.answer(response['response'])
        await state.set_state(Chat.text)
    else:
        await message.answer("Недостаточно средств на балансе")

@user.message(Image.wait)
@user.message(Chat.wait)
async def chat_wait(message: Message, state: FSMContext):
    await message.answer("Ваше сообщение генерируется, подождите")
    

@user.message(F.text == 'Генерация картинок')
async def chatting(message: Message, state: FSMContext):
    user = await get_user(message.from_user.id)
    if Decimal(user.balance) > 0:
        await state.set_state(Image.text)
        await message.answer("Введите ваш запрос", reply_markup=kb.cancel)
    else:
        await message.answer("Недостаточно средств на балансе")
    
@user.message(Image.text)
async def chat_response(message: Message, state: FSMContext):
    await state.set_state(Image.wait)
    user = await get_user(message.from_user.id)
    if Decimal(user.balance) > 0:
        response = await gpt_image(message.text, 'dall-e-3')
        await calculate(message.from_user.id, response['usage'], 'dall-e-3')
        await message.photo(photo=response['response'])
        await state.set_state(Image.text)
    else:
        await message.answer("Недостаточно средств на балансе")
    
    
    
    
    