from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


# Функция для формирования инлайн-клавиатуры на лету
def create_kb(width: int,
                     *args: str,
                     **kwargs: str) -> InlineKeyboardMarkup:
    # Инициализируем билдер
    kb_builder = InlineKeyboardBuilder()
    # Инициализируем список для кнопок
    buttons: list[InlineKeyboardButton] = []

    # Заполняем список кнопками из аргументов args и kwargs
    if args:
        pass
    if kwargs:
        for button, text in kwargs.items():
            buttons.append(InlineKeyboardButton(
                text=text,
                callback_data=button))

    # Распаковываем список с кнопками в билдер методом row c параметром width
    kb_builder.row(*buttons, width=width)

    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup()


back = InlineKeyboardButton(text="В главное меню 🔙", callback_data="to_main")
contact = InlineKeyboardButton(text="Написать разработчику 📟", url="https://t.me/alekseinushtaev")

contact_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [contact],
        [back]
    ]
)



