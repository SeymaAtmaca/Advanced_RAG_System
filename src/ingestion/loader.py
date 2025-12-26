

from PyPDF2 import PdfReader
import re

def load_pdf(path: str) -> str:
  reader = PdfReader(path)
  pages = []

  for page in reader.pages:
    text = page.extract_text()
    if text:
      pages.append(text)

  return "\n".join(pages)

def clean_text(text:str) -> str:
  text = re.sub(r'\s+',' ', text)
  text = re.sub(r'\n+', '\n', text)
  return text.strip()