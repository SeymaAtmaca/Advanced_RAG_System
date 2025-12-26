from loader import load_pdf, clean_text 
from chunking import fixed_chucking, sentence_chunking 

pdf_path = "data/raw_pdfs/InceMemed2.pdf"

raw = load_pdf(pdf_path)
cleaned = clean_text(raw) 

fixed = fixed_chucking(cleaned) 
sentence = sentence_chunking(cleaned) 

print("FIXED SAMPLE:\n", fixed[1])
print("\nSENTENCE :\n", sentence[1])