import logging
from datetime import datetime, timedelta

from .base import async_session
from sqlalchemy import select, update, delete, insert, and_
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


async def get_user_expenses_category_id_from_sub_category(sub_category_id):
    async with async_session() as db_sess:
        cat_query = select(ExpenseSubCategory.parent).where(ExpenseSubCategory.id == sub_category_id)
        category_id = (await db_sess.execute(cat_query)).first()[0]
        return category_id


async def get_user_expenses_subcategories(message_author_id, category_id):
    user_db_id = await get_user_db_id(message_author_id)
    async with async_session() as db_sess:
        sub_cat_query = select(ExpenseSubCategory.id, ExpenseSubCategory.name).where(
            and_(ExpenseSubCategory.user_id == user_db_id, ExpenseSubCategory.parent == category_id))
        sub_categories = (await db_sess.execute(sub_cat_query)).all()
        return sub_categories


async def get_user_revenues_categories(message_author_id):
    user_db_id = await get_user_db_id(message_author_id)
    async with async_session() as db_sess:
        cat_query = select(RevenueCategory.id, RevenueCategory.name).where(
            RevenueCategory.user_id == user_db_id)
        categories = (await db_sess.execute(cat_query)).all()
        return categories


async def get_user_revenues_subcategories(message_author_id, category_id):
    user_db_id = await get_user_db_id(message_author_id)
    async with async_session() as db_sess:
        sub_cat_query = select(RevenueSubCategory.id, RevenueSubCategory.name).where(
            and_(RevenueSubCategory.user_id == user_db_id, RevenueSubCategory.parent == category_id))
        sub_categories = (await db_sess.execute(sub_cat_query)).all()
        return sub_categories


async def get_expenses_category_name(category_id):
    async with async_session() as db_sess:
        category_query = select(ExpenseCategory.name).where(ExpenseCategory.id == category_id)
        category_name = (await db_sess.execute(category_query)).first()[0]
        return category_name


async def new_expenses_category_name(message_author_id, category_id, new_name):
    user_db_id = await get_user_db_id(message_author_id)
    async with async_session() as db_sess:
        async with db_sess.begin():
            new_category_name_query = update(ExpenseCategory).where(
                and_(ExpenseCategory.id == category_id,
                     ExpenseCategory.user_id == user_db_id)).values(name=new_name)
            await db_sess.execute(new_category_name_query)
        await db_sess.commit()


async def new_expenses_sub_category_name(message_author_id, sub_category_id, new_name):
    user_db_id = await get_user_db_id(message_author_id)
    async with async_session() as db_sess:
        async with db_sess.begin():
            new_sub_category_name_query = update(ExpenseSubCategory).where(
                and_(ExpenseSubCategory.id == sub_category_id,
                     ExpenseSubCategory.user_id == user_db_id)).values(
                name=new_name)
            await db_sess.execute(new_sub_category_name_query)
        await db_sess.commit()


async def delete_user_expenses_category(category_id):
    async with async_session() as db_sess:
        async with db_sess.begin():
            delete_category_query1 = delete(ExpenseSubCategory).where(
                ExpenseSubCategory.parent == category_id)
            delete_category_query2 = delete(ExpenseCategory).where(ExpenseCategory.id == category_id)
            await db_sess.execute(delete_category_query1)
            await db_sess.execute(delete_category_query2)
        await db_sess.commit()


async def delete_user_sub_category(sub_category_id):
    async with async_session() as db_sess:
        async with db_sess.begin():
            delete_category_query = delete(ExpenseSubCategory).where(
                ExpenseSubCategory.id == sub_category_id)
            await db_sess.execute(delete_category_query)
        await db_sess.commit()


async def add_expenses_category(message_author_id, category_name):
    db_id = await get_user_db_id(message_author_id)
    new_category = ExpenseCategory()
    new_category.user_id = db_id
    new_category.name = category_name
    async with async_session() as db_sess:
        async with db_sess.begin():
            db_sess.add(new_category)
        await db_sess.commit()


async def add_expenses_sub_category(message_author_id, parent_id, sub_category_name):
    db_id = await get_user_db_id(message_author_id)
    new_sub_category = ExpenseSubCategory()
    new_sub_category.user_id = db_id
    new_sub_category.parent = parent_id
    new_sub_category.name = sub_category_name
    async with async_session() as db_sess:
        async with db_sess.begin():
            db_sess.add(new_sub_category)
        await db_sess.commit()


async def add_revenues_category(message_author_id, category_name):
    db_id = await get_user_db_id(message_author_id)
    new_category = RevenueCategory()
    new_category.user_id = db_id
    new_category.name = category_name
    async with async_session() as db_sess:
        async with db_sess.begin():
            db_sess.add(new_category)
        await db_sess.commit()
    logging.info(f'категория {category_name} добавлена')


async def add_revenues_sub_category(message_author_id, parent_id, sub_category_name):
    db_id = await get_user_db_id(message_author_id)
    new_sub_category = RevenueSubCategory()
    new_sub_category.user_id = db_id
    new_sub_category.parent = parent_id
    new_sub_category.name = sub_category_name
    async with async_session() as db_sess:
        async with db_sess.begin():
            db_sess.add(new_sub_category)
        await db_sess.commit()
    logging.info(f'подкатегория {sub_category_name} добавлена')


async def get_expenses_category_id(category_name):
    async with async_session() as db_sess:
        cat_query = select(ExpenseCategory.id).where(ExpenseCategory.name == category_name)
        cat_id = (await db_sess.execute(cat_query)).first()[0]
        return cat_id


async def get_sub_category_name(sub_category_id):
    async with async_session() as db_sess:
        sub_cat_query = select(ExpenseSubCategory.name).where(
            ExpenseSubCategory.id == sub_category_id)
        sub_cat_name = (await db_sess.execute(sub_cat_query)).first()[0]
        return sub_cat_name


async def quick_add_to_revenues(params: dict):
    user_tg_id = params['user_id']
    user_db_id = await get_user_db_id(user_tg_id)

    revenue = Revenue()
    revenue.user_id = user_db_id

    user_category = params['category']
    user_sub_category = params.get('sub_category')

    categories = await get_user_revenues_categories(user_tg_id)
    if not categories:
        categories = [(0, 0)]
    for id, category in categories:
        if category == user_category:
            category_id = revenue.category = id
            break
    else:
        await add_revenues_category(user_tg_id, user_category)
        category_id = revenue.category = categories[-1][0] + 1

    sub_categories = await get_user_revenues_subcategories(user_tg_id, category_id)
    if not sub_categories:
        sub_categories = [(0, 0)]

    if user_sub_category:
        for id, sub_category in sub_categories:
            if sub_category == user_sub_category:
                revenue.sub_category = id
                break
        else:
            await add_revenues_sub_category(user_tg_id, category_id, user_sub_category)
            revenue.sub_category = sub_categories[-1][0] + 1

    revenue.amount = int(params['amount'])
    revenue.note = params.get('note')
    async with async_session() as db_sess:
        async with db_sess.begin():
            db_sess.add(revenue)
        await db_sess.commit()
    logging.info(f'запись {revenue.id} добавлена')


async def get_user_revenues_in_time(message_author_id, time: timedelta):
    user_db_id = await get_user_db_id(message_author_id)
    async with async_session() as db_sess:
        revenues_cat_query = select(Revenue.amount).where(
            and_(datetime.now() - Revenue.date <= time, Revenue.user_id == user_db_id))
        revenues = (await db_sess.execute(revenues_cat_query)).all()
        return revenues
