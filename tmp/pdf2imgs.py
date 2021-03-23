#! /usr/bin/python3
import sys

import fitz
import io
from PIL import Image


def pdf2imgs(pdf_name: str):
    pdf_file = fitz.open(pdf_name)

    # iterate over PDF pages
    for page_index in range(len(pdf_file)):
        # get the page itself
        page = pdf_file[page_index]
        image_list = page.getImageList()
        # printing number of images found in this page
        if image_list:
            print(f"[+] Found a total of {len(image_list)} images in page {page_index}")
        else:
            print("[!] No images found on page", page_index)
        for image_index, img in enumerate(page.getImageList(), start=1):
            # get the XREF of the image
            xref = img[0]
            # extract the image bytes
            base_image = pdf_file.extractImage(xref)
            image_bytes = base_image["image"]
            # get the image extension
            image_ext = base_image["ext"]
            # load it to PIL
            image = Image.open(io.BytesIO(image_bytes))
            # save it to local disk
            # image.save(open("image{page_index+1}_{image_index}.{image_ext}", "wb"))
            image.save(open("image{0:02d}_{1}.{2}".format(page_index+1, image_index, image_ext), "wb"))


def main():
    if len(sys.argv) < 2:
        print("Usage: {} img".format(sys.argv[0]))
        sys.exit(1)

    pdf2imgs(sys.argv[1])


if __name__ == "__main__":
    main()
