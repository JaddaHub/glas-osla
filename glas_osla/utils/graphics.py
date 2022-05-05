import matplotlib.pyplot as plt


async def draw_graphic(filename, amounts: iter, dates: iter):
    amounts = tuple(amounts)
    dates = tuple(dates)
    print(amounts)
    print(dates)
    plt.plot(*zip(amounts, dates))
    plt.savefig(filename)
