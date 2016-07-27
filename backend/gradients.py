from __future__ import division
from colour import Color

red = Color(rgb=(230/255, 124/255, 115/255))
yellow = Color(rgb=(1, 214/255, 102/255))
green = Color(rgb=(87/255, 187/255, 138/255))

ry = red.range_to(yellow, 12)
yg = yellow.range_to(green, 12)
gradient = [red.hex] + [x.hex for x in ry] + [yellow.hex] + \
           [x.hex for x in yg] + [green.hex]


def findColor(low, high, val):
    spread = high - low
    ratio = val / spread
    index = int(ratio * len(gradient))
    return gradient[index-1]

if __name__ == "__main__":
    print findColor(-75, 350, 40)
