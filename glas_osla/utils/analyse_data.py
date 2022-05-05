from glas_osla.db import db_commands
from glas_osla.db.models.expenses_plots_md import ExpenseCategory, ExpenseSubCategory
from glas_osla.db.models.revenues_plots_md import RevenueCategory, RevenueSubCategory


async def make_deduction(user_data: list, stat_type):
    categories = {}
    print(user_data)
    for post in user_data:
        if len(post) == 2:
            sub_cat = None
        else:
            sub_cat = post[-1]
        amount, cat = post[:2]
        cat = str(cat)
        if sub_cat:
            sub_cat = str(sub_cat)
        categories.setdefault(cat, {'result': 0, 'sub_categories': {}})
        categories[cat]['sub_categories'].setdefault('Без названия', 0)
        if sub_cat is None:
            categories[cat]['sub_categories']['Без названия'] += amount
        else:
            categories[cat]['sub_categories'].setdefault(sub_cat, 0)
            categories[cat]['sub_categories'][sub_cat] += amount
        categories[cat]['result'] += amount

    new_order = sorted(categories.keys(), key=lambda x: categories[x]['result'], reverse=True)
    sorted_categories = {key: categories[key] for key in new_order}
    for category in sorted_categories:
        new_sub_order = sorted(categories[category]['sub_categories'].keys(),
                               key=lambda x: categories[category]['sub_categories'][x], reverse=True)
        new_sub_cat = {key: categories[category]['sub_categories'][key] for key in new_sub_order}
        sorted_categories[category]['sub_categories'] = new_sub_cat

    if not len(sorted_categories):
        return "Данных нет"

    most_sub_category_at_all = "Нет данных"
    most_sub_category_at_all_parent = "Нет данных"
    most_sub_category_at_all_amount = 0
    for category in sorted_categories:
        for sub_category in sorted_categories[category]['sub_categories']:
            if sorted_categories[category]['sub_categories'][sub_category] > most_sub_category_at_all_amount:
                most_sub_category_at_all = sub_category
                most_sub_category_at_all_parent = category
                most_sub_category_at_all_amount = sorted_categories[category]['sub_categories'][sub_category]

    most_category = new_order[0]
    most_category_amount = sorted_categories[most_category]['result']
    most_sub_category_in_category = list(sorted_categories[most_category]['sub_categories'].keys())[0]
    most_sub_category_in_category_amount = sorted_categories[most_category]['sub_categories'][
        most_sub_category_in_category]
    if stat_type == 'e':
        if most_category.isdigit():
            most_category = await db_commands.get_category_name(int(most_category), ExpenseCategory)
        if most_sub_category_in_category.isdigit():
            most_sub_category_in_category = await db_commands.get_sub_category_name(int(most_sub_category_in_category),
                                                                                    ExpenseSubCategory)
        if most_sub_category_at_all.isdigit():
            most_sub_category_at_all = await db_commands.get_sub_category_name(int(most_sub_category_at_all),
                                                                               ExpenseSubCategory)
        if most_sub_category_at_all_parent.isdigit():
            most_sub_category_at_all_parent = await db_commands.get_category_name(int(most_sub_category_at_all_parent),
                                                                                  ExpenseCategory)
        result = f"Наиболее расходная категория: {most_category}.\n" \
                 f"Вы на неё потратили: {most_category_amount} рублей.\n\n" \
                 f"В ней больше всего тратила подкатегория: {most_sub_category_in_category}\n" \
                 f"Вы на неё потратили: {most_sub_category_in_category_amount} рублей.\n\n" \
                 f"В целом, самая расходная подкатегория за этот период: {most_sub_category_at_all} (в категории {most_sub_category_at_all_parent})\n" \
                 f"На неё вы потратили: {most_category_amount} рублей."

    elif stat_type == 'r':
        most_category = await db_commands.get_category_name(int(most_category), RevenueCategory)
        most_sub_category_in_category = await db_commands.get_sub_category_name(int(most_sub_category_in_category),
                                                                                RevenueSubCategory)
        most_sub_category_at_all = await db_commands.get_sub_category_name(int(most_sub_category_at_all),
                                                                           RevenueSubCategory)
        most_sub_category_at_all_parent = await db_commands.get_category_name(int(most_sub_category_at_all_parent),
                                                                              RevenueCategory)
        result = f"Наиболее прибыльная категория: {most_category}.\n" \
                 f"Вы на ней заработали: {most_category_amount} рублей.\n\n" \
                 f"В ней больше всего заработала подкатегория: {most_sub_category_in_category}\n" \
                 f"На этой подкатегории вы заработали: {most_sub_category_in_category_amount} рублей.\n\n" \
                 f"В целом, самая прибыльная подкатегория за этот период: {most_sub_category_at_all} (в категории {most_sub_category_at_all_parent})\n" \
                 f"На этой подкатегории вы заработали: {most_category_amount} рублей."
    else:
        result = "Данных нет"
    return result
