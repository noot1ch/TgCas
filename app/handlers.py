from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import asyncio

from database.database import db, save_db
import app.keyboards as kb
from app.twisters import get_roller_multiplier, get_dice_multiplier

router = Router()

def log_message(message):
    print(f'[{message.from_user.username}]{message.text}')

    id = str(message.from_user.id)
    if id not in db:
        db[id] = {'balance': 0, 'username': message.from_user.username, 'bid': 10}
        save_db(db)


class user(StatesGroup):
    balance = State()
    bid = State()
    rolling = State()


@router.message(user.rolling)
async def anti_spam(message: Message, state: FSMContext):
    await message.answer('Пожалуйста, подождите')


@router.message(F.text == 'Назад')
@router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await state.clear()
    log_message(message)

    await message.answer('Привет! Ты попал в телеграм казино-бота', reply_markup=kb.main)


@router.message(F.text == 'Крутилки')
async def slots(message: Message, state: FSMContext):
    await state.clear()
    log_message(message)

    await message.answer(f'выбери крутилку (твоя текущая ставка {db[str(message.from_user.id)]['bid']})', reply_markup=kb.twisters)
    

@router.message(F.text == 'Профиль')
async def profile(message: Message, state: FSMContext):
    await state.clear()
    log_message(message)

    await message.answer(f'Профиль\nНик: {message.from_user.username}\nБаланс: {db[str(message.from_user.id)]['balance']}\n',
                         reply_markup=kb.profile)


@router.message(F.text == 'Крутилка 1')
async def roller(message: Message, state: FSMContext):
    log_message(message)

    if db[str(message.from_user.id)]['balance'] >= db[str(message.from_user.id)]['bid']:
        bid = db[str(message.from_user.id)]['bid']
        db[str(message.from_user.id)]['balance'] -= bid

        await state.set_state(user.rolling)
        dice_msg = await message.answer_dice(emoji='🎰')

        await asyncio.sleep(2)

        multiplier = get_roller_multiplier(dice_msg.dice.value)
        if multiplier:
            db[str(message.from_user.id)]['balance'] += int(bid * multiplier)
            await message.answer(f'Ура! Ты выйграл {int(bid * multiplier)} рублей, (множитель {multiplier}), ваш баланс теперь {db[str(message.from_user.id)]['balance']}')
        else:
            await message.answer('Ты проиграл(((')

        await state.clear()
    else:
        await message.answer('У вас не хватает баланса')
    save_db(db)


@router.message(F.text == 'Крутилка 2')
async def dice(message: Message, state: FSMContext):
    log_message(message)

    if db[str(message.from_user.id)]['balance'] >= db[str(message.from_user.id)]['bid']:
        bid = db[str(message.from_user.id)]['bid']
        db[str(message.from_user.id)]['balance'] -= bid

        await state.set_state(user.rolling)
        dice_msg = await message.answer_dice(emoji='🎲')
        
        
        await asyncio.sleep(2)
        await message.answer(str(dice_msg.dice.value))

        multiplier = get_dice_multiplier(dice_msg.dice.value)
        if multiplier:
            db[str(message.from_user.id)]['balance'] += int(bid * multiplier)
            await message.answer(f'Ура! Ты выйграл {int(bid * multiplier)} рублей, (множитель {multiplier}), ваш баланс теперь {db[str(message.from_user.id)]['balance']}')
        else:
            await message.answer('Ты проиграл(((')

        await state.clear()
    else:
        await message.answer('У вас не хватает баланса')
    save_db(db)


@router.message(F.text == 'Пополнить баланс')
async def balance1(message: Message, state: FSMContext):
    log_message(message)

    await state.set_state(user.balance)
    await message.answer(f'напишите сумму пополнения')


@router.message(user.balance)
async def balance2(message: Message, state: FSMContext):
    if message.text.isdigit():
        await message.answer(f'Отлично, ваш баланс был пополнен на {message.text} рублей', reply_markup=kb.main)
        db[str(message.from_user.id)]['balance'] += int(message.text)
        save_db(db)
        await state.clear()
    else:
        await message.answer(f'Ваш ответ должен состоять только из цифр', reply_markup=kb.main)


@router.message(F.text == 'Сменить ставку')
async def bid1(message: Message, state: FSMContext):
    log_message(message)

    await state.set_state(user.bid)
    await message.answer(f'напишите желаемую ставку')


@router.message(user.bid)
async def bid2(message: Message, state: FSMContext):
    if message.text.isdigit():
        await message.answer(f'Отлично, ваша ставка теперь {message.text} рублей', reply_markup=kb.twisters)
        db[str(message.from_user.id)]['bid'] = int(message.text)
        save_db(db)
        await state.clear()
    else:
        await message.answer(f'Ваш ответ должен состоять только из цифр', reply_markup=kb.twisters)


@router.message()
async def wrong_messages(message: Message):
    print(f'[{message.from_user.username}]{message.text}')