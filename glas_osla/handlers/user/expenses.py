from aiogram.dispatcher import Dispatcher, FSMContext, filters
from aiogram import types
from glas_osla.filters.is_client import ClientFilter
from glas_osla.keyboards.inline import (
    expenses_keyboards as ex_keyboards,
    general_keyboards as gen_keyboards
)
from glas_osla.db import db_commands
from glas_osla.db.models.expenses_plots_md import ExpenseCategory, ExpenseSubCategory
from glas_osla.states.ExpensesStates import (
    ChangeExpensesCategoryStates,
    ChangeExpensesSubCategoryStates,
    AddExpensesCategory, AddExpensesSubCategory
)
from glas_osla.db.db_commands import (
    get_category_name, new_category_name,
    delete_user_category, get_user_subcategories, new_sub_category_name,
    delete_user_sub_category, get_user_category_id_from_sub_category,
    get_sub_category_name, quick_add_to_expenses
)
from glas_osla.states.ExpensesStates import (
    ChangeExpensesCategoryStates,
    ChangeExpensesSubCategoryStates
)
from glas_osla.templates import general_phrases


async def add_to_history(message: types.Message):
    try:
        arguments = message.text.split()[1:]
        if len(arguments) > 4:
            raise IndexError
    except IndexError:
        await message.answer('Введены неверные аргументы\n/quick - информация о быстрой команде')
        return

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
    await callback.message.edit_text(general_phrases.menu_text,
                                     reply_markup=gen_keyboards.menu_keyboard)


async def get_categories(callback: types.CallbackQuery):
    expenses_categories_keyboard = await ex_keyboards.expenses_categories_keyboard(
        callback.from_user.id)
    await callback.message.edit_text('Ваши категории расходов:',
                                     reply_markup=expenses_categories_keyboard)


async def get_sub_categories(callback: types.CallbackQuery):
    current_category_id = int(callback.data.split('_')[-1])
    current_category_name = await db_commands.get_category_name(current_category_id, ExpenseCategory)
    expenses_sub_categories_keyboard = await ex_keyboards.expenses_subcategories_keyboard(
        callback.from_user.id,
        current_category_id)
    await callback.message.edit_text(f'Подкатегории у {current_category_name}',
                                     reply_markup=expenses_sub_categories_keyboard)


async def change_category(callback: types.CallbackQuery):
    current_category_id = int(callback.data.split('_')[-1])
    current_category_name = await db_commands.get_category_name(current_category_id, ExpenseCategory)
    change_or_delete_expenses_category_keyboard = await ex_keyboards.change_or_delete_expenses_category(
        current_category_id)
    await callback.message.edit_text(f'Изменить или удалить категорию {current_category_name}?',
                                     reply_markup=change_or_delete_expenses_category_keyboard)


async def edit_category(callback: types.CallbackQuery, state: FSMContext):
    current_category_id = int(callback.data.split('_')[-1])
    await ChangeExpensesCategoryStates.new_category_name.set()
    await state.update_data(current_category_id=current_category_id)
    await callback.message.edit_text('Введите новое название')


async def get_new_category_name(message: types.Message, state: FSMContext):
    new_name = message.text
    current_category_id = (await state.get_data())['current_category_id']
    await db_commands.new_category_name(message.from_user.id, current_category_id, new_name,
                                        ExpenseCategory)
    edit_category_keyboard = await ex_keyboards.edit_expenses_category()
    await message.answer('OK', reply_markup=edit_category_keyboard)
    await state.finish()


async def delete_category(callback: types.CallbackQuery):
    current_category_id = int(callback.data.split('_')[-1])
    await db_commands.delete_user_category(current_category_id, ExpenseCategory, ExpenseSubCategory)
    edit_category_keyboard = await ex_keyboards.edit_expenses_category()
    await callback.message.edit_text("OK", reply_markup=edit_category_keyboard)


async def change_sub_category(callback: types.CallbackQuery):
    current_sub_category_id = int(callback.data.split('_')[-1])
    current_sub_category_name = await db_commands.get_sub_category_name(current_sub_category_id)
    change_or_delete_expenses_sub_category_keyboard = await ex_keyboards.change_or_delete_expenses_sub_category(
        current_sub_category_id)
    await callback.message.edit_text(
        f'Изменить или удалить подкатегорию {current_sub_category_name}?',
        reply_markup=change_or_delete_expenses_sub_category_keyboard)


async def edit_sub_category(callback: types.CallbackQuery, state: FSMContext):
    current_sub_category_id = int(callback.data.split('_')[-1])
    await ChangeExpensesSubCategoryStates.new_sub_category_name.set()
    await state.update_data(current_sub_category_id=current_sub_category_id)
    await callback.message.edit_text('Введите новое название')


async def get_new_sub_category_name(message: types.Message, state: FSMContext):
    new_name = message.text
    current_sub_category_id = (await state.get_data())['current_sub_category_id']
    await db_commands.new_sub_category_name(message.from_user.id, current_sub_category_id, new_name,
                                            ExpenseSubCategory)
    edit_sub_category_keyboard = await ex_keyboards.edit_expenses_sub_category()
    await message.answer('OK', reply_markup=edit_sub_category_keyboard)
    await state.finish()
    await message.delete()


async def add_new_category(callback: types.CallbackQuery, state: FSMContext):
    await AddExpensesCategory.new_category_name.set()
    await callback.message.edit_text('Введите название новой категории')


async def get_add_category_name(message: types.Message, state: FSMContext):
    new_name = message.text
    await db_commands.add_category(message.from_user.id, new_name, ExpenseCategory)
    edit_category_keyboard = await ex_keyboards.edit_expenses_category()
    await message.answer('OK', reply_markup=edit_category_keyboard)
    await state.finish()


async def add_new_sub_category(callback: types.CallbackQuery, state: FSMContext):
    parent_id = int(callback.data.split('_')[-1])
    await AddExpensesSubCategory.new_sub_category_name.set()
    await state.update_data(category_id=parent_id)
    await callback.message.edit_text('Введите название новой подкатегории')


async def get_add_sub_category_name(message: types.Message, state: FSMContext):
    new_name = message.text
    parent_id = (await state.get_data())['category_id']
    await db_commands.add_sub_category(message.from_user.id, parent_id, new_name, ExpenseSubCategory)
    edit_category_keyboard = await ex_keyboards.edit_expenses_category()
    await message.answer('OK', reply_markup=edit_category_keyboard)
    await state.finish()


async def delete_sub_category(callback: types.CallbackQuery):
    current_sub_category_id = int(callback.data.split('_')[-1])
    await db_commands.delete_user_sub_category(current_sub_category_id)
    edit_sub_category_keyboard = await ex_keyboards.edit_expenses_sub_category()
    await callback.message.edit_text("OK", reply_markup=edit_sub_category_keyboard)


async def return_from_changing_category(callback: types.CallbackQuery):
    expenses_categories_keyboard = await ex_keyboards.expenses_categories_keyboard(
        callback.from_user.id)
    await callback.message.edit_text('Ваши категории расходов:',
                                     reply_markup=expenses_categories_keyboard)


async def return_from_changing_sub_category(callback: types.CallbackQuery):
    current_sub_category_id = int(callback.data.split('_')[-1])
    current_category_id = await db_commands.get_user_category_id_from_sub_category(
        current_sub_category_id, ExpenseSubCategory)
    current_category_name = await db_commands.get_category_name(current_category_id, ExpenseCategory)
    expenses_sub_categories_keyboard = await ex_keyboards.expenses_subcategories_keyboard(
        callback.from_user.id,
        current_category_id)
    await callback.message.edit_text(f'Подкатегории у {current_category_name}',
                                     reply_markup=expenses_sub_categories_keyboard)


async def return_from_editing(callback: types.CallbackQuery):
    category_keyboard = await ex_keyboards.expenses_categories_keyboard(callback.from_user.id)
    await callback.message.edit_text('Ваши категории расходов', reply_markup=category_keyboard)


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

    dp.register_callback_query_handler(return_from_changing_category, ClientFilter(True),
                                       text='back_to_e_categories')
    dp.register_callback_query_handler(return_from_changing_sub_category, ClientFilter(True),
                                       filters.Text(startswith='back_to_e_c_'))
    dp.register_callback_query_handler(return_from_editing, ClientFilter(True),
                                       text='edit_back_to_e_categories')

    dp.register_callback_query_handler(add_new_category, ClientFilter(True), text='add_e_c')
    dp.register_message_handler(get_add_category_name, ClientFilter(True),
                                state=AddExpensesCategory.new_category_name)

    dp.register_callback_query_handler(add_new_sub_category, ClientFilter(True),
                                       filters.Text(startswith='add_e_s_c_'))
    dp.register_message_handler(get_add_sub_category_name, ClientFilter(True),
                                state=AddExpensesSubCategory.new_sub_category_name)
    dp.register_message_handler(add_to_history, is_client=True, commands='-')
