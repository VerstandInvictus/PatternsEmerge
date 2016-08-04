from __future__ import division

gradient = ["#7818d8",
            "#7800d8",
            "#7800f0",
            "#6030d8",
            "#6018d8",
            "#4848d8",
            "#4830d8",
            "#4848c0",
            "#3048c0",
            "#3060c0",
            "#1860c0",
            "#1878c0",
            "#1890c0",
            "#18a8c0",
            "#18c0d8",
            "#18a8d8",]


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
