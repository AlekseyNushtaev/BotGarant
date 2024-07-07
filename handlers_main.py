from aiogram import Router, F
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State, default_state
from aiogram.types import Message, CallbackQuery, FSInputFile
from docxtpl import DocxTemplate

from bot import bot
from config import ADMIN_IDS
from keyboard_creator import create_kb


router = Router()


class FSMFillForm(StatesGroup):
    fill_quest = State()
    fill_product = State()
    fill_number = State()
    fill_zakaz = State()
    fill_fio = State()
    fill_phone = State()
    fill_email = State()
    change = State()
    fill_id = State()
    fill_ans = State()

@router.message(CommandStart(), StateFilter(default_state))
async def process_start(msg: Message):
    await msg.answer_photo(
        photo="AgACAgIAAxkBAAMJZnpRPdVAQ-hkT0qHh5278vxn0BwAAnvYMRux7dBLxdHZbINnCHYBAAMCAANzAAM1BA",
        caption='Добро пожаловать в магазин Shikimori 😽',
        reply_markup=create_kb(1,
                               ticket="Получить гарантийный талон 📄",
                               quest="Обратиться в службу поддержки ⁉️"))


@router.callback_query(F.data == "quest", StateFilter(default_state))
async def process_quest(cb: CallbackQuery, state: FSMContext):
    await bot.send_message(cb.from_user.id, text="Напишите пожалуйста свой вопрос службе поддержки.")
    await state.set_state(FSMFillForm.fill_quest)


@router.message(StateFilter(FSMFillForm.fill_quest))
async def process_quest_forward(msg: Message, state: FSMContext):
    for admin_id in ADMIN_IDS:
        try:
            await bot.forward_message(chat_id=admin_id, from_chat_id=msg.chat.id, message_id=msg.message_id)
            await bot.send_message(chat_id=admin_id,
                                   text=f'username - {msg.from_user.username}\n'
                                        f'id -       {msg.from_user.id}',
                                   reply_markup=create_kb(1,
                                                          ans="Написать ответ через бота"))
        except Exception:
            pass
    await msg.answer(text='Ваш вопрос принят. В скором времени мы с удовольствием ответим на него, согласно нашему рабочему графику. Спасибо за обращение!',
                     reply_markup=create_kb(1,
                                            ticket="Получить гарантийный талон 📄",
                                            quest="Обратиться в службу поддержки ⁉️"))
    await state.set_state(default_state)


@router.callback_query(F.data == "ans", StateFilter(default_state))
async def process_id(cb: CallbackQuery, state: FSMContext):
    await bot.send_message(cb.from_user.id, text="Введите id юзера")
    await state.set_state(FSMFillForm.fill_id)


@router.message(StateFilter(FSMFillForm.fill_id))
async def process_ans(msg: Message, state: FSMContext):
    await state.update_data(user_id=msg.text)
    await msg.answer(text="Введите сообщение для юзера")
    await state.set_state(FSMFillForm.fill_ans)


@router.message(StateFilter(FSMFillForm.fill_ans))
async def process_send_ans(msg: Message, state: FSMContext):
    dct = await state.get_data()
    try:
        await bot.send_message(chat_id=dct['user_id'], text=msg.text)
        await msg.answer(text="Сообщение отправлено")
        await state.set_state(default_state)
    except Exception:
        await msg.answer(text="Что-то пошло не так")
        await state.set_state(default_state)


@router.callback_query(F.data == "ticket", StateFilter(default_state))
async def process_ticket(cb: CallbackQuery, state: FSMContext):
    await bot.send_message(chat_id=cb.from_user.id,
                           text="Выберите пожалуйста наименование Товара.",
                           reply_markup=create_kb(1,
                                                  p_1="GoPro hero 12",
                                                  p_2="Meta Quest 3 128GB",
                                                  p_3="Google Pixel 8A 128GB",
                                                  p_4="SSD Samsung 990 Pro 1TB",
                                                  p_5="SSD Samsung 990 Pro 2TB"))
    await state.set_state(FSMFillForm.fill_product)


@router.callback_query(F.data.in_({'p_1', 'p_2', 'p_3', 'p_4', 'p_5'}), StateFilter(FSMFillForm.fill_product))
async def process_product(cb: CallbackQuery, state: FSMContext):
    dct = {
        'p_1': "GoPro hero 12",
        'p_2': "Meta Quest 3 128GB",
        'p_3': "Google Pixel 8A 128GB",
        'p_4': "SSD Samsung 990 Pro 1TB",
        'p_5': "SSD Samsung 990 Pro 2TB"
    }
    await state.update_data(product=dct[cb.data])
    await bot.send_message(chat_id=cb.from_user.id,
                           text="Введите пожалуйста серийный номер товара.")

    await state.set_state(FSMFillForm.fill_number)


@router.message(StateFilter(FSMFillForm.fill_number))
async def process_number(msg: Message, state: FSMContext):
    await state.update_data(number=msg.text)
    await msg.answer(text="Введите пожалуйста номер заказа на Ozon/WB/Yandex/Sber.")

    await state.set_state(FSMFillForm.fill_zakaz)


@router.message(StateFilter(FSMFillForm.fill_zakaz))
async def process_zakaz(msg: Message, state: FSMContext):
    await state.update_data(zakaz=msg.text)
    await msg.answer(text="Введите пожалуйста Ваше ФИО.",
                     reply_markup=create_kb(1,
                                            no_fio='Не предоставлять данные'))

    await state.set_state(FSMFillForm.fill_fio)


@router.message(StateFilter(FSMFillForm.fill_fio))
async def process_fio(msg: Message, state: FSMContext):
    await state.update_data(fio=msg.text)
    await msg.answer(text="Введите пожалуйста Ваш контактный номер телефона.")

    await state.set_state(FSMFillForm.fill_phone)


@router.callback_query(F.data == 'no_fio', StateFilter(FSMFillForm.fill_fio))
async def process_no_fio(cb: CallbackQuery, state: FSMContext):
    await state.update_data(fio="Частное лицо")
    await bot.send_message(chat_id=cb.from_user.id,
                           text="Введите пожалуйста Ваш контактный номер телефона.")

    await state.set_state(FSMFillForm.fill_phone)


@router.message(StateFilter(FSMFillForm.fill_phone))
async def process_phone(msg: Message, state: FSMContext):
    await state.update_data(phone=msg.text)
    await msg.answer(text="На какой эл. адрес отправить гарантийник?")

    await state.set_state(FSMFillForm.fill_email)


@router.message(StateFilter(FSMFillForm.fill_email))
async def process_doc(msg: Message, state: FSMContext):
    await state.update_data(email=msg.text)
    dct = await state.get_data()
    doc = DocxTemplate("temp.docx")
    context = {'product': dct['product'],
               'number': dct['number'],
               'zakaz': dct['zakaz'],
               'fio': dct['fio'],
               'phone': dct['phone'],
               'email': dct['email']}
    doc.render(context)
    doc.save(f"Гарантийные обязательства-{msg.from_user.id}.docx")
    document = FSInputFile(f"Гарантийные обязательства-{msg.from_user.id}.docx")
    await msg.answer_document(document=document,
                              caption="Спасибо за регистрацию продукта, ознакомьтесь с содержимым, после прочтения нажмите кнопку Согласен и мы вам пришлем заполненый талон на вашу почту.",
                              reply_markup=create_kb(1,
                                                     yes="Согласен",
                                                     no="Не согласен"))
    await state.set_state(FSMFillForm.change)


@router.callback_query(F.data.in_({'yes', 'no'}), StateFilter(FSMFillForm.change))
async def process_restart(cb: CallbackQuery, state: FSMContext):
    if cb.data == 'yes':
        await bot.send_message(chat_id=cb.from_user.id,
                         text='В ближайшее время мы направим на Вашу электронную почту гарантийное соглашение')
        for admin_id in ADMIN_IDS:
            try:
                await bot.send_document(admin_id, FSInputFile(f"Гарантийные обязательства-{cb.from_user.id}.docx"),
                                        caption=f"username - {cb.from_user.username}\n"
                                                f"user_id - {cb.from_user.id}")
            except Exception:
                pass
    await cb.bot.send_photo(
        chat_id=cb.from_user.id,
        photo="AgACAgIAAxkBAAMJZnpRPdVAQ-hkT0qHh5278vxn0BwAAnvYMRux7dBLxdHZbINnCHYBAAMCAANzAAM1BA",
        caption='Добро пожаловать в магазин Shikimori 😽',
        reply_markup=create_kb(1,
                               ticket="Получить гарантийный талон 📄",
                               quest="Обратиться в службу поддержки ⁉️"))
    await state.set_state(default_state)

@router.message(F.from_user.id == 1012882762)
async def process_load_photo(mes: Message):
    print(mes.photo[0].file_id)
