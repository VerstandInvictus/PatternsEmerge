from __future__ import division

gradient = ["#8300e9",
            "#790be5",
            "#6f16e0",
            "#5e2ad9",
            "#4f3ad1",
            "#3f4cca",
            "#2e5ec2",
            "#1f6fbb",
            "#1678b6",
            "#1489bd",
            "#159ac7",
            "#16a5cd",
            "#16abd1",
            "#17b8d8",]


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
