from aiogram.dispatcher import Dispatcher, FSMContext, filters
from aiogram import types
from glas_osla.filters.is_client import ClientFilter
from glas_osla.keyboards.inline import keyboards
from glas_osla.db.db_commands import (
    get_expenses_category_name, new_expenses_category_name,
    delete_user_expenses_category, get_user_expenses_subcategories, new_expenses_sub_category_name,
    delete_user_expenses_sub_category, get_user_expenses_category_id_from_sub_category,
    get_expenses_sub_category_name, quick_add_to_expenses
)
from glas_osla.states.ExpensesStates import (
    ChangeExpensesCategoryStates,
    ChangeExpensesSubCategoryStates
)
from glas_osla.templates import general_phrases


async def add_to_history(message: types.Message):
    arguments = message.text.split()[1:]
    if not arguments:
        await message.answer('Введите аргументы')
        return
    params = {
        'user_id':  message.from_user.id,
        'amount':   arguments[0],
        'category': arguments[1],
    }
    try:
        params['sub_category'] = arguments[2]
        params['note'] = arguments[3]
    except IndexError:
        pass

    await quick_add_to_expenses(params)
    await message.answer(f'запись добавлена')


async def return_to_menu(callback: types.CallbackQuery):
    await callback.message.edit_text(general_phrases.menu_text, reply_markup=keyboards.menu_keyboard)


async def get_categories(callback: types.CallbackQuery):
    expenses_categories_keyboard = await keyboards.expenses_categories_keyboard(
        callback.from_user.id)
    await callback.message.edit_text('Ваши категории расходов:',
                                     reply_markup=expenses_categories_keyboard)


async def get_sub_categories(callback: types.CallbackQuery):
    print(callback.data)
    current_category_id = int(callback.data.split('_')[-1])
    current_category_name = await get_expenses_category_name(current_category_id)
    expenses_sub_categories_keyboard = await keyboards.expenses_subcategories_keyboard(
        callback.from_user.id,
        current_category_id)
    await callback.message.edit_text(f'Подкатегории у {current_category_name}',
                                     reply_markup=expenses_sub_categories_keyboard)


async def change_category(callback: types.CallbackQuery):
    current_category_id = int(callback.data.split('_')[-1])
    current_category_name = await get_expenses_category_name(current_category_id)
    change_or_delete_expenses_category_keyboard = await keyboards.change_or_delete_expenses_category(
        current_category_id)
    await callback.message.edit_text(f'Изменить или удалить {current_category_name}?',
                                     reply_markup=change_or_delete_expenses_category_keyboard)


async def edit_category(callback: types.CallbackQuery, state: FSMContext):
    current_category_id = int(callback.data.split('_')[-1])
    await ChangeExpensesCategoryStates.new_category_name.set()
    await state.update_data(current_category_id=current_category_id)
    await callback.message.edit_text('Введите новое название')


async def get_new_category_name(message: types.Message, state: FSMContext):
    new_name = message.text
    current_category_id = (await state.get_data())['current_category_id']
    await new_expenses_category_name(message.from_user.id, current_category_id, new_name)
    edit_category_keyboard = await keyboards.edit_expenses_category()
    await message.answer('OK', reply_markup=edit_category_keyboard)
    await state.finish()


async def delete_category(callback: types.CallbackQuery):
    current_category_id = int(callback.data.split('_')[-1])
    await delete_user_expenses_category(current_category_id)
    edit_category_keyboard = await keyboards.edit_expenses_category()
    await callback.message.answer("OK", reply_markup=edit_category_keyboard)


async def change_sub_category(callback: types.CallbackQuery):
    current_sub_category_id = int(callback.data.split('_')[-1])
    current_sub_category_name = await get_expenses_sub_category_name(current_sub_category_id)
    change_or_delete_expenses_sub_category_keyboard = await keyboards.change_or_delete_expenses_sub_category(
        current_sub_category_id)
    await callback.message.edit_text(f'Изменить или удалить {current_sub_category_name}?',
                                     reply_markup=change_or_delete_expenses_sub_category_keyboard)


async def edit_sub_category(callback: types.CallbackQuery, state: FSMContext):
    current_sub_category_id = int(callback.data.split('_')[-1])
    await ChangeExpensesSubCategoryStates.new_sub_category_name.set()
    await state.update_data(current_sub_category_id=current_sub_category_id)
    await callback.message.edit_text('Введите новое название')


async def get_new_sub_category_name(message: types.Message, state: FSMContext):
    new_name = message.text
    current_sub_category_id = (await state.get_data())['current_sub_category_id']
    await new_expenses_sub_category_name(message.from_user.id, current_sub_category_id, new_name)
    edit_sub_category_keyboard = await keyboards.edit_expenses_sub_category()
    await message.answer('OK', reply_markup=edit_sub_category_keyboard)
    await state.finish()
    await message.delete()


async def delete_sub_category(callback: types.CallbackQuery):
    current_sub_category_id = int(callback.data.split('_')[-1])
    await delete_user_expenses_sub_category(current_sub_category_id)
    edit_sub_category_keyboard = await keyboards.edit_expenses_sub_category()
    await callback.message.answer("OK", reply_markup=edit_sub_category_keyboard)


async def return_from_editing_or_changing_category(callback: types.CallbackQuery):
    expenses_categories_keyboard = await keyboards.expenses_categories_keyboard(
        callback.from_user.id)
    await callback.message.edit_text('Ваши категории расходов:',
                                     reply_markup=expenses_categories_keyboard)


async def return_from_changing_sub_category(callback: types.CallbackQuery):
    current_sub_category_id = int(callback.data.split('_')[-1])
    current_category_id = await get_user_expenses_category_id_from_sub_category(
        current_sub_category_id)
    current_category_name = await get_expenses_category_name(current_category_id)
    expenses_sub_categories_keyboard = await keyboards.expenses_subcategories_keyboard(
        callback.from_user.id,
        current_category_id)
    await callback.message.edit_text(f'Подкатегории у {current_category_name}',
                                     reply_markup=expenses_sub_categories_keyboard)


def setup_expenses_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(return_to_menu, ClientFilter(True), text='e_c_back_to_menu')
    dp.register_callback_query_handler(get_categories, ClientFilter(True), text='get_expenses')
    dp.register_callback_query_handler(get_sub_categories, ClientFilter(True),
                                       filters.Text(startswith='e_c_'))
    dp.register_callback_query_handler(change_category, ClientFilter(True),
                                       filters.Text(startswith='change_e_c_'))
    dp.register_callback_query_handler(edit_category, ClientFilter(True),
                                       filters.Text(startswith='edit_e_c_'))
    dp.register_message_handler(get_new_category_name, ClientFilter(True),
                                state=ChangeExpensesCategoryStates.new_category_name)
    dp.register_callback_query_handler(delete_category, ClientFilter(True),
                                       filters.Text(startswith='del_e_c_'))

    dp.register_callback_query_handler(change_sub_category, ClientFilter(True),
                                       filters.Text(startswith='e_s_c_'))
    dp.register_callback_query_handler(edit_sub_category, ClientFilter(True),
                                       filters.Text(startswith='edit_e_s_c_'))
    dp.register_message_handler(get_new_sub_category_name, ClientFilter(True),
                                state=ChangeExpensesSubCategoryStates.new_sub_category_name)
    dp.register_callback_query_handler(delete_sub_category, ClientFilter(True),
                                       filters.Text(startswith='del_e_s_c_'))

    dp.register_callback_query_handler(return_from_editing_or_changing_category, ClientFilter(True),
                                       text='back_to_categories')
    dp.register_callback_query_handler(return_from_changing_sub_category, ClientFilter(True),
                                       text='back_to_c_')
    dp.register_message_handler(add_to_history, ClientFilter(True), commands='-')
