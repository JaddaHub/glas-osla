import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime


async def draw_graphic(filename, amounts: iter, dates: iter):
    amounts = list(amounts)
    dates = list(dates)
    fig, ax = plt.subplots()
    ax.plot(dates, amounts)

    date_format = mdates.DateFormatter("%d-%m-%y")
    ax.xaxis.set_major_formatter(date_format)
    fig.autofmt_xdate()
    plt.savefig(filename)
