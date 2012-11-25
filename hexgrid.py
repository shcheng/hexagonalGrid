#!/usr/bin/python

#
# hexgrid.py
# by Shih-Ho Cheng (shihho.cheng@gmail.com)
#

import sys
import numpy as np
import math as m
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.collections import PatchCollection

if (len(sys.argv)==1):
  allPixFlag = True
elif (len(sys.argv)==2):
  inputFileName = sys.argv[1]
  allPixFlag = False
else:
  print "Usage:", sys.argv[0], "[list of pixels]"
  print "(If no argument is present, it prints all the pixels)"
  sys.exit(1)

s_chnList = []
chnList = []
if(allPixFlag):
  for i in range(1,441):
    chnList.append(i)
  s_chnList = map(str, chnList)
else:
  inFile = file(inputFileName)
  for line in inFile:
    s_chnList.append( line.split()[0] )
  chnList = map(int, s_chnList)

# Get the Hex col and row displacement
# Output: [dc,dr] row and column displacement
def getHexDispl(seed, nchn):
  srow = seed%22
  if srow==0:
    srow = 22
  scol = (seed-srow)/22 + 1
  nrow = nchn%22
  if nrow==0:
    nrow = 22
  ncol = (nchn-nrow)/22 + 1
  return [ncol-scol, nrow-srow]

# Some constants of the unit hexagon
A = 0.025
a = A * m.sqrt(3.)/2.
b = A/2.
x_o = 4.5 * A 
y_o = 4.*A

# Draw the necessary hexagons
positions = []
patches = []
x = x_o
y = y_o
deltaCR = getHexDispl(1,chnList[0])
if (chnList[1]%2!=0):
  offset = 0
else:
  offset = -a
deltaX = deltaCR[0] * 2.*a + offset
deltaY = deltaCR[1] * (A+b)
x = x + deltaX
y = y + deltaY
patches.append(mpatches.RegularPolygon((x,y), 6, A))
positions.append([x,y])
for i in range(1,len(chnList)):
  deltaCR = getHexDispl(chnList[i-1],chnList[i])
  if (chnList[i-1]%2)==(chnList[i]%2):
    offset = 0
  elif (chnList[i-1]%2==0) and (chnList[i]%2!=0):
    offset = a
  else:
    offset = -a
  deltaX = deltaCR[0] * 2.*a + offset
  deltaY = deltaCR[1] * (A+b)
  x = x + deltaX
  y = y + deltaY
  patches.append(mpatches.RegularPolygon((x,y), 6, A))
  positions.append([x,y])
hexGrid = PatchCollection(patches, facecolor='none', edgecolor='black')

# Plot 
fig = plt.figure()
ax = plt.axes([0,0,1,1])
ax.add_collection(hexGrid)
for i in range(len(positions)):
  ax.text(positions[i][0], positions[i][1], s_chnList[i], ha='center', size=10, va='center')
plt.setp(ax, xticks=[], yticks=[])
#plt.savefig("FD-HexGrid.png")
plt.show()
