from aiogram import types
from aiogram.dispatcher import Dispatcher, FSMContext, filters

from glas_osla.db import db_commands
from glas_osla.db.db_commands import quick_add_to_revenues
from glas_osla.db.models.revenues_plots_md import RevenueCategory, RevenueSubCategory
from glas_osla.filters.is_client import ClientFilter
from glas_osla.keyboards.inline import (
    revenues_keyboards as re_keyboards,
    general_keyboards as gen_keyboards
)
from glas_osla.states.RevenuesStates import (
    ChangeRevenuesCategoryStates,
    ChangeRevenuesSubCategoryStates,
    AddRevenuesCategory, AddRevenuesSubCategory
)
from glas_osla.templates.general_phrases import *


async def add_to_history(message: types.Message):
    try:
        arguments = message.text.split()[1:]
        int(arguments[0])
        if len(arguments) > 4:
            raise IndexError
    except (IndexError, ValueError):
        await message.answer('Введены неверные аргументы\n/quick - информация о быстрой команде')
        return

    if not arguments:
        await message.answer(must_input_args_text)
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
    print(params)
    await quick_add_to_revenues(params)
    await message.answer(post_added_text)


async def return_to_menu(callback: types.CallbackQuery):
    await callback.message.edit_text(menu_text, reply_markup=gen_keyboards.menu_keyboard)


async def get_categories(callback: types.CallbackQuery):
    expenses_categories_keyboard = await re_keyboards.revenues_categories_keyboard(
        callback.from_user.id)
    await callback.message.edit_text(f'{your_revenues_cat_text}',
                                     reply_markup=expenses_categories_keyboard)


async def get_sub_categories(callback: types.CallbackQuery):
    current_category_id = int(callback.data.split('_')[-1])
    current_category_name = await db_commands.get_category_name(current_category_id, RevenueCategory)
    expenses_sub_categories_keyboard = await re_keyboards.revenues_subcategories_keyboard(
        callback.from_user.id,
        current_category_id)
    await callback.message.edit_text(f'{sub_cats_from_text} {current_category_name}',
                                     reply_markup=expenses_sub_categories_keyboard)


async def change_category(callback: types.CallbackQuery):
    current_category_id = int(callback.data.split('_')[-1])
    current_category_name = await db_commands.get_category_name(current_category_id, RevenueCategory)
    change_or_delete_expenses_category_keyboard = await re_keyboards.change_or_delete_revenues_category(
        current_category_id)
    await callback.message.edit_text(f'{edit_or_delete_cat_text} {current_category_name}?',
                                     reply_markup=change_or_delete_expenses_category_keyboard)


async def edit_category(callback: types.CallbackQuery, state: FSMContext):
    current_category_id = int(callback.data.split('_')[-1])
    await ChangeRevenuesCategoryStates.new_category_name.set()
    await state.update_data(current_category_id=current_category_id)
    await callback.message.edit_text(enter_new_name_text)


async def get_new_category_name(message: types.Message, state: FSMContext):
    new_name = message.text
    current_category_id = (await state.get_data())['current_category_id']
    await db_commands.new_category_name(message.from_user.id, current_category_id, new_name,
                                        RevenueCategory)
    edit_category_keyboard = await re_keyboards.edit_revenues_category()
    await message.answer(ok_text, reply_markup=edit_category_keyboard)
    await state.finish()


async def delete_category(callback: types.CallbackQuery):
    current_category_id = int(callback.data.split('_')[-1])
    await db_commands.delete_user_category(current_category_id, RevenueCategory, RevenueSubCategory)
    edit_category_keyboard = await re_keyboards.edit_revenues_category()
    await callback.message.edit_text(ok_text, reply_markup=edit_category_keyboard)


async def change_sub_category(callback: types.CallbackQuery):
    current_sub_category_id = int(callback.data.split('_')[-1])
    current_sub_category_name = await db_commands.get_sub_category_name(callback.from_user.id, current_sub_category_id,
                                                                        RevenueSubCategory)
    change_or_delete_expenses_sub_category_keyboard = await re_keyboards.change_or_delete_revenues_sub_category(
        current_sub_category_id)
    await callback.message.edit_text(f'{edit_or_delete_sub_cat_text} {current_sub_category_name}?',
                                     reply_markup=change_or_delete_expenses_sub_category_keyboard)


async def edit_sub_category(callback: types.CallbackQuery, state: FSMContext):
    current_sub_category_id = int(callback.data.split('_')[-1])
    await ChangeRevenuesSubCategoryStates.new_sub_category_name.set()
    await state.update_data(current_sub_category_id=current_sub_category_id)
    await callback.message.edit_text(enter_new_name_text)


async def get_new_sub_category_name(message: types.Message, state: FSMContext):
    new_name = message.text
    current_sub_category_id = (await state.get_data())['current_sub_category_id']
    await db_commands.new_sub_category_name(message.from_user.id, current_sub_category_id, new_name,
                                            RevenueSubCategory)
    edit_sub_category_keyboard = await re_keyboards.edit_revenues_sub_category()
    await message.answer(ok_text, reply_markup=edit_sub_category_keyboard)
    await state.finish()
    await message.delete()


async def add_new_category(callback: types.CallbackQuery, state: FSMContext):
    await AddRevenuesCategory.new_category_name.set()
    await callback.message.edit_text(enter_add_cat_name_text)


async def get_add_category_name(message: types.Message, state: FSMContext):
    new_name = message.text
    await db_commands.add_category(message.from_user.id, new_name, RevenueCategory)
    edit_category_keyboard = await re_keyboards.edit_revenues_category()
    await message.answer(ok_text, reply_markup=edit_category_keyboard)
    await state.finish()


async def add_new_sub_category(callback: types.CallbackQuery, state: FSMContext):
    parent_id = int(callback.data.split('_')[-1])
    await AddRevenuesSubCategory.new_sub_category_name.set()
    await state.update_data(category_id=parent_id)
    await callback.message.edit_text(enter_add_sub_cat_name_text)


async def get_add_sub_category_name(message: types.Message, state: FSMContext):
    new_name = message.text
    parent_id = (await state.get_data())['category_id']
    await db_commands.add_sub_category(message.from_user.id, parent_id, new_name, RevenueSubCategory)
    edit_category_keyboard = await re_keyboards.edit_revenues_sub_category()
    await message.answer(ok_text, reply_markup=edit_category_keyboard)
    await state.finish()


async def delete_sub_category(callback: types.CallbackQuery):
    current_sub_category_id = int(callback.data.split('_')[-1])
    await db_commands.delete_user_sub_category(current_sub_category_id)
    edit_sub_category_keyboard = await re_keyboards.edit_revenues_sub_category()
    await callback.message.edit_text(ok_text, reply_markup=edit_sub_category_keyboard)


async def return_from_changing_category(callback: types.CallbackQuery):
    expenses_categories_keyboard = await re_keyboards.revenues_categories_keyboard(
        callback.from_user.id)
    await callback.message.edit_text(your_revenues_cat_text,
                                     reply_markup=expenses_categories_keyboard)


async def return_from_changing_sub_category(callback: types.CallbackQuery):
    current_sub_category_id = int(callback.data.split('_')[-1])
    current_category_id = await db_commands.get_user_category_id_from_sub_category(
        current_sub_category_id,
        RevenueSubCategory)
    current_category_name = await db_commands.get_category_name(current_category_id, RevenueCategory)
    expenses_sub_categories_keyboard = await re_keyboards.revenues_subcategories_keyboard(
        callback.from_user.id,
        current_category_id)
    await callback.message.edit_text(f'{sub_cats_from_text} {current_category_name}',
                                     reply_markup=expenses_sub_categories_keyboard)


async def return_from_editing(callback: types.CallbackQuery):
    category_keyboard = await re_keyboards.revenues_categories_keyboard(callback.from_user.id)
    await callback.message.edit_text(your_revenues_cat_text, reply_markup=category_keyboard)


def setup_revenues_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(return_to_menu, ClientFilter(True), text='r_c_back_to_menu')
    dp.register_callback_query_handler(get_categories, ClientFilter(True), text='get_revenues')
    dp.register_callback_query_handler(get_sub_categories, ClientFilter(True),
                                       filters.Text(startswith='r_c_'))
    dp.register_callback_query_handler(change_category, ClientFilter(True),
                                       filters.Text(startswith='change_r_c_'))
    dp.register_callback_query_handler(edit_category, ClientFilter(True),
                                       filters.Text(startswith='edit_r_c_'))
    dp.register_message_handler(get_new_category_name, ClientFilter(True),
                                state=ChangeRevenuesCategoryStates.new_category_name)
    dp.register_callback_query_handler(delete_category, ClientFilter(True),
                                       filters.Text(startswith='del_r_c_'))

    dp.register_callback_query_handler(change_sub_category, ClientFilter(True),
                                       filters.Text(startswith='r_s_c_'))
    dp.register_callback_query_handler(edit_sub_category, ClientFilter(True),
                                       filters.Text(startswith='edit_r_s_c_'))
    dp.register_message_handler(get_new_sub_category_name, ClientFilter(True),
                                state=ChangeRevenuesSubCategoryStates.new_sub_category_name)
    dp.register_callback_query_handler(delete_sub_category, ClientFilter(True),
                                       filters.Text(startswith='del_r_s_c_'))

    dp.register_callback_query_handler(return_from_changing_category, ClientFilter(True),
                                       text='back_to_r_categories')
    dp.register_callback_query_handler(return_from_changing_sub_category, ClientFilter(True),
                                       filters.Text(startswith='back_to_r_c_'))
    dp.register_callback_query_handler(return_from_editing, ClientFilter(True),
                                       text='edit_back_to_r_categories')

    dp.register_callback_query_handler(add_new_category, ClientFilter(True), text='add_r_c')
    dp.register_message_handler(get_add_category_name, ClientFilter(True),
                                state=AddRevenuesCategory.new_category_name)

    dp.register_callback_query_handler(add_new_sub_category, ClientFilter(True),
                                       filters.Text(startswith='add_r_s_c_'))
    dp.register_message_handler(get_add_sub_category_name, ClientFilter(True),
                                state=AddRevenuesSubCategory.new_sub_category_name)
    dp.register_message_handler(add_to_history, ClientFilter(True), commands='a')
    dp.register_message_handler(add_to_history, is_client=True, commands='+')
