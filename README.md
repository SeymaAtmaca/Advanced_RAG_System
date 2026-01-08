# 🧠 Advanced RAG Desktop App (PyQt5 + FAISS + Ollama)

A local **Retrieval-Augmented Generation (RAG)** desktop application built with **PyQt5**, **FAISS**, and **Ollama**.  
Users can load PDFs, build vector indexes, and chat with an LLM grounded strictly in the selected document content.

---

## ✨ Features

- 📄 PDF ingestion & chunking
- 🔍 FAISS vector search
- 🧠 RAG pipeline with reranking
- 💬 Chat-based desktop UI (PyQt5)
- ⏳ Modal loading dialog with progress indicator
- 🗂 Loaded PDFs listed in sidebar
- 🧠 Conversation memory support

---

## 🖼 UI Preview

### Main Chat Interface
![Main UI](assets/ui_main.png)

### PDF Indexing (Blocking Loading Dialog)
![Loading Dialog](assets/ui_loading.png)

---

## 🏗 Architecture Overview

```text
UI (PyQt5)
 └── MainWindow
      └── RAGController
           ├── PDF Loader
           ├── Chunker
           ├── Embedder (SentenceTransformer)
           ├── FAISS Store
           ├── Reranker (CrossEncoder)
           └── Ollama LLM
