#!/usr/bin/python
import matplotlib
matplotlib.use('svg')
import matplotlib.pyplot as plt
from numpy import arange
j=0
#plt.xkcd()
for rule in ["seq", "rand"]:
    for thread in ["1", "2", "5"]:
        for i in ["10k", "100k", "200k", "1M", "10M"]:
            for t in [1000]:
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
                    if i[-1] == "k":
                        y = 0.6
                    elif i == "1M":
                        y = 2.0
                    else:
                        y = 20.0
                    plt.ylim(0, y)
                    plt.yticks(arange(0, y, y/10))
                    plt.xticks(arange(0, t, t/10))
                    plt.grid(True, which='both', axis='both')
                    plt.legend()
                    plt.title(rule.capitalize())
                    plt.savefig("./result/img/" + rule
                                + thread + "*" + str(t) + "*" + i + ".svg")
                    print("Saved " + i + " * " + str(t))
                    j+=1
                except Exception as e:
                    print e
