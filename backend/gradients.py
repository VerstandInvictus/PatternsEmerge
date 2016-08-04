from __future__ import division

gradient = ["#8206E0",
            "#8718C9",
            "#901AC5",
            "#981CC2",
            "#A11EBE",
            "#AA21B9",
            "#B324B6",
            "#B928AA",
            "#BF3193",
            "#C4397B",
            "#CA4165",
            "#CF4A4B",
            "#D55234",
            "#DB5B1C",]


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
