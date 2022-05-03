import matplotlib.pyplot as plt


def draw_circle_diagram(filename, labels: iter, percentages: iter, explode=None):
    labels = tuple(labels)
    percentages = tuple(percentages)

    fig1, ax1 = plt.subplots()

    ax1.pie(percentages, explode=explode, labels=labels, autopct='%1.1f%%', shadow=True,
            startangle=90, colors=('#38CA44', '#9932CC'))

    ax1.axis('equal')
    plt.savefig(filename)

    return plt


if __name__ == '__main__':
    draw_circle_diagram('test_cd.png', ('revenues', 'expanses'), (40, 60)).show()
