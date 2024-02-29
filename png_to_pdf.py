from PIL import Image
import os
def convert_img_pdf(filepath, output_path):
    output = Image.open(filepath)
    output.save(output_path, "pdf", save_all=True)
if __name__ == "__main__":
    convert_img_pdf("test.jpg","test.pdf")