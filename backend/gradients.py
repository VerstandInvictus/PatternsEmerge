from __future__ import division

gradient = ["#BD00B5",
            "#B306B5",
            "#A90CB5",
            "#9F12B6",
            "#9519B6",
            "#8B1FB7",
            "#8125B7",
            "#772CB7",
            "#6D32B8",
            "#6338B8",
            "#593FB9",
            "#4F45B9",
            "#454BBA",
            "#3B52BA",
            "#3158BA",
            "#275EBB",
            "#1D65BB",
            "#136BBC",
            "#0971BC",
            "#0078BD",]


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
