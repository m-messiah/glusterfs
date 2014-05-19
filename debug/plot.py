#!/usr/bin/python
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from numpy import arange
j=0
#plt.xkcd()
for rule in ["seq", "rand"]:
    for thread in ["1", "2", "5", "write"]:
        for i in ["10k", "100k", "200k", "1M", "10M"]:
            for t in [1000, 250]:
                try:
                    plt.figure(j)
                    for algo, color in [("LRU", ("r", 1)),
                                        ("MRU", ("g", 0.7)),
                                        ("LFU", ("orange", 0.5)),
                                        ("FIFO", ("b", 0.5))]:
                        print algo
                        x=map(float,
                            open("./result/" + algo + "/"
                                 + rule + thread + "*" + str(t) + "*" + i + ".txt",
                                 'r').readlines())
                        plt.plot(range(len(x)), x,
                                 color[0], label=algo, alpha=color[1])
    
                    plt.ylabel("Sec/file")
                    if i == "10k":
                        ymin, ymax, tick = 0.15, 0.5, 0.05
                    elif i == "100k":
                        ymin, ymax, tick = 0.15, 0.6, 0.05
                    elif i == "200k":
                        y = 0.6
                        if thread == "write":
                            ymin, tick = 0.3, 0.01
                        else:
                            ymin, tick = 0.2, 0.05
                    elif i == "1M":
                        if thread == "5":
                            ymin, ymax, tick = 0.3, 0.8, 0.05
                        elif thread == "write":
                            ymin, ymax, tick = 0.7, 1.4, 0.05
                        else:
                            ymin, ymax, tick = 0.2, 0.6, 0.05
                    elif i == "10M":
                        if thread == "1":
                            ymin, ymax, tick = 0, 2, 0.1
                        elif thread == "2":
                            ymin, ymax, tick = 0, 16, 1
                        elif thread == "5":
                            ymin, ymax, tick = 0, 20, 1
                        else:
                            ymin, ymax, tick = 3, 5, 0.1  
                    plt.ylim(ymin, ymax)
                    plt.yticks(arange(ymin, ymax, tick))
                    plt.xticks(arange(0, 1000, 100))
                    plt.grid(True, which='both', axis='both')
                    plt.legend()
                    plt.title(rule.capitalize())
                    plt.savefig("./result/img/" + rule
                                + thread + "*" + str(t) + "*" + i + ".png",
                                format="png")
                    print("Saved " + i + " * " + str(t))
                    j+=1
                except Exception as e:
                    print e
