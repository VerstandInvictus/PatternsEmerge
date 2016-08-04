from __future__ import division
from colour import Color

gradient = [
    "#8701e8",
    "#9805DC",
    "#9e06d7",
    "#a909cf",
    "#c00ebf",
    "#d813ad",
    "#f81a96",
    "#ff2f76",
    "#ff346f",
    "#ff4458",
    "#ff5048",
    "#ff5a39",
    "#ff622e",
    "#ff6c20",]

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
    print gradient
    print findColor(0, 690, 595)
