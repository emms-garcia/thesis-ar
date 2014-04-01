#!/usr/bin/python
import random
import numpy

N = 30

file_names = ["lux.dat", "imsize.dat", "qrsize.dat", "multiple.dat"]

#Iluminacion
x = [(i*(1000/N) + 250) for i in range(N)]
y = numpy.random.poisson(1.0, N) 
with open("lux.dat", "w") as file:
  for i in range(N):
    file.write("%s %s\n"%(x[i], y[i]))




#Resolucion QR


#Multiples QR
