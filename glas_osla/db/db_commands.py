import logging
from datetime import datetime, timedelta

from .base import async_session
from typing import Union
from sqlalchemy import select, update, delete, insert, and_

from .models.expenses_md import Expense
from .models.users_md import User
from .models.expenses_plots_md import ExpenseCategory, ExpenseSubCategory
from .models.revenues_plots_md import RevenueCategory, RevenueSubCategory
from .models.revenues_md import Revenue
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


async def get_user_categories(message_author_id, db_model: Union[ExpenseCategory, RevenueCategory]):
    user_db_id = await get_user_db_id(message_author_id)
    async with async_session() as db_sess:
        cat_query = select(db_model.id, db_model.name).where(
            db_model.user_id == user_db_id)
        categories = (await db_sess.execute(cat_query)).all()
        return categories


async def get_user_subcategories(
        message_author_id, category_id, db_model: Union[ExpenseSubCategory, RevenueSubCategory]):
    user_db_id = await get_user_db_id(message_author_id)
    async with async_session() as db_sess:
        sub_cat_query = select(db_model.id, db_model.name).where(
            and_(db_model.user_id == user_db_id, db_model.parent == category_id))
        sub_categories = (await db_sess.execute(sub_cat_query)).all()
        return sub_categories


async def get_user_category_id_from_sub_category(
        sub_category_id, db_model: Union[ExpenseSubCategory, RevenueSubCategory]):
    async with async_session() as db_sess:
        cat_query = select(db_model.parent).where(db_model.id == sub_category_id)
        category_id = (await db_sess.execute(cat_query)).first()[0]
        return category_id


async def get_category_name(category_id, db_model: Union[ExpenseCategory, RevenueCategory]):
    async with async_session() as db_sess:
        category_query = select(db_model.name).where(db_model.id == category_id)
        category_name = (await db_sess.execute(category_query)).first()[0]
        return category_name


async def new_category_name(
        message_author_id, category_id, new_name,
        db_model: Union[ExpenseCategory, RevenueCategory]):
    user_db_id = await get_user_db_id(message_author_id)
    async with async_session() as db_sess:
        async with db_sess.begin():
            new_category_name_query = update(db_model).where(
                and_(db_model.id == category_id, db_model.user_id == user_db_id)).values(
                name=new_name)
            await db_sess.execute(new_category_name_query)
        await db_sess.commit()


async def new_sub_category_name(
        message_author_id, sub_category_id, new_name,
        db_model: Union[ExpenseSubCategory, RevenueSubCategory]):
    user_db_id = await get_user_db_id(message_author_id)
    async with async_session() as db_sess:
        async with db_sess.begin():
            new_sub_category_name_query = update(db_model).where(
                and_(db_model.id == sub_category_id, db_model.user_id == user_db_id)).values(
                name=new_name)
            await db_sess.execute(new_sub_category_name_query)
        await db_sess.commit()


async def delete_user_category(
        category_id, db_model_category: Union[ExpenseCategory, RevenueCategory],
        db_model_sub_category: Union[ExpenseSubCategory, RevenueSubCategory]):
    async with async_session() as db_sess:
        async with db_sess.begin():
            delete_category_query1 = delete(db_model_sub_category).where(
                db_model_sub_category.parent == category_id)
            delete_category_query2 = delete(db_model_category).where(
                db_model_category.id == category_id)
            await db_sess.execute(delete_category_query1)
            await db_sess.execute(delete_category_query2)
        await db_sess.commit()


async def delete_user_sub_category(
        sub_category_id, db_model: Union[ExpenseSubCategory, RevenueSubCategory]):
    async with async_session() as db_sess:
        async with db_sess.begin():
            delete_category_query = delete(db_model).where(db_model.id == sub_category_id)
            await db_sess.execute(delete_category_query)
        await db_sess.commit()


async def add_category(
        message_author_id, category_name, db_model: Union[ExpenseCategory, RevenueCategory]):
    db_id = await get_user_db_id(message_author_id)
    new_category = db_model()
    new_category.user_id = db_id
    new_category.name = category_name
    async with async_session() as db_sess:
        async with db_sess.begin():
            db_sess.add(new_category)
        await db_sess.commit()
    logging.info(f'категория {category_name} добавлена')


async def add_sub_category(
        message_author_id, parent_id, sub_category_name,
        db_model: Union[ExpenseSubCategory, RevenueSubCategory]):
    db_id = await get_user_db_id(message_author_id)
    new_sub_category = db_model()
    new_sub_category.user_id = db_id
    new_sub_category.parent = parent_id
    new_sub_category.name = sub_category_name
    async with async_session() as db_sess:
        async with db_sess.begin():
            db_sess.add(new_sub_category)
        await db_sess.commit()


async def get_category_id(category_name, db_model: Union[ExpenseCategory, RevenueCategory]):
    async with async_session() as db_sess:
        cat_query = select(db_model.id).where(db_model.name == category_name)
        cat_id = (await db_sess.execute(cat_query)).first()[0]
        return cat_id


async def get_sub_category_name(
        sub_category_id, db_model: Union[ExpenseSubCategory, RevenueSubCategory]):
    async with async_session() as db_sess:
        sub_cat_query = select(db_model.name).where(db_model.id == sub_category_id)
        sub_cat_name = (await db_sess.execute(sub_cat_query)).first()[0]
        return sub_cat_name


async def quick_add_to_revenues(params: dict):
    user_tg_id = params['user_id']
    user_db_id = await get_user_db_id(user_tg_id)

    revenue = Revenue()
    revenue.user_id = user_db_id

    user_category = params['category']
    user_sub_category = params.get('sub_category')

    categories = await get_user_categories(user_tg_id, RevenueCategory)
    if not categories:
        categories = [(0, 0)]
    for id, category in categories:
        if category == user_category:
            category_id = revenue.category = id
            break
    else:
        await add_category(user_tg_id, user_category, RevenueCategory)
        category_id = revenue.category = categories[-1][0] + 1

    sub_categories = await get_user_subcategories(user_tg_id, category_id, RevenueSubCategory)
    if not sub_categories:
        sub_categories = [(0, 0)]

    if user_sub_category:
        for id, sub_category in sub_categories:
            if sub_category == user_sub_category:
                revenue.sub_category = id
                break
        else:
            await add_sub_category(user_tg_id, category_id, user_sub_category, RevenueSubCategory)
            revenue.sub_category = sub_categories[-1][0] + 1

    revenue.amount = int(params['amount'])
    revenue.note = params.get('note')
    async with async_session() as db_sess:
        async with db_sess.begin():
            db_sess.add(revenue)
        await db_sess.commit()
    logging.info(f'запись {revenue.id} добавлена')


async def quick_add_to_expenses(params: dict):
    user_tg_id = params['user_id']
    user_db_id = await get_user_db_id(user_tg_id)

    expenses = Expense()
    expenses.user_id = user_db_id

    user_category = params['category']
    user_sub_category = params.get('sub_category')

    categories = await get_user_categories(user_tg_id, ExpenseCategory)
    if not categories:
        categories = [(0, 0)]
    for id, category in categories:
        if category == user_category:
            category_id = expenses.category = id
            break
    else:
        await add_category(user_tg_id, user_category, ExpenseCategory)
        category_id = expenses.category = categories[-1][0] + 1

    sub_categories = await get_user_subcategories(user_tg_id, category_id, ExpenseSubCategory)
    if not sub_categories:
        sub_categories = [(0, 0)]

    if user_sub_category:
        for id, sub_category in sub_categories:
            if sub_category == user_sub_category:
                expenses.sub_category = id
                break
        else:
            await add_sub_category(user_tg_id, category_id, user_sub_category, ExpenseSubCategory)
            expenses.sub_category = sub_categories[-1][0] + 1

    expenses.amount = int(params['amount'])
    expenses.note = params.get('note')
    async with async_session() as db_sess:
        async with db_sess.begin():
            db_sess.add(expenses)
        await db_sess.commit()
    logging.info(f'запись {expenses.id} добавлена')


async def get_user_in_time(
        message_author_id, time: timedelta, db_model: Union[Revenue, Expense]):
    user_db_id = await get_user_db_id(message_author_id)
    async with async_session() as db_sess:
        db_model_cat_query = select(db_model.amount, db_model.category, db_model.sub_category).where(
            and_(datetime.now() - db_model.date <= time, db_model.user_id == user_db_id))
        data = (await db_sess.execute(db_model_cat_query)).all()
        return data
