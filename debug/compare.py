#!/usr/bin/python
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
from numpy import arange

#plt.xkcd()
ind = None
ymax = 0
width = 0.35
for size in ["10k", "100k", "200k", "1M", "10M"]:
    if size == "1M":
        textlabels = [i + s + rep for i in ["1", "2", "5", "w"]
                      for s in ["s", "r"] for rep in ["", "<"]]
    else:
        textlabels = [i + s for i in ["1", "2", "5", "w"] for s in ["s", "r"]]
    fig, ax = plt.subplots()
    rects = []
    for algo, color, offset in [("LRU", ("r", 1), 0),
                                ("MRU", ("g", 0.7), 1),
                                ("LFU", ("orange", 0.5), 2),
                                ("FIFO", ("b", 0.5), 3)]:
        means = []
        for thread in ["1", "2", "5", "write"]:
            for rule in ["seq", "rand"]:
                for t in [1000, 250]:
                    try:
                        x = reduce(lambda a, b: a + b,
                                   map(float,
                                       open("./result/" + algo + "/"
                                            + rule + thread + "*"
                                            + str(t) + "*" + size + ".txt",
                                            'r').readlines())) / 1000
                        ymax = x if x > ymax else ymax
                        means.append(x)
                    except Exception as e:
                        continue
        if not len(means):
            continue
        ind = arange(len(means))
        for index, mean in enumerate(means):

            rects.append(ax.bar(index * width * 6 + offset * width,
                                mean, width,
                                color=color[0], alpha=color[1]))

    ymax *= 1.2
    ax.set_ylim(0, ymax)
    ax.set_xlim(0, 6 * width * len(ind) - 2 * width)
    ax.set_ylabel('Time')
    ax.set_title('Time for ' + size)
    ax.set_xticks(ind * width * 6 + width * 2)
    ax.set_xticklabels(textlabels)
    ax.set_yticks(arange(0, ymax, round(ymax / 10, 2)))

    labels = [rects[i * len(rects) / 4] for i in range(4)]
    ax.legend(labels, ["LRU", "MRU", "LFU", "FIFO"], loc=0)
    plt.minorticks_on()
    plt.grid(True, which='both', axis='y')

    plt.savefig("./result/compare_" + size + ".png", format="png")
