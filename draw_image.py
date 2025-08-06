import sys
import cv2
from cv2.typing import MatLike
from numpy.char import add as ncadd


def rgb_to_ansi(r, g, b):
    return f"{r};{g};{b}"

def draw_image(image: MatLike):
    char = "█"

    sys.stdout.write("\033[?25l") # カーソル非表示
    sys.stdout.write("\033[H") # 左上
    sys.stdout.flush()

    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    r = rgb_image[:, :, 0].astype(str)
    g = rgb_image[:, :, 1].astype(str)
    b = rgb_image[:, :, 2].astype(str)

    start="\033[38;2;"
    end=f"m{char}\033[0m"

    ansi = ncadd(ncadd(ncadd(ncadd(ncadd(ncadd(start, r), ";"), g), ";"), b), end)

    print("\n".join(["".join(row) for row in ansi]))