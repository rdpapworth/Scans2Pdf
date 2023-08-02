from PIL import Image
import os
import math
from PyPDF2 import PdfWriter
import img2pdf

def extract_numeric_part(filename):
    return int(filename.split('(')[1].split(')')[0])

def crop_and_split_images(source_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    filenames = sorted([f for f in os.listdir(source_dir) if f.endswith('.png')], key=extract_numeric_part)
    
    for filename in filenames:
        filepath = os.path.join(source_dir, filename)
        image = Image.open(filepath)
        width, height = image.size

        # Crop the image by removing 85px from the top, bottom, left, and right
        cropped_image = image.crop((85, 85, width - 85, height - 85))

        # Split the cropped image into two equal halves
        half_width = int(math.ceil(cropped_image.width / 2))
        left_image = cropped_image.crop((0, 0, half_width, cropped_image.height))
        right_image = cropped_image.crop((half_width, 0, cropped_image.width, cropped_image.height))

        # Save the left and right images to the output directory
        left_image.save(os.path.join(output_dir, f"{filename.split('.')[0]}_left.png"))
        right_image.save(os.path.join(output_dir, f"{filename.split('.')[0]}_right.png"))

def create_pdf_from_images(images_dir, output_pdf_path):
    filenames = sorted([f for f in os.listdir(images_dir) if f.endswith('.png')], key=extract_numeric_part)
    filenames = [os.path.join(images_dir, f) for f in filenames]

    with open(output_pdf_path, 'wb') as pdf_output:
        pdf_output.write(img2pdf.convert(filenames))
        #pdf_writer.write(pdf_output)


if __name__ == "__main__":
    source_directory = r"\Pictures\Screenshots\101 Games"
    output_directory = r"\Pictures\Screenshots\101 Games2"
    output_pdf_path = r"\Pictures\Screenshots\101_Games.pdf"

    crop_and_split_images(source_directory, output_directory)
    create_pdf_from_images(output_directory, output_pdf_path)
