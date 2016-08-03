from __future__ import division
from colour import Color

red = Color(rgb=(86/255, 77/255, 143/255))
yellow = Color(rgb=(170/255, 83/255, 151/255))
green = Color(rgb=(233/255, 145/255, 45/255))

ry = red.range_to(yellow, 30)
yg = yellow.range_to(green, 30)
gradient = [red.hex] + [x.hex for x in ry] + [yellow.hex] + \
           [x.hex for x in yg] + [green.hex]


def findColor(low, high, val):
    spread = high - low
    ratio = (val - low) / spread
    index = int(ratio * len(gradient))
    if index < 0:
        return gradient[0]
    try:
        return gradient[index]
    except IndexError:
        return gradient[-1]

if __name__ == "__main__":
    print findColor(-100, 200, -130)
