# app/main.py
import logging
from fastapi import FastAPI, UploadFile, File, Query,BackgroundTasks
from app.core.config import settings
from app.utils.file_handler import save_upload_file
from app.utils.pdf_parser import extract_text_from_pdf
from app.utils.chunker import chunk_text
from app.utils.chunk_metadata import add_metadata_to_chunks
from app.utils.embeddings import embed_chunks, embed_query
from app.utils.vectorstore import add_chunks_to_index, query_index
import openai
import numpy as np
import time
import hashlib
import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")



# ---------------- Logging ----------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)
logger = logging.getLogger("rag1")

# ---------------- FastAPI App ----------------
app = FastAPI(title=settings.app_name)

  # Masked logging

# ---------------- Endpoints ----------------
@app.get("/")
def root():
    return {"message": f"{settings.app_name} backend is running"}

@app.get("/health")
def health():
    return {"status": "ok", "env": settings.environment}

# -# ---------------- PDF Processing Function ----------------
def process_pdf(file_path: str, filename: str):
    try:
        logger.info(f"Started processing: {filename}")
        pdf_text = extract_text_from_pdf(file_path)
        chunks = chunk_text(pdf_text)
        chunk_objects = add_metadata_to_chunks(chunks, filename)

        # Deduplicate chunks
        chunk_hashes = set()
        unique_chunks = [
            c for c in chunk_objects
            if hashlib.md5(c['text'].encode()).hexdigest() not in chunk_hashes
            and not chunk_hashes.add(hashlib.md5(c['text'].encode()).hexdigest())
        ]
        logger.info(f"Unique chunks for {filename}: {len(unique_chunks)}")

        # Embed chunks
        embedded_chunks = embed_chunks(unique_chunks)

        # Add to vector store
        add_chunks_to_index(embedded_chunks)
        logger.info(f"Finished processing {filename}: {len(embedded_chunks)} chunks indexed.")
    except Exception as e:
        logger.exception(f"Error processing PDF {filename}: {e}")

# ---------------- Upload PDF Endpoint ----------------
@app.post("/upload-pdf/")
async def upload_pdf(file: UploadFile = File(...), background_tasks: BackgroundTasks = None):
    try:
        logger.info(f"Received upload: {file.filename}")
        file_path = await save_upload_file(file)

        # Background processing
        background_tasks.add_task(process_pdf, file_path, file.filename)

        return {"message": f"File {file.filename} is being processed in the background."}
    except Exception as e:
        logger.exception("Error during PDF upload")
        return {"error": str(e)}


# ---------- Ask ----------
@app.get("/ask/")
async def ask(question: str = Query(..., description="Your question about uploaded PDFs")):
    try:
        logger.info(f"Question received: {question}")
        query_emb = np.array(embed_query(question)).reshape(1, -1)
        top_chunks = query_index(query_emb, top_k=5)

        # Deduplicate top chunks
        unique_chunks = list({c['chunk_id']: c for c in top_chunks}.values())
        if not unique_chunks:
            return {"answer": "No relevant info found in uploaded documents."}

        context_text = "\n\n".join([c["text"] for c in unique_chunks])
        client = openai.OpenAI(api_key=OPENAI_API_KEY
)

        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Answer based on context:\n\n{context_text}\n\nQuestion: {question}"}
        ]

        # Retry mechanism
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=messages,
                    max_tokens=300,
                    temperature=0
                )
                answer = response.choices[0].message.content
                break
            except Exception as e:
                logger.warning(f"OpenAI request failed: {e}")
                if attempt < max_retries - 1:
                    time.sleep(1)
                else:
                    return {"answer": "OpenAI request failed after multiple retries."}

        return {"answer": answer}

    except Exception as e:
        logger.exception("Error in /ask")
        return {"error": str(e)}
