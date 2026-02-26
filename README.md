# 🚀 End-to-End RAG System (FastAPI + Vector Search + LLM)

Production-style Retrieval-Augmented Generation system for ingesting PDFs, performing semantic search, and generating grounded answers using LLMs.

---

## ✨ Features

✅ Async PDF ingestion with background indexing  
✅ Intelligent text chunking + metadata enrichment  
✅ Duplicate chunk removal using hashing  
✅ Semantic embeddings for retrieval  
✅ Vector similarity search  
✅ Context-grounded LLM answering  
✅ Retry logic for LLM reliability  
✅ Production logging & observability  

---

## 🧠 Architecture

1. Upload PDF → background processing  
2. PDF parsing → text extraction  
3. Chunking → metadata enrichment  
4. Deduplication → embedding generation  
5. Vector indexing  
6. Query embedding → similarity search  
7. LLM generates grounded answer  

---

## ⚙️ Tech Stack

* FastAPI
* OpenAI embeddings
* Vector similarity search
* NumPy
* Async background tasks

---

## 📸 Demo

### Upload API
![Upload](screenshots/upload_api.png)

### Query Response
![Query](screenshots/query_response.png)

---

## 🚀 Run Locally

```bash
git clone <repo>
cd RAG_END_TO_END
pip install -r requirements.txt
uvicorn app.main:app --reload
