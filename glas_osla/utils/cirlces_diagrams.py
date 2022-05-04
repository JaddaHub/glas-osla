import matplotlib.pyplot as plt
from random import choices


async def draw_circle_diagram(filename, labels: iter, percentages: iter, explode=None):
    labels = tuple(labels)
    percentages = tuple(percentages)

    fig1, ax1 = plt.subplots()

    colors = ('#7F152E', '#EDAE01', '#E94F08', '#D55448', '#FFA577', '#896E69')
    while True:
        color = choices(colors, k=len(labels))
        if len(color) == len(set(color)):
            break

    ax1.pie(percentages, explode=explode, labels=labels, autopct='%1.1f%%',
            startangle=90, colors=color)

    ax1.axis('equal')
    plt.savefig(filename)

    return plt
