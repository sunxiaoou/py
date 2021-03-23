#! /usr/bin/python3
import re
import sys

import tesserocr
from PIL import Image, ImageEnhance


def image2text(image_name: str) -> str:
    image = Image.open(image_name)
    image = image.convert('L')
    new_size = tuple(2 * x for x in image.size)             # enlarge the image size
    image = image.resize(new_size, Image.ANTIALIAS)
    # image.show()
    return tesserocr.image_to_text(image, lang='eng+chi_sim', psm=tesserocr.PSM.SINGLE_BLOCK)


def main():
    if len(sys.argv) < 2:
        print("Usage: {} img".format(sys.argv[0]))
        sys.exit(1)

    print(image2text(sys.argv[1]))


if __name__ == "__main__":
    main()
