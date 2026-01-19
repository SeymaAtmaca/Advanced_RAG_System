# 🧠 Local PDF Chat — Advanced RAG Desktop Application

> A production-grade **Retrieval-Augmented Generation (RAG)** desktop application  
> built with **PyQt5**, **FAISS**, **SentenceTransformers**, and **Ollama**.

This application allows users to load one or more PDFs, build persistent vector
indexes, and chat with a local LLM grounded strictly in document content.

---

## 🚀 Key Highlights

- Fully local & offline-capable (except Ollama runtime)
- Multi-PDF support with isolated memory per document
- Persistent embedding & FAISS index caching
- Context packing for higher answer quality
- Packaged as a standalone Windows `.exe`
- Designed with **AI system engineering** best practices

---

## 🧩 Core Features

### 📄 Document Ingestion
- PDF parsing via **PyPDF2**
- Page-level text extraction
- Robust text cleaning & chunking
- Metadata preservation (PDF source, page index)

### 🔍 Vector Search
- Sentence embeddings using:
  - `paraphrase-multilingual-mpnet-base-v2`
- FAISS `IndexFlatIP` (cosine similarity)
- Batched embedding generation with progress feedback

### 🧠 Advanced RAG Pipeline
- Dense retrieval (FAISS)
- Context packing (top-ranked chunks packed optimally)
- Strict grounding: LLM answers using **only retrieved context**
- Per-PDF conversational memory

### ⚡ Performance Optimizations
- **Embedding cache** (PDF hash-based)
- Persistent FAISS index on disk
- No re-embedding for previously indexed PDFs

### 💬 Desktop UI (PyQt5)
- Modern dark theme
- WhatsApp-style chat bubbles
- Modal loading dialog with real progress (%)
- Sidebar with loaded PDFs
- Active PDF switching

---

## 🏗️ Architecture Overview
```
UI (PyQt5)
├── MainWindow
│ ├── Chat UI
│ ├── PDF Sidebar
│ └── Loading Dialog
│
└── RAGController
├── PDF Loader
├── Chunker
├── Embedder
├── FAISS Store
├── Context Packer
├── Prompt Builder
├── Chat Memory
└── Ollama LLM
```

---

## 📁 Project Structure

```
RAG/
├── app/
│ ├── ui/
│ ├── workers/
│ ├── controller.py
│ └── main.py
│
├── src/
│ ├── ingestion/
│ ├── chunking/
│ ├── embedding/
│ ├── vectorstore/
│ ├── rag/
│ ├── llm/
│ └── utils/
│
├── data/
│ ├── embeddings/ # Cached embeddings (hash-based)
│ ├── faiss/ # Persistent FAISS indexes
│ └── raw_pdfs/
│
├── dist/ # Built executable
├── assets/
├── README.md
└── requirements.txt

```
---

## 🧠 Embedding Cache Strategy

To avoid recomputing embeddings:

1. PDF content is hashed (SHA256)
2. Embeddings are stored as `.npy`
3. FAISS index & metadata are saved to disk
4. On reload:
   - If hash exists → load embeddings & index
   - Else → compute & cache

This provides **massive speed-up** and is critical for production systems.

---

## 🖥️ Build Instructions (EXE)

```bash
pip install -r requirements.txt
pyinstaller LocalPdfChat.spec
```



🇹🇷 Türkçe Açıklama
🧠 Yerel PDF Sohbet — Gelişmiş RAG Masaüstü Uygulaması

Bu proje, PDF belgelerle konuşabilen, tamamen yerel çalışan,
profesyonel seviyede bir RAG (Retrieval-Augmented Generation) sistemidir.

🎯 Temel Özellikler

* PDF yükleme ve parçalama
* FAISS ile vektör arama
* Embedding cache (hash tabanlı)
* Context packing (cevap kalitesi artışı)
* Çoklu PDF desteği
* PDF başına ayrı sohbet hafızası
* PyQt5 ile modern masaüstü arayüz
* PyInstaller ile .exe paketleme




📜 License

MIT License — free to use, modify, and distribute.