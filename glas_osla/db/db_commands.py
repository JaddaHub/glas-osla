from .base import async_session
from sqlalchemy import select
from .models.users_md import User
from .models.expenses_plots_md import ExpenseCategory, ExpenseSubCategory
from .models.revenues_plots_md import RevenueCategory, RevenueSubCategory


async def get_user_db_id(message_author_id):
    async with async_session() as db_sess:
        id_query = select(User.id).where(User.tg_id == message_author_id)
        db_id = (await db_sess.execute(id_query)).first()[0]
        return db_id


async def get_user_nickname(message_author_id):
    async with async_session() as db_sess:
        id_query = select(User.name).where(User.tg_id == message_author_id)
        db_name = (await db_sess.execute(id_query)).first()[0]
        return db_name


async def get_user_expenses_categories(message_author_id):
    user_db_id = await get_user_db_id(message_author_id)
    async with async_session() as db_sess:
        cat_query = select(ExpenseCategory.id, ExpenseCategory.name).where(
            ExpenseCategory.user_id == user_db_id)
        categories = (await db_sess.execute(cat_query)).all()
        return categories


async def get_user_expenses_subcategories(message_author_id):
    user_db_id = await get_user_db_id(message_author_id)
    async with async_session() as db_sess:
        sub_cat_query = select(ExpenseSubCategory.id, ExpenseSubCategory.name).where(
            ExpenseSubCategory.user_id == user_db_id)
        sub_categories = (await db_sess.execute(sub_cat_query)).all()
        return sub_categories


async def get_user_revenues_categories(message_author_id):
    user_db_id = await get_user_db_id(message_author_id)
    async with async_session() as db_sess:
        cat_query = select(RevenueCategory.id, RevenueCategory.name).where(
            RevenueCategory.user_id == user_db_id)
        categories = (await db_sess.execute(cat_query)).all()
        return categories


async def get_user_revenues_subcategories(message_author_id):
    user_db_id = await get_user_db_id(message_author_id)
    async with async_session() as db_sess:
        sub_cat_query = select(RevenueSubCategory.id, RevenueSubCategory.name).where(
            RevenueSubCategory.user_id == user_db_id)
        sub_categories = (await db_sess.execute(sub_cat_query)).all()
        return sub_categories
