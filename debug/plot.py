#!/usr/bin/python
import numpy
from matplotlib import pyplot as plt
x=map(float, open("1.txt",'r').readlines())
plt.plot(range(len(x)), x, 'r')
plt.grid(True)
plt.savefig('foo.png')
