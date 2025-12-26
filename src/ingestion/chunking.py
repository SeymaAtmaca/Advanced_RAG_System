import nltk
nltk.download("punkt")
nltk.download("punkt_tab")
from nltk.tokenize import sent_tokenize 

def fixed_chucking(text, chunk_size=500, overlap=100):
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size 
        chunks.append(text[start:end])
        start = end - overlap 

    return chunks 

def sentence_chunking(text, max_len = 500):
    sentences = sent_tokenize(text, language="turkish")
    chunks = []
    current = ""
    print(f"Chucking size : {len(sentences)}")

    for sent in sentences:
        if len(current) + len(sent) <= max_len:
            current += " " + sent 
        else:
            chunks.append(current.strip())
            current = sent

    if current:
        chunks.append(current.strip())

    return chunks