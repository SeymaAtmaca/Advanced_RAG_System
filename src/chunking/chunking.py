import nltk
nltk.download("punkt")
nltk.download("punkt_tab")
from nltk.tokenize import sent_tokenize 


# def sentence_chunking(text, max_len=1000):
#     sentences = sent_tokenize(text, language="turkish")
#     chunks = []
#     current = ""

#     for sent in sentences:
#         if len(current) + len(sent) <= max_len:
#             current += " " + sent 
#         else:
#             chunks.append(current.strip())
#             current = sent 

#     if current:
#         chunks.append(current.strip())


def chunk_documents(documents, chunk_size=1500, overlap=200):
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


