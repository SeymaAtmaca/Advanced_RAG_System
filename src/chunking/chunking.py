import nltk
nltk.download("punkt")
nltk.download("punkt_tab")
from nltk.tokenize import sent_tokenize 


def chunk_documents(documents, chunk_size=500, overlap=100):
    chunks = []

    for doc in documents:
        text = doc["text"]
        page_num = doc["page_num"]

        start = 0
        while start < len(text):
            end = start + chunk_size 
            chunk_text = text[start:end]

            chunks.append({
                "text": chunk_text,
                "page": page_num
            })

            start = end - overlap 
    
    return chunks

