#!/usr/bin/python
import matplotlib
matplotlib.use('svg')
import matplotlib.pyplot as plt
j=0
for i in ["1k", "4k", "10k", "100k", "1M", "10M", "40M", "80M", "100M", "1024M"]:
	for t in ["1000", "10000"]:
		try:
			plt.figure(j)
			x=map(float, open("./result/FIFO/1*" + t + "*" + i + ".txt", 'r').readlines())
			plt.plot(range(len(x)), x, 'r')
			plt.grid(True)
			plt.savefig("./result/FIFO/1*" + t + "*" + i + ".svg")
			print("Saved " + i)
			j+=1
		except:
			pass
