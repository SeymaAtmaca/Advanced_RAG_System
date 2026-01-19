import hashlib
from typing import List, Dict


def hash_documents(documents: List[Dict]) -> str:
    """
    PDF content hash (deterministic)

    documents format:
    [
        { "text": "...", "page": 1 },
        ...
    ]
    """
    hasher = hashlib.sha256()

    for doc in documents:
        # order + content must be stable
        hasher.update(doc["text"].encode("utf-8"))
        # hasher.update(str(doc["page"]).encode("utf-8"))

    return hasher.hexdigest()
