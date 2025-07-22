from google import genai
import config
from PIL import Image
import pytesseract
from pdf2image import convert_from_path
import sys
import os


file_name = sys.argv[1]



PATH = r'/usr/bin' # Provide your path
pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'  # Provide your path
client = genai.Client(api_key=config.API_KEY)  # Provide your api key
chat = client.chats.create(model="gemini-2.5-flash")


def extract_text_from_scanned_pdf(pdf_path):
    extracted_text = ""
        # Convert PDF pages to images
    print(f"Converting pages of {pdf_path} to images...")
    pages = convert_from_path(pdf_path, poppler_path=PATH)
    for i, img in enumerate(pages):
        img.save(f'page_{i + 1}.jpg', 'JPEG')
    print(f"Processing {len(pages)} pages with OCR...")


    for i, img in enumerate(pages):
        print(f"  Performing OCR on page {i + 1}...")
        # Perform OCR on each image
        im = Image.open(f"page_{i + 1}.jpg")
        text = pytesseract.image_to_string(im)
        os.remove(f"page_{i + 1}.jpg")
        extracted_text += text + "\n--- Page End (OCR) ---\n"

    return extracted_text


def answer(user_input):
    response = chat.send_message(user_input)
    return response.text


scanned_pdf_file = file_name
extracted_text_ocr = extract_text_from_scanned_pdf(scanned_pdf_file)
question = extracted_text_ocr + " Summarize previous text in original language."
summary = (answer(question))
print(summary)

while True:
    question = input(">>> ")
    if question == "quit":
        break
    summary = (answer(question))
    print(summary)


