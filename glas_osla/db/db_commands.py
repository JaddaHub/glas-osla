import logging
from datetime import datetime, timedelta

from .base import async_session
from sqlalchemy import select, and_
from .models.users_md import User
from .models.expenses_plots_md import ExpenseCategory, ExpenseSubCategory
from .models.revenues_plots_md import RevenueCategory, RevenueSubCategory
from .models.revenues_md import Revenue


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


async def quick_add_to_revenues(params: dict):
    user_tg_id = params['user_id']
    user_db_id = await get_user_db_id(user_tg_id)

    revenue = Revenue()
    revenue.user_id = user_db_id

    categories = await get_user_revenues_categories(user_tg_id)
    if not categories:
        categories = [(0, 0)]
    sub_categories = await get_user_revenues_subcategories(user_tg_id)
    if not sub_categories:
        sub_categories = [(0, 0)]

    user_category = params['category']
    user_sub_category = params.get('sub_category')

    for id, category in categories:
        if category == user_category:
            category_id = revenue.category = id
            break
    else:
        await add_new_category(user_db_id, user_category)
        category_id = revenue.category = categories[-1][0] + 1

    if user_sub_category:
        for id, sub_category in sub_categories:
            if sub_category == user_sub_category:
                revenue.sub_category = id
                break
        else:
            await add_new_subcategory(user_db_id, user_sub_category, category_id)
            revenue.sub_category = sub_categories[-1][0] + 1

    revenue.amount = int(params['amount'])
    revenue.note = params.get('note')
    async with async_session() as db_sess:
        async with db_sess.begin():
            db_sess.add(revenue)
        await db_sess.commit()
    logging.info(f'запись {revenue.id} добавлена')


async def add_new_category(user_db_id, category_name):
    category = RevenueCategory()
    category.user_id = user_db_id
    category.name = category_name
    async with async_session() as db_sess:
        async with db_sess.begin():
            db_sess.add(category)
        await db_sess.commit()
    logging.info(f'категория {category.name} добавлена')


async def add_new_subcategory(user_db_id, sub_category_name, category_id):
    sub_category = RevenueSubCategory()
    sub_category.user_id = user_db_id
    sub_category.parent = category_id
    sub_category.name = sub_category_name
    async with async_session() as db_sess:
        async with db_sess.begin():
            db_sess.add(sub_category)
        await db_sess.commit()
    logging.info(f'подкатегория {sub_category.name} добавлена')


async def get_user_revenues_in_time(message_author_id, time: timedelta):
    user_db_id = await get_user_db_id(message_author_id)
    async with async_session() as db_sess:
        revenues_cat_query = select(Revenue.amount).where(
            and_(datetime.now() - Revenue.date <= time, Revenue.user_id == user_db_id))
        revenues = (await db_sess.execute(revenues_cat_query)).all()
        return revenues
