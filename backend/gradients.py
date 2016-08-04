from __future__ import division
from colour import Color

sunburst = ["#8206E0",
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

deepblue = ["#8300e9",
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

red = Color(rgb=(230/255, 124/255, 115/255))
yellow = Color(rgb=(1, 214/255, 102/255))
green = Color(rgb=(87/255, 187/255, 138/255))

ry = red.range_to(yellow, 12)
yg = yellow.range_to(green, 12)
hprographics = [x.hex for x in ry] + [x.hex for x in yg]

themes = {
    "hprographics": hprographics,
    "deepblue": deepblue,
    "sunburst": sunburst
}


def findColor(low, high, val, theme):
    spread = high - low
    ratio = (val - low) / spread
    index = int(ratio * len(themes[theme]))
    if index < 0:
        return themes[theme][0]
    try:
        return themes[theme][index]
    except IndexError:
        return themes[theme][-1]

if __name__ == "__main__":
    print themes
    print findColor(0, 690, 595, 'hprographics')
