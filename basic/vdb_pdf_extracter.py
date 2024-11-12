import fitz  # PyMuPDF
import io
from PIL import Image
import string
import nltk
from nltk.corpus import stopwords
import os
import re
nltk.download('stopwords')
def extract_text_from_page(page):
    """Extracts text from a PDF page."""
    return page.get_text("text")

def extract_images_from_page(page, image_folder="images"):
    """Extracts images from a PDF page."""
    image_list = []
    for img_index, img in enumerate(page.get_images(full=True)):
        xref = img[0]
        base_image = page.get_image(xref)
        image_bytes = base_image["image"]
        image = Image.open(io.BytesIO(image_bytes))

        # Save the image
        if not os.path.exists(image_folder):
            os.makedirs(image_folder)
        img_path = f"{image_folder}/image_{page.number + 1}_{img_index + 1}.png"
        image.save(img_path)
        image_list.append(img_path)
    return image_list

def extract_tables_from_page(page):
    """Extracts tables from a PDF page by looking for structures resembling tables."""
    text = page.get_text("text")
    tables = []
    current_table = []
    for line in text.split('\n'):
        if re.match(r'(\s*[-\|]+\s*)+', line):  # Assuming table border lines
            if current_table:
                tables.append('\n'.join(current_table))
                current_table = []
        else:
            current_table.append(line)
    if current_table:
        tables.append('\n'.join(current_table))
    return tables
def clean_text(text):
    # Convert text to lowercase
    #text = text.lower()

    # Remove URLs
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    
    # Remove HTML tags
    text = re.sub(r'<.*?>', '', text)
    
    # Remove special characters but keep currency symbols, dates, and numbers
    text = re.sub(r'[^\w\s\$€£¥%/\-.,]', '', text)
    
    # Remove stopwords (optional, based on requirement)
    #stop_words = set(stopwords.words('english'))
    #text = ' '.join([word for word in text.split() if word not in stop_words])
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def extract_from_pdf(pdf_path, image_folder="images"):
    doc = fitz.open(pdf_path)
    all_content = []

    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        text = extract_text_from_page(page)
        text = clean_text(text)
        #images = extract_images_from_page(page, image_folder)
        #tables = extract_tables_from_page(page)

        page_content = {
            "page_number": page_num + 1,
            "text": text,
        }

        all_content.append(page_content)

    return all_content

def format_content(content):
    formatted_text = ""
    for page in content:
        formatted_text += f"\n\n[Page {page['page_number']}]\n\n"
        
        if page["text"]:
            formatted_text += f"[Text]\n{page['text']}\n"
        
        # if page["tables"]:
        #     for i, table in enumerate(page["tables"]):
        #         formatted_text += f"\n[Table {i + 1}]\n{table}\n"
        
 
    return formatted_text

# Example usage
pdf_path = "C:/DJ/docs/query/Tesla.pdf"
data = extract_from_pdf(pdf_path)

# Format extracted data
formatted_data = format_content(data)
print(formatted_data)

# Save formatted data to a file for review
with open("extracted_content.txt", "w") as f:
    f.write(formatted_data)
