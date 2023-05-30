import pytesseract
from PIL import Image

def extract_text_from_image(image_path):
    # Open the image using PIL
    image = Image.open(image_path)

    # Use Tesseract to extract text from the image
    text = pytesseract.image_to_string(image)

    return text

image = "img.png"
extracted = extract_text_from_image(image)
print(extracted)