# Coordinates are given as points in the complex plane
from svgpathtools import Path, Line, QuadraticBezier, CubicBezier, Arc, svg2paths, parse_path, svg2paths2
import numpy as np
import pandas as pd
import soundfile as sf
# velocity = input("Enter Velocity\n")
# name = input("Enter Output name\n")





paths, attributes, svg_attributes = svg2paths2('Misc\SVG/Artboard 1_2.svg')
print(type(paths))
print(len(paths))
total = 0

lst = svg_attributes['viewBox'].split()
xminus = int(lst[2])/2
yminus = int(lst[3])/2 
divno = max(xminus,yminus)
for i in range(len(paths)):
    mypath = paths[i]
    total = total + mypath.length()
    # print(mypath)
    # print(mypath.point(0))
    # print(mypath.point(0.1))
    # print(mypath.point(0.3))
    # print(mypath.point(0.5))
    # print(type(mypath.point(1)))
print ("total = ", total)
vel = total / 20000
print ("Velocity = ", int(vel))
arr = np.zeros((0,2))
for i in range(len(paths)):
    curpath = paths[i]
    # for j in range(0, int(mypath.length()), int(vel)):
    for j in np.arange(0, mypath.length(), vel):
        arr = np.append(arr,[[(curpath.point(j/mypath.length()).real - xminus)/divno,(yminus - curpath.point(j/mypath.length()).imag)/divno]], axis = 0)
# for i in range(10):
#     arr = np.append(arr,arr,axis = 0)
sf.write('testhbd2.wav', arr, 48000)  



