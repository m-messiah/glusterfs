#!/usr/bin/python
from operator import itemgetter
import matplotlib

#matplotlib.use('Agg')
import matplotlib.pyplot as plt
from numpy import arange
from matplotlib.pyplot import Rectangle

#plt.xkcd()

red, green, orange, blue = "#e9655a", "#8fb283", "#d6c04a", "#00b7c7"
ind = arange(4)
ymin, ymax = 100, 0
width = 1
for size in ["10k", "100k", "200k", "1M", "10M"]:
    if size == "1M":
        textlabels = filter(
            lambda a: a != "wrm" and a != "wsm",
            [i + s + rep
             for i in ["1", "2", "5", "w"]
             for s in ["s", "r"] for rep in ["", "m"]])
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
                for algo, color, offset in [("LRU", red, 0),
                                            ("MRU", green, 1),
                                            ("LFU", orange, 2),
                                            ("FIFO", blue, 3)]:
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

                for mean, color in sorted(means, key=itemgetter(0),
                                          reverse=True):
                    rects.append(
                        ax.bar((j if j < 14 else 13) * width * 2,
                               mean, width, linewidth=0, color=color))
                j += 1

    ymax *= 1.01
    ymin *= 0.95
    ax.set_ylim(ymin, ymax)
    #ax.set_ylabel('Time')
    ax.set_title('Time for ' + size)
    j = j if j < 15 else 14
    ind = arange(j)
    ax.set_xticks(ind * width * 2 + width / 2.)
    ax.set_xlim(0, 2 * width * j)
    ax.set_xticklabels(textlabels)
    ax.set_yticks(arange(ymin, ymax, round((ymax - ymin) / 10, 2)))
    labels = [Rectangle((0, 0), 1, 1, fc=c, alpha=0.8, linewidth=0)
              for c in [red, green, orange, blue]]
    ax.legend(labels, ["LRU", "MRU", "LFU", "FIFO"], loc=2, frameon=False)
    plt.minorticks_on()
    plt.tick_params(axis="x", which='both', bottom='off', top='off',
                    labelbottom='on')
    plt.tick_params(axis="y", which='both', left='off', right='off',
                    labelleft='off')
    #plt.grid(True, which='both', axis='y')
    plt.box()
    #fig.set_size_inches(12, 8)
    #plt.show()
    #exit(0)
    plt.savefig("./result/compare_" + size + ".png", format="png",
                dpi=300, bbox_inches='tight')
