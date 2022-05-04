from aiogram.dispatcher import Dispatcher


# from glas_osla.keyboards.inline import keyboards
#
#
# async def get_graphics(callback: types.CallbackQuery):
#     await callback.message.answer('Выберите на каком отрезке будет строиться график',
#                                   reply_markup=keyboards.graphics_keyboard)
#
#
# async def show_week_graphic(callback: types.CallbackQuery):
#     photo = InputFile('glas_osla/resources/img/graphics/')
#     await callback.bot.send_photo(callback.from_user.id, photo=photo,
#                                   reply_markup=keyboards.current_graphic_keyboard)
#
#
# async def show_month_graphic(callback: types.CallbackQuery):
#     photo = InputFile('glas_osla/resources/img/graphics/')
#     await callback.bot.send_photo(callback.from_user.id, photo,
#                                   reply_markup=keyboards.current_graphic_keyboard)
#
#
# async def show_year_graphic(callback: types.CallbackQuery):
#     photo = InputFile('glas_osla/resources/img/graphics/')
#     await callback.bot.send_photo(callback.from_user.id, photo,
#                                   reply_markup=keyboards.current_graphic_keyboard)
#
# #
# # async def current_back_to_graphics(callback: types.CallbackQuery):
# #     await get_graphics(callback)
#
#
def setup_graphics_handlers(dp: Dispatcher):
    pass
#     dp.register_callback_query_handler(get_graphics, is_client=True, text='get_graphics')
#     dp.register_callback_query_handler(show_week_graphic, is_client=True, text='show_week_graphic')
#     dp.register_callback_query_handler(show_month_graphic, is_client=True, text='show_month_graphic')
#     dp.register_callback_query_handler(show_year_graphic, is_client=True, text='show_year_graphic')
#     dp.register_callback_query_handler(current_back_to_graphics, is_client=True,
#                                        text='current_back_to_graphics')
