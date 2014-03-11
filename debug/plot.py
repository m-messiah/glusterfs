#!/usr/bin/python
import matplotlib
matplotlib.use('svg')
import matplotlib.pyplot as plt
j=0
#for i in ["1k", "4k", "10k", "100k", "1M", "10M", "40M", "80M", "100M", "1G"]:
for i in ["1G"]:
	try:
		plt.figure(j)
		x=map(float, open("./result/LRU/1*10000*" + i + ".txt", 'r').readlines())
		plt.plot(range(len(x)), x, 'r')
		plt.grid(True)
		plt.savefig("./result/LRU/1*10000*" + i + ".svg")
		print("Saved " + i)
		j+=1
	except:
		pass
