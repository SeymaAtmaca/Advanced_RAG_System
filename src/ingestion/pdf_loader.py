

from PyPDF2 import PdfReader
import re

def load_pdf(path: str) -> str:
  reader = PdfReader(path)
  docts = []

  for page_num, page in enumerate(reader.pages):
    text = page.extract_text()
    if text:
      docts.append({
        "text": page,
        "page_num": page_num + 1
      })
      

  return docts

def clean_text(text:str) -> str:
  text = re.sub(r'\s+',' ', text)
  text = re.sub(r'\n+', '\n', text)
  return text.strip()