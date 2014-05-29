#!/usr/bin/python
import matplotlib

#matplotlib.use('Agg')
import matplotlib.pyplot as plt
from numpy import arange
from matplotlib.pyplot import Rectangle

#plt.xkcd()
ind = arange(4)
ymin, ymax = 100, 0
width = 0.35
for size in ["10k", "100k", "200k", "1M", "10M"]:
    if size == "1M":
        textlabels = filter(
            lambda a: a != "wr<",
            [i + s + rep if i + s + rep != "ws<" else ""
             for i in ["1", "2", "5", "w"]
             for s in ["s", "r"] for rep in ["", "<"]])
    else:
        textlabels = [i + s for i in ["1", "2", "5", "w"] for s in ["s", "r"]]
    fig, ax = plt.subplots()
    rects = []
    j = 0
    for thread in ["1", "2", "5", "write"]:
        for rule in ["seq", "rand"]:
            ts = [1000]
            if size == "1M":
                ts.append(250)
            for t in ts:
                means = []
                for algo, color, offset in [("LRU", "r", 0),
                                            ("MRU", "g", 1),
                                            ("LFU", "orange", 2),
                                            ("FIFO", "b", 3)]:
                    try:
                        x = reduce(lambda a, b: a + b,
                                   map(float,
                                       open("./result/" + algo + "/"
                                            + rule + thread + "*"
                                            + str(t) + "*" + size + ".txt",
                                            'r').readlines())) / 1000
                        ymax = x if x > ymax else ymax
                        ymin = x if x < ymin else ymin
                        means.append((x, color))
                    except Exception as e:
                        continue

                for offset, (mean, color) in enumerate(means):
                    rects.append(
                        ax.bar(j * width * 6 + offset * width,
                               mean, width, linewidth=0, color=color,
                               alpha=1
                               if mean == min(map(lambda m: m[0], means))
                               else 0.2))
                j += 1

    ymax *= 1.2
    ymin *= 0.9
    ax.set_ylim(ymin, ymax)
    ax.set_ylabel('Time')
    ax.set_title('Time for ' + size)
    ind = arange(j)
    ax.set_xticks(ind * width * 6 + width * 2)
    ax.set_xlim(0, 6 * width * j + 2 * width)
    ax.set_xticklabels(textlabels)
    ax.set_yticks(arange(ymin, ymax, round((ymax - ymin) / 10, 2)))
    labels = [Rectangle((0, 0), 1, 1, fc=c, alpha=0.8, linewidth=0)
              for c in ["r", "g", "orange", "b"]]
    ax.legend(labels, ["LRU", "MRU", "LFU", "FIFO"], loc=2, frameon=False)
    plt.minorticks_on()
    plt.tick_params(axis="x", which='both', bottom='off', top='off',
                    labelbottom='on')
    plt.tick_params(axis="y", which='both', left='off', right='off',
                    labelleft='off')
    #plt.grid(True, which='both', axis='y')
    plt.box()
    #plt.show()
    #exit(0)
    plt.savefig("./result/compare_" + size + ".png", format="png")
